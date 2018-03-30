#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！
import hashlib
import datetime

def proofofwork(string,zero_len):
	m = hashlib.md5()
	m.update(bytes(string,'utf8'))
	bin_result = bin(int('0x' + m.hexdigest(),16))[2:]
	#print(len(bin_result))
	if (128 - zero_len) > len(bin_result):
		return string
	else:
		return

def proofofwork_show(string,zero_len):
	m = hashlib.md5()
	m.update(bytes(string,'utf8'))
	bin_result = bin(int('0x' + m.hexdigest(),16))[2:]
	if (128 - zero_len) > len(bin_result):
		need_add_0 = 128 - len(bin_result)
		hash_128 = '0'*need_add_0 + bin_result
		return hash_128,need_add_0
	else:
		return
if __name__ == '__main__':
	import sys
	import random
	import datetime
	need_0 = int(sys.argv[1])
	while True:
		hash_128 = proofofwork_show(str(random.randint(0,99999999999)),need_0)
		if hash_128:
			print('-'*30+'HASH Zero Length:' + str(hash_128[1]) +'-'*30)
			print(hash_128[0])
			