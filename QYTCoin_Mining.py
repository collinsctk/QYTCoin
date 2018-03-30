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
from QYTCoin_Class import *

#初始化数据库，创建表qytcoin_chain
import pg8000

conn = pg8000.connect(host='10.1.1.1', user='qytangdbuser', password='Cisc0123', database='qytangdb')
cursor = conn.cursor()
cursor.execute("drop table qytcoin_chain") 
cursor.execute("CREATE TABLE qytcoin_chain (index int,chain_datetime timestamp,previous_hash varchar(1000),transaction_data varchar(9999),transaction_data_id int,secure_code varchar(60),hash varchar(1000))") 
conn.commit()

#创世区块
def create_genesis_block():
    #创世区块创建的时间
    genesis_block_datetime = date.datetime.now()
    #把创世区块插入数据库，除了时间都为空
    conn = pg8000.connect(host='10.1.1.1', user='qytangdbuser', password='Cisc0123', database='qytangdb')
    cursor = conn.cursor()
    sql_full_cmd = "insert into qytcoin_chain values (0, '"+ str(genesis_block_datetime)+"', '', '', 0, '', '')"
    cursor.execute(sql_full_cmd) 
    conn.commit()
    #返回创世区块
    return Block(0, genesis_block_datetime, "0", {}, 0)

#创建后续区块的函数
def next_block(last_block):
    #在上一个区块唯一ID基础上加1
    this_index = last_block.index + 1
    #区块产生时间
    this_timestamp = date.datetime.now()

    #由于暂时只有一个矿工，所以每创建一个新的Block就给唯一矿工qyt001发12.5的奖金
    conn = pg8000.connect(host='10.1.1.1', user='qytangdbuser', password='Cisc0123', database='qytangdb')
    cursor = conn.cursor()
    block_trans = Transaction(date.datetime.now(),"qyt001",[],[["qyt001",12.5]])
    sql_full_cmd = "insert into qytcoin_transaction_data (transcation_datetime,source,source_trans,destination,sig_b64) values " + block_trans.sqlcmd('Key.pem')
    #print(sql_full_cmd)
    cursor.execute(sql_full_cmd) 
    conn.commit()


    #连接数据库，得到自上一个区块最后一个交易ID之后的交易信息
    cursor.execute("select * from qytcoin_transaction_data where id > " + str(last_block.transaction_data_id))
    yourresults = cursor.fetchall()

    #创建空交易数据列表
    transaction_data = []

    #写入交易数据
    if yourresults:
        for i in yourresults:
            new_list = []
            new_list.append(i[0])
            #需要转化datetime类型数据到字符串，便于JSON序列化
            new_list.append(str(i[1]))
            new_list.extend(i[2:])
            transaction_data.append(new_list)
        #得到最后一个交易的交易ID
        transaction_data_id = transaction_data[-1][0]
    #如果没有交易，交易数据写入空列表，保持原来的交易ID
    else:
        transaction_data = []
        transaction_data_id = last_block.transaction_data_id

    #取得上一个区块的HASH值
    previous_hash = last_block.hash

    #返回新区块
    return Block(this_index, this_timestamp, previous_hash, transaction_data,transaction_data_id)

#产生创世区块
previous_block = create_genesis_block()

#开始挖矿
while True:
    #产生下一个区块
    block_to_add = next_block(previous_block)

    #打印区块信息
    print("="*50)
    print("区块 #{} 已经被加入区块链!".format(block_to_add.index))

    print("上一个区块HASH值: {}".format(block_to_add.previous_hash))

    print("当前的区块HASH值: {}".format(block_to_add.hash))

    print("最后一笔记录交易的ID: {}".format(block_to_add.transaction_data_id))

    #区块信息写入数据库
    conn = pg8000.connect(host='10.1.1.1', user='qytangdbuser', password='Cisc0123', database='qytangdb')
    cursor = conn.cursor()
    sql_full_cmd = "insert into qytcoin_chain values " + block_to_add.sqlcmd()
    cursor.execute(sql_full_cmd) 
    conn.commit()

    #新区块会成为下一个块的前一个区块
    previous_block = block_to_add
