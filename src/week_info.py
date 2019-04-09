# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 15:49:10 2019

@author: qlteng
"""

import datetime
import pandas as pd


USER = ['王春燕','田泽英','牛红峰','王丰','张兆哲','李永明','Asif','ashil','雷宗木','丁洁','Nomaan Khan','Muhammad','赵宇轩','魏昂','朱蓉蓉','闫东超','Shafiq Rai','张陈然','牛军锋','赵颖慧','蔡志波','周存理','滕千礼']

sp = {'滕千礼':48}
def acc_time(time_list):
    acc = datetime.timedelta()
    for x in time_list:
        if 'day' in x:
            x = x.split(' ')[-1]
        h,m = [int(x) for x in x.split(':')]
        acc += datetime.timedelta(hours = h, minutes = m)
    return acc

def get_date(num):

    today = datetime.datetime.today()
    oneday=datetime.timedelta(days=1)
    datelist = []
    for i in range(1,num+1):
        temp_date = today - oneday*i
        temp_date = str(datetime.datetime.strftime(temp_date,'%Y-%m-%d'))
        datelist.append(temp_date)

    return datelist

def init_dict():

    kv = {}

    for uid in USER:
        if uid not in kv.keys():
                kv[uid] = []
    return kv

def message_on_mon(top3,no_reach):
    msg = "Weekly Check Info\n\n"
    msg += "Top3: %s,%s,%s\n\n"%(top3[0],top3[1],top3[2])
    msg += "Not reach:\n\n"
    for uid,time in no_reach:
        msg += "%s: %sh\n"%(uid,time)
    msg += "Sorry to tell you that your work time is not enough last week,please work harder this week\n"
    for uid,time in no_reach:
        msg += "@%s "%uid
    return msg

def message_on_sat(no_reach):
    msg = "Workday Check Attention\n\n"

    msg += "Your work time not reach 40 hours,please keep working on the weekend\n\n"
    for uid,time in no_reach:
        msg += "%s: %sh\n"%(uid,time)
    for uid,time in no_reach:
        msg += "@%s "%uid
    return msg

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


def sum_time(days,dir_prefix = "",to_csv=True):

    yesterday = str(datetime.datetime.strftime((datetime.datetime.today() - datetime.timedelta(days=1)),'%Y-%m-%d'))
    no_reach = []
    week_csv = "%s/report/%s_week.csv"%(dir_prefix,yesterday)

    date = get_date(days)
    kv = init_dict()

    for x in date:
        csv = "%s/report/%s.csv" % (dir_prefix, x)
        temp_df = pd.read_csv(csv,encoding = 'utf_8_sig')
        for index, row in temp_df.iterrows():
            user = row['user'].encode('utf_8')
            time = row['sum_time'].encode('utf_8')
            if user not in kv.keys():
                kv[user] = [time]
            else:
                kv[user].append(time)
    res = []
    for k in kv.keys():
        kv[k] = round(acc_time(kv[k]).total_seconds()/3600,1)

        item = [k,kv[k]]
        res.append(item)
        if k in sp.keys():
            if kv[k]<sp[k]:
                no_reach.append([k,kv[k]])
        elif kv[k]<40:
            no_reach.append([k,kv[k]])

    df = pd.DataFrame(res,columns = ['user','sum_time(h)'])
    if to_csv:
        df.to_csv(week_csv, encoding='utf_8_sig',columns = ['user','sum_time(h)'], index = False)

    return df,no_reach

if __name__ == '__main__':

    dir_prefix="/home/cywang/daily_check"
    print send_on_sat(dir_prefix)
    print send_on_mon(dir_prefix)

#print send_on_sat()
#print send_on_mon(dir_prefix = "")
#    kv = temp_df.apply(lambda row: parse_df(str(row['user'].encode('utf-8')), str(row['sum_time'].encode('utf-8')), kv), axis=1)


#sched = BlockingScheduler()
#sched.add_job(p, 'cron',day_of_week='sun', hour=15, minute = 55)
#sched.add_job(p, 'cron',day_of_week='tue-fri', hour=15, minute = 55)
#sched.start()
