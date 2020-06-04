# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from wxpy import *
import schedule

# 开启uid
bot = Bot(False, True)
Bot.enable_puid(bot)
fish_group = ensure_one(bot.groups().search('abc'))
day_total_msg = 0

# 获取群成员
def registe_group_member(group):
    members = []
    for member in group:
        members.append(member)
    return members


members = registe_group_member(fish_group)

# 群成员类
class Member:
    def __init__(self, member):
        self.uid = member.puid
        self.message_count = 0
        self.name = member.nick_name

    def increaseCount(self):
        self.message_count = self.message_count + 1

    def clearCount(self):
        self.message_count = 0

# 消息记录初始化
def init_message_counter(members):
    counters = {}
    for member in members:
        counters[member.puid] = Member(member)
    return counters


counters = init_message_counter(members)


# 最后的提示消息
def notify_message():
    msg_list = counters.values()
    sorted_list = sorted(msg_list, key=lambda e: e.message_count, reverse=True)

    msg = '今日摸🐟排行榜，共摸了' + str(day_total_msg) + '条：\n'
    no = 0
    for member in sorted_list:
        if member.message_count > 0:
            no += 1
            msg += member.name + ':' + '🐟*' + str(member.message_count) + '\n'
    # 完全没人摸鱼
    if no == 0:
        return '今天没人摸🐟'
    else:
        return msg

# 清空当日数据
def clear_fish():
    global day_total_msg
    day_total_msg = 0
    for member in counters:
        counters[member].clearCount()

# 发送消息
def send_message():
    msg = notify_message()
    # fish_group.send(msg)
    bot.file_helper.send(msg)


@bot.register(None, None, False)
def handle_msg(msg):
    if msg.chat == fish_group:
        global day_total_msg
        sender = msg.member
        # 总数 + 1
        day_total_msg += 1

        # 个人 + 1
        counters[sender.puid].increaseCount()
    else:
        return


# 消息提示
# schedule.every().day.at("00:00").do(send_message)
# schedule.every().day.at("00:00").do(clear_fish)
schedule.every().minute.do(send_message)
schedule.every().minute.do(clear_fish)

while True:
    schedule.run_pending()

# 堵塞线程，并进入 Python 命令行
embed()
