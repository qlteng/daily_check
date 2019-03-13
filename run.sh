#!/bin/bash
dir=`pwd`
today=`date -d today +"%Y-%m-%d"`
/usr/bin/python ${dir}/src/daily_recorder.py --dir ${dir} >${dir}/log/${today}.log 2>&1 &
