# coding: utf-8

class init_user:

    def __init__(self):

        self.userlist = ['田泽英','牛红峰','张兆哲','李永明','Asif','ashil','雷宗木','丁洁','Nomaan Khan','Muhammad','赵宇轩','魏昂','朱蓉蓉','闫东超','Shafiq Rai','张陈然','牛军锋','赵颖慧']
        self.sp = {}

if __name__ == '__main__':

    user = init_user()
    userlist = user.userlist
    sp = user.sp
    for x in userlist:
        print x
    for k,v in sp.items():
        print k,v
