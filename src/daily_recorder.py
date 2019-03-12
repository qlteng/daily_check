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

sys.path.append('/usr/local/lib/python2.7/dist-packages/itchat/__init__.py')

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
            print item
            with open('../data/%s.txt'%date,'a') as fw:
                fw.write(item)
        except:
            pass

def get_chatroom(chatrooms):
    for c in chatrooms:
        if c['NickName'].encode('utf8')=='每日打卡':
            chat_id=c['UserName']
    return chat_id


itchat.auto_login()
chatrooms = itchat.get_chatrooms(update=True)
chat_id=get_chatroom(chatrooms)
itchat.run()
