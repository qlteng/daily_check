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
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import argparse


LOG_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
logging.basicConfig(level = logging.INFO, format = LOG_FORMAT)

sys.path.append('/usr/local/lib/python2.7/dist-packages/itchat/__init__.py')

def send_msg(chat_id,dir_prefix):

    txt = data_process(dir_prefix)
    itchat.send_msg(unicode(txt,'UTF-8'), chat_id.encode('utf-8'))



@itchat.msg_register([co.TEXT, co.SHARING], isGroupChat=True)
def group_reply_text(msg):

    chatroom_id = msg['FromUserName']
    username = msg['ActualNickName']
    content=msg['Content']
    now_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(now_time,'%Y-%m-%d %H:%M')

    if chatroom_id==chat_id:
        date = str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'))
        try:
            item = "%s\t%s\t%s\n"%(username.encode('utf8'), content.encode('utf8'), str(timestamp))
            logging.INFO(item)
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
itchat.auto_login()
chatrooms = itchat.get_chatrooms(update=True)
chat_id=get_chatroom(chatrooms)
sched = BackgroundScheduler()
sched.add_job(send_msg, 'cron',day_of_week='2-6', hour=7, minute = 30,kwargs={"chat_id": chat_id, "dir_prefix" : dir_prefix})
sched.start()
itchat.run()




