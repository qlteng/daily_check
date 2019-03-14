# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 21:30:15 2019

@author: qlteng
"""

import datetime
import re
import pandas as pd

SYMS = ['.','：','。',',','，']
USER = ['王春燕','牛红峰','王丰','张兆哲','李永明','Asif','ashil','雷宗木','丁洁','Nomaan Khan','Muhammad','ZYX赵宇轩','魏昂','朱蓉蓉','闫东超','Shafiq Rai','张陈然','牛军锋','赵颖慧','蔡志波','周存理','滕千礼']
SIMP = ['[',']','#',"'"]

def getYesterday():

    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday

def revise_time(ctn_time, base_time,yesterday):

    ctn_time = "%s %s"%(yesterday, ctn_time)
    ctn_time = datetime.datetime.strptime(ctn_time,'%Y-%m-%d %H:%M')

    base_time = "%s %s"%(yesterday, base_time)
    base_time =  datetime.datetime.strptime(base_time,'%Y-%m-%d %H:%M')

    if base_time - ctn_time > datetime.timedelta(hours = 12):
        ctn_time = ctn_time + datetime.timedelta(hours = 12)

    return datetime.datetime.strftime(ctn_time,'%H:%M')

def match_check(time_list):

    stack = []
    check_timelist = []
    for x in time_list:
        stack.append(x)
        if stack[-1].startswith('out') and len(stack)>=2:
            out_str = stack.pop()
            in_str = stack.pop()
            stack = []
            if datetime.datetime.strptime(out_str.split('#')[1],'%H:%M') - datetime.datetime.strptime(in_str.split('#')[1],'%H:%M') < datetime.timedelta(hours = 8):
                check_timelist.append(in_str)
                check_timelist.append(out_str)
    return check_timelist

def format_io(uid, ctn, time, yesterday):

    try:
        ctn_low = ctn.lower().strip()

        if 'in' not in ctn_low and 'out' not in ctn_low:
            return None

        if ctn_low in ['in','out']:
            return "%s#%s" % (ctn_low, time)

        for split in SYMS:
                ctn_low = ctn_low.replace(split, ':')

        if 'in' in ctn_low and 'out' in ctn_low:

            pattern = re.compile(r'\d+:\d+')
            time_io = re.findall(pattern, ctn_low)

            time_io = sorted([revise_time(x, time, yesterday) for x in time_io])
            return ["in#%s"%time_io[0],"out#%s"%time_io[1]]

        if 'in' in ctn_low or 'out' in ctn_low:
            flag = None
            if 'in' in ctn_low:
                flag = 'in'
            else:
                flag = 'out'

            pattern = re.compile(r'\d+:\d+')
            time_io = re.findall(pattern, ctn_low)

            if time_io == []:
                pattern = re.compile(r'\d+')
                time_io = re.findall(pattern, ctn_low)
                if time_io == []:
                    return "%s#%s" % (flag, time)
                else:
                    time_io[0] = "%s:00"%time_io[0]
                    return "%s#%s" %(flag, revise_time(time_io[0], time, yesterday))
            else:

                return "%s#%s" % (flag, revise_time(time_io[0], time, yesterday))

    except:
        print "Exception in (%s,%s,%s)" %(uid, ctn, time)

def acc_time(time_list):
    acc = datetime.timedelta()
    for x in time_list:
        h,m = [int(x) for x in x.split(':')]
        acc += datetime.timedelta(hours = h, minutes = m)
    return acc

def sum_time(time_list):

    time_delta = acc_time(time_list[1::2])-acc_time(time_list[0::2])
    seconds = time_delta.total_seconds()
    return str(time_delta)[:-3],int(seconds)

def init_dict(yesterday,dir_prefix):

    kv = {}

    for uid in USER:
        if uid not in kv.keys():
                kv[uid] = []
    with open('%s/data/%s.txt'%(dir_prefix,yesterday), 'r') as fr:
        for line in fr:
            line = line.strip()

            uid, ctn, time = line.split('\t')
            time = time.split(' ')[1]
            if uid not in kv.keys():
                kv[uid] = []
            io = format_io(uid, ctn, time, yesterday)
            if io == None:
                continue
            if isinstance(io,list):
                kv[uid].extend(io)
            else:
                kv[uid].append(io)
    return kv

def save_csv(kv,yesterday,dir_prefix):

    res = []
    for uid in kv.keys():
        timelist = kv[uid]
        timelist = timelist[:6]
        timelist = match_check(timelist)
        item = [ x.split('#')[1] for x in timelist]
        total_time,seconds= sum_time(item)
        while len(item) != 6:
            item.append('')
        item.insert(0, uid)
        item.append(total_time)
        item.append(seconds)
        res.append(item)

    csv_utf = '%s/report/%s.csv'%(dir_prefix,yesterday)
    df = pd.DataFrame(res,columns = ['user','in1','out1','in2','out2','in3','out3','sum_time','seconds'])
    df.to_csv(csv_utf, encoding='utf_8_sig',columns = ['user','in1','out1','in2','out2','in3','out3','sum_time'], index = False)
    return df

def top_last(df):

    top3_df = df.sort_values(by='seconds',ascending=False)
    top3 = []
    for uid in top3_df[:3]['user']:
        top3.append(uid)

    unfinish_df = df[df['seconds']<21600]
    unfinish = []
    for uid in unfinish_df['user']:
        unfinish.append(uid)
    return top3, unfinish

def message(top3,unfinish,kv,yesterday):
    msg = "%s Daily Check Info\n"%yesterday
    msg += "Top3: %s,%s,%s\n"%(top3[0],top3[1],top3[2])
    msg += "Not reached:\n"
    for uid in unfinish:
        txt = str(kv[uid])
        for split in SIMP:
            txt = txt.replace(split,'')
        txt = txt.replace(',',' ')
        msg += "%s %s\n"%(uid,txt)
    return msg

def data_process(dir_prefix):

    yesterday = str(getYesterday())
    kv = init_dict(yesterday,dir_prefix)
    dataframe = save_csv(kv,yesterday,dir_prefix)
    top, last = top_last(dataframe)
    msg = message(top,last,kv,yesterday)
    return msg

if __name__ == '__main__':

    dir_prefix="/home/qlteng/qlteng_data/daily_check"
    msg = data_process(dir_prefix)
    print msg
