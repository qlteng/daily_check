#!/bin/bash
dir=`pwd`
today=`date -d today +"%Y-%m-%d"`
/usr/bin/python2.7 ${dir}/src/daily_recorder.py --dir ${dir}>>${dir}/log/daily_check.log 2>&1 &
