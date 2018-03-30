#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！


from HTTP_JSON_POST_Request_1 import http_post_json
from rsa_sign import sign
import datetime

private_key_file = r'Key.pem'

def post_transaction_data():
	transaction_data = {}
	transaction_data['transaction_src'] = input('请输入转账发起账号:')
	transaction_data['transaction_dst'] = input('请输入转账接受账号:')
	transaction_data['qytcoin_count'] = input('乾颐通宝数量      :')
	transaction_data['request_type'] = '1'
	transaction_data['datetime'] = str(datetime.datetime.now())
	sign_data = transaction_data['transaction_src'] + \
				transaction_data['transaction_dst'] + \
				transaction_data['qytcoin_count'] + \
				transaction_data['request_type'] + \
				transaction_data['datetime']
	bytes_sign_data = bytes(sign_data,'utf8')
	sig_b64 = sign(bytes_sign_data, private_key_file)
	transaction_data['sig_b64'] = sig_b64

	http_post_json('10.1.1.1',transaction_data)


if __name__ == "__main__":
	post_transaction_data()
