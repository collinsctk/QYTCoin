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
from proofofwork import proofofwork

#字符串拼接产生SQL语句时，单引号要用两个单引号替代
def str_single_to_double_single(list_test):
    list_str = "["
    for i in list_test:
        list_str = list_str +  '[' + "''" + i[0] + "''" + ',' + str(i[1]) + ']' + ','
    list_str = list_str[0:-1] + ']'
    return list_str

#块的类
class Block:
    def __init__(self, index, timestamp, previous_hash, transaction_data,transaction_data_id):
        #区块唯一ID
        self.index = index
        #区块产生时间
        self.timestamp = timestamp
        #前一个区块HASH值
        self.previous_hash = previous_hash
        #本区块记录的交易数据
        self.transaction_data = transaction_data
        #本区块记录的交易数据的最后一个交易的唯一ID
        self.transaction_data_id = transaction_data_id

        #计算数学难题，得到安全码
        while True:
        	random_num = randint(0,9999999999)
        	hash_string = str(self.index) + str(self.timestamp) + self.previous_hash + json.dumps(self.transaction_data) + str(self.transaction_data_id) + str(random_num)
        	#16为0的个数要求
        	if proofofwork(hash_string,16):
        		self.nonceforproofwork = random_num
        		break
        #本区块的HASH值
        self.hash = self.hash_block()

    def hash_block(self):#计算区块的HASH值函数
        md5 = hasher.md5()

        md5.update((str(self.index) +

                   str(self.timestamp) +

                   str(self.transaction_data) +

                   str(self.nonceforproofwork) +

                   str(self.transaction_data_id) +

                   str(self.previous_hash)).encode("utf8"))

        return md5.hexdigest()
    #产生插入数据库的SQL语句
    def sqlcmd(self):
        inject_values = "(" + str(self.index) + \
                         ", '" + str(self.timestamp) + "'"\
                         ", '" + self.previous_hash + "'"\
                         ", '" + json.dumps(self.transaction_data).replace("'","''") + "'"\
                         ", " + str(self.transaction_data_id) + \
                         ", '" + str(self.nonceforproofwork) + "'"\
                         ", '" + str(self.hash) + "')"
        return inject_values

#交易的类
class Transaction:
    def __init__(self, timestamp, source, source_trans, destination):
        #区块产生时间
        self.timestamp = timestamp
        #前一个区块HASH值
        self.source = source
        #本区块记录的交易数据
        self.source_trans = source_trans
        #本区块记录的交易数据的最后一个交易的唯一ID
        self.destination = destination
        #数字签名，后续赋值
        self.signature = None

    #产生交易的base64数字签名，必须要有私钥
    def sig_b64(self,private_key):
        sig_string = str(self.timestamp) + \
                     str(self.source) + \
                     str(self.source_trans) + \
                     str(self.destination)
        self.signature = rsa_sign.sign(bytes(sig_string,'utf8'), private_key)
        return rsa_sign.sign(bytes(sig_string,'utf8'), private_key)
    #校验交易的数字签名，要有对应的公钥
    def verify_sig(self,signature,public_key):
        sig_string = str(self.timestamp) + \
                     str(self.source) + \
                     str(self.source_trans) + \
                     str(self.destination)
        verify_result = rsa_sign.verify_str(bytes(sig_string,'utf8'), signature, public_key)
        return verify_result
    #产生插入数据库的SQL语句，本地产生的交易，直接可以产生数字签名
    def sqlcmd(self,private_key):
        sig_b64_string = self.sig_b64(private_key)
        inject_values = "('" + str(self.timestamp) + "'," + "'" + str(self.source) + "',"\
                     + "'" + str(self.source_trans) + "',"\
                     + "'" + str_single_to_double_single(self.destination) + "',"\
                     + "'" + self.signature + "')"
        return inject_values
    #产生插入数据库的SQL语句，其他账号产生的交易，需要提取他们提供的数字签名
    def sqlcmd_no_sig(self):
        inject_values = "('" + str(self.timestamp) + "'," + "'" + str(self.source) + "',"\
                     + "'" + str(self.source_trans) + "',"\
                     + "'" + str_single_to_double_single(self.destination) + "',"\
                     + "'" + self.signature + "')"
        return inject_values