#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！
import base64

def key_b64(file):

    key_file = open(file, 'rb')
    key_data = key_file.read()
    key_file.close()

    key_b4code = base64.b64encode(key_data)

    str_key_b4code = str(key_b4code)

    str_key_b4code = str(str_key_b4code)[2:-1]

    return str_key_b4code

if __name__ == '__main__':
	print(key_b64('Key.pem'))
