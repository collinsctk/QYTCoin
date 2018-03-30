#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！

# 导入cryptography库的相关模块和函数
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import base64

#为了传输，把数字签名（纯二进制）转换为Base64字符串
def sig_b64(sig):
    sig_b4code = base64.b64encode(sig)

    str_sig_b4code = str(sig_b4code)

    str_sig_b4code = str(sig_b4code)[2:-1]

    return str_sig_b4code

#把Base64字符串，转换回数字签名（纯二进制）
def b64_sig(b64):
    b4code_back = bytes(b64,'utf8')

    signature = base64.b64decode(b4code_back)

    return signature

#数字签名
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
        sign_string,
        padding.PKCS1v15(),
        hashes.SHA256())

    # 返回BASE64转码后的数字签名
    return sig_b64(signature)


def verify(sign_string, b64_signature, public_key_file_name):

    # 从PEM文件中读取公钥数据
    key_file = open(public_key_file_name, 'rb')
    key_data = key_file.read()
    key_file.close()

    # 从PEM文件数据中加载公钥
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
            b64_sig(b64_signature),
            sign_string,
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

def verify_str(sign_string, b64_signature, public_key_str):
    public_key_str = public_key_str.replace('\\n','\n')
    public_key = serialization.load_pem_public_key(
        bytes(public_key_str,'utf8'),
        backend=default_backend()
    )

    # 验证结果，默认为False
    verify_ok = False

    try:
        # 使用公钥对签名数据进行验证
        # 指定填充方式为PKCS1v15
        # 指定hash方式为sha256
        public_key.verify(
            b64_sig(b64_signature),
            sign_string,
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
    # 指定签名字符串
    sign_string = b'welcome to qytang'

    # 指定签名的私钥
    private_key_file = r'Key.pem'

    # 指定验证签名的公钥
    #public_key_file = r'Key_pub.pem'

    # 签名并返回签名结果
    signature = sign(sign_string, private_key_file)

    #打印数字签名
    #print(signature)

    import pg8000

    conn = pg8000.connect(host='10.1.1.1', user='qytangdbuser', password='Cisc0123', database='qytangdb')
    cursor = conn.cursor()   
    cursor.execute("select pub_key from qytcoin_public_key where id = 'qyt001'")
    yourresults = cursor.fetchall() 
    #print(yourresults[0][0])
    #public_key_string = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0ne0xy3j4tl2MWAw4dP0\n2UiNUUMhWmibHXNiUqwoLMNNo4oiRdup14Q7Zq7FEWArFB0buVjKsz7evbYO/vl6\n85pdijE32VIuA7XoS0eglu7au08amgzlGiY0X4Gp0oWGuCYlmZoRujWoDj/j9+A+\nwrBM/I8OoEHGiyAT6SqFdm2/HbE2lImen0g97+049+msi5XZXFdykdX5H6Yb9BuQ\nCxZdB0/U9hRlaaSZbPT3V65+mjDMwMjrZ4ndMGp9/Pu80En1K29UHHhlMW677PBz\nTiwEJ+s6ju3qUVPQqQMc2/8dTnsmQiebqKX1Q5fEtgavgZptOV196bjK6PyKcgWn\n3wIDAQAB\n-----END PUBLIC KEY-----\n"
    #print(public_key_string)
    #print(type(yourresults[0][0]))
    public_key_string = yourresults[0][0]
    print(signature)
    print(yourresults[0][0])
    verify_ok = verify_str(sign_string, signature, public_key_string)
    #verify_ok = verify_str(sign_string, signature, yourresults[0][0])
    if verify_ok:
        print('verify ok!')
    else:
        print('verify fail!')