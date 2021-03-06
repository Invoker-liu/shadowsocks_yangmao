import requests,json,threading,random
from get_free_email import *
from getVpnAccount import *
from config import *
from requests import exceptions

class zoomEy:
    def __init__(self):
    #     self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6Ijk1MTI1NDIyOUBxcS5jb20iLCJpYXQiOjE1ODc3NDI3MjAsIm5iZiI6MTU4Nzc0MjcyMCwiZXhwIjoxNTg3Nzg1OTIwfQ.MQwRDGBlR1xR8X30rvURs6wUxSyCK8ve5LYnkRM3fRU"
        self.hosts = []
    def getAccessToken(self):
     #    loginUrl = "https://api.zoomeye.org/user/login"
     #    data = {
     # n   "username": config['zoomeyAccount'],
     #    "password":config['zoomeyPassword']
     #    }
     #    res = requests.post(loginUrl,json.dumps(data))
     #    print(res.text)
     #    accessToken = json.loads(res.text)['access_token']
        self.token = config["API_KEY"][random.randint(0,len(config["API_KEY"])-1)]

    
    def search(self,q,start,end):
        if self.token == "":
            return false
        header = {
            "API-KEY":self.token
        }
        searchUrl = "https://api.zoomeye.org/host/search"
        for page in range(start,end):
            search = {
                "query" : q,
                "page":page
            }
            res = requests.get(searchUrl,params = search, headers=header)
            zoomRes = json.loads(res.text)
            if not 'matches' in zoomRes:
                break
            res = zoomRes['matches']
            total = zoomRes['total']
            hosts = []
            for i in res:
                hosts.append("%s://%s:%s"%(i['portinfo']['service'], i['ip'], i['portinfo']['port']))
            self.hosts.extend(hosts)
            print("第%d页一共找到%d个节点,总共有:%d,可用:%d"%(page,len(hosts),total,zoomRes['available']))
        
    def screenStation(self, email, account):     #节点初筛
        print("开始初筛节点,共有%d个待筛节点"%(len(self.hosts)))
        if len(self.hosts) > 0:
            i = 0
            while i < len(self.hosts):
                account = vpnAccount(email.getMailAddr(),self.hosts[i])  #准备开始申请账号
                try:
                    requests.get(self.hosts[i],timeout=10,verify=False)
                except:     #超时了
                    print("[%s]连接超时"%(self.hosts[i]))
                    self.hosts.pop(i)
                    i -= 1
                else:
                    if not account.sendCode(): #不能发验证码即没通过初筛
                        print("[%s]不太行"%(self.hosts[i]))
                        self.hosts.pop(i)
                        i -= 1
                i+=1

    def save(self):
        if len(self.hosts) > 0:
            f = open('hosts/hosts.json','a+')
            hosts = json.dumps(f.read())
            if len(hosts):
                hosts = list(set(hosts).union(set(self.hosts)))
            else:
                hosts = []
            f.write(json.dumps(hosts))
            f.close()
            return True
        else:
            return False
def getStations(start,end):

    z = zoomEy()
    z.getAccessToken()
    z.search('shadowsocks-manager',start,end)
    
    account = vpnAccount(email.getMailAddr())  #准备开始申请账号
    z.screenStation(email,account)  #预先把没用的链接去了
    z.save()
email = email()  #先生成一个邮箱
x=1
while x<=40:
    start = x
    end = x+2
    t = threading.Thread(target=getStations, args=(start,end)) 
    t.start()
    # t.join()
    x += 2


