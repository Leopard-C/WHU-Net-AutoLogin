
# Github: Leopard-C/WHU-Net-AutoLogin
# Email: leopard.c@outlook.com

import requests
from time import sleep
from urllib import parse

def login():
    url_test = 'http://www.lib.whu.edu.cn'    # WHU library website url
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    
    r = requests.get(url_test, headers=headers).text

    # If found the word 'confirmuser', you are logged in. Then exit the program
    if r.find('confirmuser') != -1:
        print('Login successfully!')
        exit(0)
    
    # If not logged in.
    # Extract the query parameter of the return valur r.
    query = (r.split('?')[-1]).split('\'')[0]

    url_auth = 'http://172.19.1.9:8080/eportal/InterFace.do?method=login'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    formData = {
        "userId": "xxxxxx",
        "password": "xxxxxxx",
        "service": "Internet",
        "queryString": query
    }
    formDataEncoeded = parse.urlencode(formData)

    r = requests.post(url_auth, headers=headers, data=formDataEncoeded).text
    if r.find('success') != -1:
        print('Login successfully!')
        exit(0)
    

if __name__ == "__main__":
    count = 0
    while True:
        login();    # Once loggeg in, the program exit.
        sleep(3)
        count = count + 1
        if count > 20:
            print('Login error!')
            exit(1)
