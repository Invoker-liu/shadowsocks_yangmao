#!/usr/bin/env python
# encoding=utf-8
import requests,random,json,time,re
from pyquery import PyQuery
from config import *
class email:
    def __init__(self):
        self.mail_addr = self.__madeMailName()
        self.session = requests.session()
        self.getCookie()  #得到本次的cookie
        mail = self.mail_addr
        self.mail_addr_url = mail.replace('@','(a)').replace('.','-_-')   #当前邮箱获取邮件的URL
        self.time = 0
        self.get_email()
    def getMailAddr(self):
        return self.mail_addr
    def __madeMailName(self):  #生成随机邮箱地址
        user_s = random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',random.randint(4,9))
        user = ''.join(user_s)
        host = config["mail_host"][random.randint(0,2)]
        mail_addr = user+"@"+host
        return mail_addr
    def getmail(self):    #检查邮件
        t = time.time()
        post_data = {"mail":self.mail_addr,"time":self.time,'-':int(round(t * 1000))}
        print(post_data)
        res = requests.post(config["getmail_url"],post_data)
        result = json.loads(res.text)
        print(result)
        if result["success"] == "true":
            self.time = result['time']
            if len(result['mail'])>0:
                return result["mail"][len(result['mail'])-1][4]   #返回邮件eml文件名
            else:
                return False
    def getMailContent(self,eml):            #获取邮件中的验证码
       
        header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'Upgrade-Insecure-Requests':'1',
                'Pragma': 'no-cache',
                'Host': 'bccto.me',
                'Cache-Control': 'no-cache',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                }
        self.session.headers.update(header)
        header["Cookie"] = self.cookie
        url = config["mail_content_url"]+self.mail_addr_url+"/"+eml
        print("邮件地址：",url)
        self.session.headers.update(header)  #更新cookie
        res = self.session.get(url.split('\n')[0])
        doc = PyQuery(res.text)
        str = doc.find("body").text()
        print(str)
        verify = re.findall(r"\[(.+?)\]",str)[0].strip()
        return verify

    def getCookie(self):
        self.session.headers.update({'User-Agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"})
        head = self.session.get("https://bccto.me/")
        self.cookie = 'UM_distinctid=16c999e56ae3c4-0d71057333df0a-3f385804-100200-16c999e56af404; CNZZDATA3645431=cnzz_eid%3D1577743675-1565943539-%26ntime%3D1565943539;mail="'+self.session.cookies.get("mail")+'";pgv_pvi=9883091968; pgv_si=s8566673408'
    def get_email(self):   #获得10分钟邮箱
        post_data = {"mail": self.mail_addr}
        header={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '24',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'pgv_pvi=5395792896; UM_distinctid=169945da30077-004c407c78306-5d1f3b1c-15f900-169945da301507; pgv_si=s7441818624; CNZZDATA3645431=cnzz_eid%3D187048399-1552967396-https%253A%252F%252Fbccto.me%252F%26ntime%3D1565853022; mail="2|1:0|10:1565855441|4:mail|40:Mzl0OHZ0MnNAYmNjdG8ubWV8MTU2NTg1NTQ0MQ==|44c7bcefa4f4a6c2b0fcb9da6bfd17ceaa3ff698e0b5ea96684d056042a0eace"; time="2|1:0|10:1565855441|4:time|16:MTU2NTg1NTQ0MQ==|d6140e57c92e116313744f4a8bb104255f3507e40798f01bb00867762afe2e75"',
        'Host': 'bccto.me',
        'Origin': 'https://bccto.me',
        'Pragma': 'no-cache',
        'Referer': 'https://bccto.me/',
        }
        res =  self.session.post(config["apply_url"],post_data,headers=header)
        if res:
            result = json.loads(res.text)
            print(result)
            if result["success"] == "true":
                return True
            else:
                return False



