ps -e -o 'pid,comm,args,rsz,user'|grep daily_check|grep python2.7|awk '{print $1}'|xargs kill -9
