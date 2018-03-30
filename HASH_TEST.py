#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！
import hashlib as hasher
from random import randint
import datetime as date
start_time = date.datetime.now()
timestamp = str(start_time)
hash_md5 = hasher.md5()
hash_md5.update(str(randint(0,10000)).encode("utf8"))
previous_hash = hash_md5.hexdigest()


while True:
	hash_md5_test = hasher.md5()
	random_num = randint(0,9999999999)
	hash_md5_test.update((timestamp+previous_hash+str(random_num)).encode("utf8"))
	hash_md5_test.hexdigest()
	if hash_md5_test.hexdigest()[0] == '0' \
	   and hash_md5_test.hexdigest()[1] == '0' \
	   and hash_md5_test.hexdigest()[2] == '0' \
	   and hash_md5_test.hexdigest()[3] == '0' \
	   and hash_md5_test.hexdigest()[4] == '0' \
	   and hash_md5_test.hexdigest()[5] == '0':
		time1 = date.datetime.now()
		print(random_num)
		print(hash_md5_test.hexdigest())
		print(time1 - start_time)
