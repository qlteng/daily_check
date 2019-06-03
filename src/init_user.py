# coding: utf-8

class init_user:

    def __init__(self):

        self.userlist = ['滕千礼','蔡志波','王春燕','周存理','张兆哲','李永明','雷宗木','丁洁','Nomaan Khan','赵宇轩','魏昂','朱蓉蓉','闫东超','Shafiq Rai','张陈然','牛军锋','赵颖慧']
        self.sp = {'牛红峰':50,'ashil':50,'Muhammad':50,'Asif':50}

if __name__ == '__main__':

    user = init_user()
    userlist = user.userlist
    sp = user.sp
    for x in userlist:
        print x
    for k,v in sp.items():
        print k,v
