#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！

import hashlib as hasher
import datetime as date
from random import randint
import json
import rsa_sign


import pg8000
import ast

conn = pg8000.connect(host='10.1.1.1', user='qytangdbuser', password='Cisc0123', database='qytangdb')
cursor = conn.cursor()
#cursor.execute("drop table qytcoin_chain") 
cursor.execute("select transaction_data from qytcoin_chain where index = 1") 
yourresults = cursor.fetchall()

jiaoyi_data = json.loads(yourresults[0][0])

print(jiaoyi_data)
#print(type(json.loads(jiaoyi_data)[0][0]))
#dst_trans = json.loads(jiaoyi_data)[0][4].replace("'",'"')
#print(type(json.loads(dst_trans)))
#print(json.loads(dst_trans)[0])
#print(type(jiaoyi_data))
#print(type(jiaoyi_data[]))



