#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！

from flask import Flask

from flask import request

from rsa_sign import b64_sig,verify_str

from datetime import datetime

from dateutil import parser

import json

from QYTCoin_Class import *

#初始化数据库
import pg8000

conn = pg8000.connect(host='10.1.1.1', user='qytangdbuser', password='Cisc0123', database='qytangdb')
cursor = conn.cursor()
cursor.execute("drop table qytcoin_transaction_data") 
cursor.execute("CREATE TABLE qytcoin_transaction_data (id SERIAL,transcation_datetime varchar(60),source varchar(60),source_trans varchar(9999),destination varchar(99999),sig_b64 varchar(1000));") 
conn.commit()

node = Flask(__name__)

@node.route('/qytcoin_transaction', methods=['POST'])

def transaction():

  if request.method == 'POST':

    # 获取POST请求中的数据

    new_qytcoin_transaction = request.get_json()

    # 获取POST 数据中的JSON数据

    #打印交易信息

    #请求类型为1表示，初次提交
    if new_qytcoin_transaction['request_type'] == '1':
    	print("="*50)
    	print("收到一笔乾颐通宝的交易")
    	print("转账发起账号: {}".format(new_qytcoin_transaction['transaction_src']))
    	print("转账接受账号: {}".format(new_qytcoin_transaction['transaction_dst']))
    	print("乾颐通宝数量: {}".format(new_qytcoin_transaction['qytcoin_count']))
    	print("交易时间:     {}".format(new_qytcoin_transaction['datetime']))

    	sign_data = bytes((new_qytcoin_transaction['transaction_src'] + \
                	new_qytcoin_transaction['transaction_dst'] + \
                	new_qytcoin_transaction['qytcoin_count'] + \
                	new_qytcoin_transaction['request_type'] + \
                	new_qytcoin_transaction['datetime']),'utf8')
    	#提取提交交易账号的公钥，用于校验签名
    	conn = pg8000.connect(host='10.1.1.1', user='qytangdbuser', password='Cisc0123', database='qytangdb')
    	cursor = conn.cursor()
    	cursor.execute("select pub_key from qytcoin_public_key where id = '" + new_qytcoin_transaction['transaction_src'] + "'")
    	public_key = cursor.fetchall()[0][0]
    	#公钥验证签名
    	verify_ok = verify_str(sign_data, new_qytcoin_transaction['sig_b64'], public_key)
    	if verify_ok:
            print('签名校验成功！')
    	else:
            print('签名校验失败！')
            return "签名失败！！！\n"
    	#获取提交交易账户	
    	qytcoin_source = new_qytcoin_transaction['transaction_src']
    	#--------获取交易数据库中这个账户使用过的交易ID（可能有交易还未加入块，用于双重检查）------------
    	cursor.execute("select source,source_trans from qytcoin_transaction_data")
    	transactions_double_check = cursor.fetchall()
    	used_transaction_id_double_check = []
    	for i in transactions_double_check:
    		if i[0] == qytcoin_source:
    			json_string = i[1].replace("'",'"').replace('"[','[').replace(']"',']')
    			used_transaction_id_double_check.extend(json.loads(json_string))
    	#------------------------------------------------------------------------------------------------
    	#-----------获取区块链数据库中这个账户使用过的交易ID，和收到qytcoin的交易ID和金额----------------
    	cursor.execute("select transaction_data from qytcoin_chain")
    	transactions = cursor.fetchall()
    	receive_transaction = []
    	used_transaction_id = []

    	for i in transactions[1:]:

        	json_string = i[0].replace("'",'"').replace('"[','[').replace(']"',']')
        	for a in json.loads(json_string):
        		if a[2] == qytcoin_source:
        			used_transaction_id.extend(a[3])
        		for x in a[4]:
        			if x[0] == qytcoin_source:
        				receive_transaction.append([a[0],x[1]])
		#------------------------------------------------------------------------------------------------
    	#---------------------------------------计算得到可以使用的交易ID---------------------------------
    	active_transaction = receive_transaction[:]

    	for u in used_transaction_id:
        	for r in receive_transaction:
        		if r[0] == u:
        			active_transaction.pop(active_transaction.index(r))

    	#------------------------------------------------------------------------------------------------
    	#-------------------计算本次交易消耗的交易ID，并且返回给客户确认并且再签名-----------------------
    	active_transaction_qytcoin = 0
    	pre_use_transaction = []

    	for qytcoin in active_transaction:
    		#双重校验交易ID是否被使用
    		if qytcoin[0] in used_transaction_id_double_check:
    			continue

    		active_transaction_qytcoin = active_transaction_qytcoin + qytcoin[1]
    		pre_use_transaction.append(qytcoin[0])
    		#如果金额正好等于
    		if active_transaction_qytcoin == float(new_qytcoin_transaction['qytcoin_count']):
    			return_json = [new_qytcoin_transaction['datetime'],\
    				       	   new_qytcoin_transaction['transaction_src'],\
    				       	   pre_use_transaction,\
    				       	   [[new_qytcoin_transaction['transaction_dst'],new_qytcoin_transaction['qytcoin_count']]]
    				       	  ]

    			return json.dumps(return_json)
    		#如果金额大于
    		elif active_transaction_qytcoin > float(new_qytcoin_transaction['qytcoin_count']):
    			#print('大于')
    			#print(active_transaction_qytcoin,float(new_qytcoin_transaction['qytcoin_count']))
    			reback = active_transaction_qytcoin - float(new_qytcoin_transaction['qytcoin_count'])
    			#print(pre_use_transaction)
    			return_json = [new_qytcoin_transaction['datetime'],\
    				       	   new_qytcoin_transaction['transaction_src'],\
    				       	   pre_use_transaction,\
    				       	   [[new_qytcoin_transaction['transaction_dst'],new_qytcoin_transaction['qytcoin_count']],\
    				       	   	[new_qytcoin_transaction['transaction_src'],reback]
    				       	   ]
    				       	  ]

    			return json.dumps(return_json)
    	else:
    		print('金额不足')
    		return "金额不足！！！\n"
    	
    #请求类型为2表示，客户确认
    elif new_qytcoin_transaction['request_type'] == '2':
    	print("="*50)
    	print("收到一笔乾颐通宝的确认")
    	print("转账发起账号    : {}".format(new_qytcoin_transaction['transaction_src']))
    	print("转账接受者与金额: {}".format(new_qytcoin_transaction['transaction_dst']))
    	print("使用的交易ID    : {}".format(new_qytcoin_transaction['source_trans']))
    	print("交易时间        : {}".format(new_qytcoin_transaction['datetime']))

    	#提取提交交易账号的公钥，用于校验签名
    	final_tran = Transaction(parser.parse(new_qytcoin_transaction['datetime']), new_qytcoin_transaction['transaction_src'], new_qytcoin_transaction['source_trans'], new_qytcoin_transaction['transaction_dst'])    	
    	conn = pg8000.connect(host='10.1.1.1', user='qytangdbuser', password='Cisc0123', database='qytangdb')
    	cursor = conn.cursor()
    	cursor.execute("select pub_key from qytcoin_public_key where id = '" + new_qytcoin_transaction['transaction_src'] + "'")    	
    	public_key = cursor.fetchall()[0][0] 

    	#如果签名校验成功就写入交易数据库
    	if final_tran.verify_sig(new_qytcoin_transaction['sig_b64'],public_key):
    		print('签名校验成功！交易已经成功写入数据库！')
    		final_tran.signature = new_qytcoin_transaction['sig_b64']
    		conn = pg8000.connect(host='10.1.1.1', user='qytangdbuser', password='Cisc0123', database='qytangdb')
    		cursor = conn.cursor()
    		sql_full_cmd = "insert into qytcoin_transaction_data (transcation_datetime,source,source_trans,destination,sig_b64) values " + final_tran.sqlcmd_no_sig()
    		cursor.execute(sql_full_cmd) 
    		conn.commit()
    		return "交易已经成功接受，恭喜发财！！！\n"
    	else:
    		print('签名失败！')
    		return "签名失败！！！\n"

if __name__ == "__main__":
    node.run(host = '0.0.0.0')
