#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！


from http.client import HTTPConnection
import json
from QYTCoin_Class import *
from dateutil import parser
from datetime import datetime

def http_post_json(ip,dict_data,port=5000):
	c = HTTPConnection(ip, port=port)

	#创建并写入HTTP头部数据
	headers = {}
	headers['Content-Type'] = 'application/json'

	#写入HTTP Body部分的JSON数据
	post_json_data = json.dumps(dict_data).encode('utf-8')

	#发起HTTP连接
	c.request('POST', '/qytcoin_transaction', body=post_json_data, headers=headers)

	#获取响应
	res = c.getresponse()

	#打印响应，由于有中文，所以注意使用utf-8解码
	responce_1 = res.read().decode('utf-8')
	try:
		result = json.loads(responce_1)
		print("+"*50)
		print("服務器需要再次确认您的交易")
		print("交易时间      :" + str(result[0]))
		print("交易源        :" + str(result[1]))
		print("使用之前交易ID:" + str(result[2]))
		print("接受者与金额  :" + str(result[3]))
		print("+"*50)
		choice_result = input('\n请确认您的交易[y|n]:')
		if choice_result == "y" or choice_result == "Y":
			#print(type(result[0]))
			#print(type(result[1]))
			#print(type(result[2]))
			#print(type(result[3]))
			new_trans = Transaction(parser.parse(result[0]), result[1], result[2], result[3])
			tran_sig_64 = new_trans.sig_b64('Key.pem')
			transaction_data = {}
			transaction_data['datetime'] = str(new_trans.timestamp)
			transaction_data['request_type'] = '2'
			transaction_data['transaction_src'] = new_trans.source
			transaction_data['transaction_dst'] = new_trans.destination
			transaction_data['source_trans'] = new_trans.source_trans
			transaction_data['sig_b64'] = tran_sig_64
			#print(transaction_data)
			post_json_data = json.dumps(transaction_data).encode('utf-8')
			c = HTTPConnection(ip, port=port)
			c.request('POST', '/qytcoin_transaction', body=post_json_data, headers=headers)
			res = c.getresponse()

			#打印响应，由于有中文，所以注意使用utf-8解码
			responce_2 = res.read().decode('utf-8')
			print(responce_2)

		elif choice_result == "n" or choice_result == "N":
			print("交易已经取消！")
		else:
			print("选择错误，请重新开始交易！")
	except json.decoder.JSONDecodeError:
		print(responce_1)

if __name__ == "__main__":
	json_data = {"from": "akjflw", "to":"fjlakdj", "amount": 3}
	http_post_json('10.1.1.1',json_data)
