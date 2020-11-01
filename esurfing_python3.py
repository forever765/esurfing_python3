'''
作者：forever765
Github项目地址：https://github.com/forever765/esurfing_python3
1. 使用Python3重写
2. 标准化部分函数名
3. 增加生成随机mac地址
4. 增加自动获取本机IP地址
5. 使用requests替代urllib2
6. 优化认证流程，修改不合理死循环，整合无用函数，增强异常处理
感谢原作者提供的认证和保活算法, 原项目地址：https://github.com/mynuolr/GD-esurfingschoolclient-portal
'''

import time
import json
import random
import socket
import hashlib
import requests

def GetIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ipaddr = s.getsockname()[0]
        #ipaddr = "192.168.195.175"
    except:
        print(NowTime() + 'Get ip failed, please check your network setting, exit!')
        exit(444)
    else:
        return(ipaddr)

def GenFakeMAC():
    myhexdigits = []
    for x in range(6):
        a = random.randint(0,255)
        hex = '%02x' % a
        myhexdigits.append(hex)
    Fake_MAC = '-'.join(myhexdigits).upper()
    return Fake_MAC

def GetMD5(str):
    m = hashlib.md5()
    m.update(str.encode("utf-8"))
    return (m.hexdigest()).upper()

def GetTime():
    return int(time.time()*1000)

def GetVerifyCode():
    print(NowTime() + 'Starting get verify code...')
    timestr = str(GetTime())
    clientip = GetIP()
    print(NowTime() + 'IP Address: ' + clientip)
    C_rawdata = str(clientip + nasip + mac + timestr + md5_secret)
    md5str = GetMD5(C_rawdata)
    #print(NowTime() + "GetVerifyCode MD5加密结果：" + md5str)
    Curl = url + 'challenge'
    values = {
        "iswifi": "4060",
        "clientip": clientip,
        "nasip": nasip,
        "mac": mac,
        "timestamp": timestr,
        "authenticator": md5str,
        "username": user
    }
    PostData = json.dumps(values)
    header = {'User-agent': ua}
    try:
        Creq = requests.post(url=Curl, headers=header, data=PostData)
        RCode = json.loads(Creq.text)
    except Exception as e:
        print(NowTime() + 'Challenge Error: ' + e + ', response: ' + Creq.text)
        exit(444)
    else:
        #Check Get Challenge Result
        if float(RCode['rescode']) == 0:
            #Check Challenge Code Length
            if len(RCode['challenge']) == 4:
                print(NowTime() + 'Get verift code successfully! Challenge is: ' + RCode['challenge'])
                return RCode['challenge']
            else:
                print(NowTime() + 'Get verify code error: The challenge length is not equal to 4')
        else:
            print(NowTime() + 'Get verift code failed!',Creq.text)

def NowTime():
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    t1=time.strftime(ISOTIMEFORMAT, time.localtime( time.time() ) )
    str="[ "+t1+" ]\t"
    return str

def LoginHttpPost(token):
    print(NowTime() + 'Sending login request...')
    timestr= str (GetTime())
    L_rawdata= str(clientip + nasip + mac + timestr + token + md5_secret)
    md5str = GetMD5(L_rawdata)
    #print(NowTime() + "Login Http Post MD5加密结果：" + md5str)
    Lurl = url + 'login'
    values = {
        "username" : user,
        "password" : password,
        "clientip" : GetIP(),
        "nasip" : nasip,
        "mac" : mac,
        "timestamp" : timestr,
        "authenticator" : md5str,
        "verificationcode" : token,
        "iswifi" : wifi
    }
    PostData_Login = json.dumps(values)
    #print('%s Login参数：%s' % (NowTime(), str(values)))
    header = {'User-agent': ua}
    try:
        Lreq = requests.post(url=Lurl, headers=header, data=PostData_Login)
        Lresp = json.loads(Lreq.text)
        if Lresp['rescode'] == '0':
            print(NowTime() + 'Login successfully!')
        return Lreq.text
    except Exception as e:
        print(NowTime() + 'Login Error: ' + e + ', response: ' + Lreq.text)
        return "x"

def GoLogin():
    AuthCode = GetVerifyCode()
    LoginResult = LoginHttpPost(AuthCode)

def KeepAlive():
    timestr = str(GetTime())
    K_rawdata= str(clientip + nasip + mac + timestr + md5_secret)
    md5str = GetMD5(K_rawdata)
    #print(NowTime() + "KeepAlive MD5加密结果：" + md5str)
    Kurl = active+"username="+user+"&clientip="+clientip+"&nasip="+nasip+"&mac="+mac+"&timestamp="+timestr+"&authenticator="+md5str
    header = {'User-agent': ua}
    #print(NowTime() + "Send KeepAlive Request: "+url)
    try:
        KeepReq = requests.get(url=Kurl, headers=header)
        KeepResult = json.loads(KeepReq.text)
        return KeepResult['rescode']
    except Exception as e:
        print(NowTime() + e)
        return "x"

def Loop_KeepAlive(time_interval):
    while 1:
        KeepAliveResp = KeepAlive()
        if KeepAliveResp == '0':
            print(NowTime() + r'\口-口/ 续命成功，+1s')
            time.sleep(time_interval)
            continue
        elif(KeepAliveResp == "1"):
            GoLogin()
            continue

if __name__ == "__main__":
    nasip = "183.56.17.66"                    #net auth ip, GDHSXY using 183.56.17.66 
    user = "xxx"                     #username
    password = "xxx"                  #password
    clientip = GetIP()
    mac = GenFakeMAC()                        #Fake random mac address
    wifi = "1050"                             #GDHSXY 'iswifi' is 1050
    url = "http://125.88.59.131:10001/client/"
    active = "http://enet.10000.gd.cn:8001/hbservice/client/active?"
    md5_secret = "Eshore!@#"
    ua = 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)'          #seems not require
    testurl = "http://www.qq.com"
    time_interval = 3600                        #心跳包发送时间间隔, wifi≈3600s, 有线≈120s

    try:
        #test internet status
        rn = requests.get(url=testurl, timeout=10)
    except Exception as e:
        print(NowTime() + 'Check internet trigger error: ' + e)
    else:
        #if internet is normal, start keepalive, if not, go to login
        if rn.url == testurl:
            r = KeepAlive()
            if r == '0':
                print(NowTime() + r'\口-口/ 续命成功，+1s')
        else:
            GoLogin()
            time.sleep(90)
            Loop_KeepAlive(time_interval)
