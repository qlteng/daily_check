#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 10:16:10 2019

@author: qlteng
"""

import itchat
import itchat.content as co
import datetime
import sys
from process import data_process
from week_info import message_on_sat,message_on_mon,sum_time
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import argparse

LOG_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT)

sys.path.append('/usr/local/lib/python2.7/dist-packages/itchat/__init__.py')

def send_on_mon(dir_prefix):

    df, no_reach = sum_time(7,dir_prefix)

    top3_df = df.sort_values(by='sum_time(h)',ascending=False)
    top3 = []
    for uid in top3_df[:3]['user']:
        top3.append(uid)

    return message_on_mon(top3,no_reach)


def send_on_sat(dir_prefix):

    df, no_reach = sum_time(5,dir_prefix, to_csv = False)

    return message_on_sat(no_reach)


def send_msg(chat_id,dir_prefix,flag):
    txt = None
    if flag == 0:
        txt = data_process(dir_prefix)
    elif flag == 1:
        txt = send_on_sat(dir_prefix)
    elif flag == 2:
        txt = send_on_mon(dir_prefix)
    itchat.send_msg(unicode(txt,'UTF-8'), chat_id.encode('utf-8'))



@itchat.msg_register([co.TEXT, co.SHARING], isGroupChat=True)
def group_reply_text(msg):

    chatroom_id = msg['FromUserName']
    chatroom_id2 = msg['ToUserName']
    username = msg['ActualNickName']
    content=msg['Content']
    now_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(now_time,'%Y-%m-%d %H:%M')
    today = str(datetime.datetime.strftime(datetime.datetime.today(),'%Y-%m-%d'))
    yesterday = str(datetime.datetime.strftime(datetime.datetime.today()-datetime.timedelta(days=1),'%Y-%m-%d'))
    threshold_time = datetime.datetime.strptime("%s 02:00" % today, '%Y-%m-%d %H:%M')

    if chatroom_id == chat_id or chatroom_id2 == chat_id:

        date = ""
        if now_time < threshold_time:
            date = yesterday
        else:
            date = today
        try:
            item = "%s\t%s\t%s\n"%(username.encode('utf8'), content.encode('utf8'), str(timestamp))
            if 'Check Info' in content.encode('utf-8') or 'Check Attention' in content.encode('utf-8'):
                pass
            else:
                with open('%s/data/%s.txt'%(dir_prefix, date),'a') as fw:
                    fw.write(item)
        except:
            pass

def get_chatroom(chatrooms):
    chat_id = None
    for c in chatrooms:
        if c['NickName'].encode('utf8')=='每日打卡':
            chat_id=c['UserName']
            break
    return chat_id


parser = argparse.ArgumentParser()
parser.add_argument('--dir',type = str)
args = parser.parse_args()
dir_prefix = args.dir
itchat.auto_login(enableCmdQR=True)
chatrooms = itchat.get_chatrooms(update=True)
chat_id=get_chatroom(chatrooms)

sched = BackgroundScheduler()
sched.add_job(data_process, 'cron', day_of_week='*', hour=7, minute = 0, second = 0, kwargs={"dir_prefix" : dir_prefix})
sched.add_job(send_msg, 'cron', day_of_week='tue-fri', hour=7, minute = 30, second = 9, kwargs={"chat_id" : chat_id, "dir_prefix" : dir_prefix, "flag":0})
sched.add_job(send_msg, 'cron', day_of_week = 'sat', hour = 7, minute = 30, second = 10, kwargs = {"chat_id": chat_id, "dir_prefix" : dir_prefix, "flag":1})
sched.add_job(send_msg, 'cron', day_of_week = 'mon', hour = 7, minute = 30, second = 11, kwargs = {"chat_id": chat_id, "dir_prefix" : dir_prefix, "flag":2})
sched.start()
itchat.run()




