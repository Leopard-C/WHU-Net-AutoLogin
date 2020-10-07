import requests
import sys
import json
import filecmp
import socket
import time
import datetime
import smtplib
from urllib import parse
from urllib import request
from email.mime.text import MIMEText 


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1",80))
        ipaddr=s.getsockname()[0]
        s.close()
        return ipaddr
    except:
        return ''


def check_network():
    try:
        html = requests.get("http://www.baidu.com", timeout=2).text
        return html.find('STATUS OK') > 0
    except:
        return False


# send email of this this host's ip
def send_ip_to_me(ipaddr):
    smtp_server = 'smtp.qq.com'
    from_add = 'xxxxxxx@qq.com'             ## <-------
    from_pwd = 'auth_code(not password!)'   ## <-------
    to_add = ['xxxxxx@qq.com']              ## <-------

    msg = MIMEText(ipaddr,'plain','utf-8')
    msg['From'] = from_add
    msg['To'] = to_add[0]
    msg['Subject'] = 'Subject'              ## <-------
    
    try:
        server = smtplib.SMTP_SSL(smtp_server,465)
        server.login(from_add,from_pwd)
        server.sendmail(from_add,to_add,msg.as_string())
        server.quit()
    except smtplin.SMTPException as e:
        print('error',e)


# login WHU Network
def do_login():
    url = "http://172.19.1.9:8080/eportal/InterFace.do?"
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }
    params = {
        'method': 'login',
        'service': 'Internet',
        'userId': 'xxxxxxxxx',      ## <-------
        'password': 'yyyyyy',       ## <-------
        'queryString': 'zzzzzz',    ## <-------
        'operatorUserId': '',
        'operatorPwd': '',
        'validcode': '',
        'passwordEncrypt': 'false',
    }

    for k,v in params.items():
        url += '%s=%s&' % (k, parse.quote(v))
    url = url[:-1]
    
    response = requests.post(url, headers=headers)
    data = json.loads(response.text)

    if 'result' in data and data['result'] == 'success':
            return True
    else:
        return False


# get formated time string
def now():
    return datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')


# main function
def main():
    enableSendEmail    = False  # send email of this host's ip to me(or someone else)
    enableLoop         = False  # check network constantly
    loopInterval       = 10     # 10 seconds
    lastIp = ''
    
    while True:
        # 1. Check network
        if check_network():
            currentIp = get_ip_address()
            print(now(), 'Network is OK. Current IP:', currentIp)
            if enableSendEmail:
                if currentIp != lastIp:
                    send_ip_to_me(currentIp)
                    lastIp = currentIp
        else:
            # 2. network is not connected -> do_login
            print(now(), 'Login...')
            success = False
            for i in range(1, 10):
                if do_login():
                    success = True
                    break
                else:
                    print(now(), "Login failed, retry:", i)
                    time.sleep(1)
                
            # 3. send email ?
            if success:
                print(now(), 'Login successfully')
                currentIp = get_ip_address()
                print(now(), 'Current IP:', currentIp)
                if enableSendEmail:
                    if currentIp != lastIp:
                        send_ip_to_me(currentIp)
                        lastIp = currentIp
            else:
                print(now(), 'Login failed for 10 times!')  
            
        # loop
        if enableLoop:
            time.sleep(loopInterval)
        else:
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(now(), 'exit')
