#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import base64

def sign(sign_string, private_key_file_name):
    """
    1.产生私钥
    openssl genrsa -out Key.pem -f4 2048
    2.产生公钥
    openssl rsa -in Key.pem -pubout -out Key_pub.pem
    """
    # 从PEM文件中读取私钥数据
    key_file = open(private_key_file_name, 'rb')
    key_data = key_file.read()
    key_file.close()

    # 从PEM文件数据中加载私钥
    private_key = serialization.load_pem_private_key(
        key_data,
        password=None,
        backend=default_backend()
    )

    # 使用私钥对数据进行签名
    # 指定填充方式为PKCS1v15
    # 指定hash方式为sha256
    signature = private_key.sign(
        bytes(sign_string,'utf8'),
        padding.PKCS1v15(),
        hashes.SHA256())

    # 返回BASE64转码后的数字签名
    return signature

def verify(sign_string, signature, public_key_file_name):

    # 从PEM文件中读取公钥数据
    key_file = open(public_key_file_name, 'rb')
    key_data = key_file.read()
    key_file.close()

    public_key = serialization.load_pem_public_key(
        key_data,
        backend=default_backend()
    )

    # 验证结果，默认为False
    verify_ok = False

    try:
        # 使用公钥对签名数据进行验证
        # 指定填充方式为PKCS1v15
        # 指定hash方式为sha256
        public_key.verify(
            signature,
            bytes(sign_string,'utf8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    # 签名验证失败会触发名为InvalidSignature的exception
    except InvalidSignature:
        # 打印失败消息
        print('invalid signature!')
    else:
        # 验证通过，设置True
        verify_ok = True

    # 返回验证结果
    return verify_ok

if __name__ == '__main__':
	import sys
	print('='*30,end='')
	print('计算数字签名',end='')
	print('='*30)
	print('数字签名结果如下:')
	[print('%02x' % x, end='') for x in sign(sys.argv[1], 'Key.pem')]
	print()
	signature = sign(sys.argv[1], 'Key.pem')

	print('='*30,end='')
	print('校验数字签名',end='')
	print('='*30)
	if verify(sys.argv[1], signature, 'Key_pub.pem'):
		print('数字签名校验成功！')
	else:
		print('数字签名校验失败！')


