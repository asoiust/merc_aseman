# -*- coding: utf-8 -*-
'''
import requests
from bs4 import BeautifulSoup
def kos(my_str):
    res = my_str.split(",")
    result = "".join(res)
    return float(result)
request = requests.get('http://www.johnlewis.com/john-lewis-hampstead-leather-corner-sofa-unit/p1959376')
content = request.content
soup = BeautifulSoup(content, "html.parser")
element = soup.find("span", {"itemprop": "price", "class": "now-price"})
string_price = element.text.strip()[1:]
print kir(string_price)
'''
'''
import requests
def kos(my_str):
    res = my_str.split(",")
    result = "".join(res)
    return float(result)

from bs4 import BeautifulSoup
def kir(my_list):
    for item in my_list:
        yield kos(item.text)
request = requests.get('http://rayansaba.com/newshop6/category/cpus--processors--intel-/')
content = request.content
soup = BeautifulSoup(content, "html.parser")

element = soup.find_all("span",{"class":"price nowrap","itemprop":"price"},True)
for item in kos(element):
    print item
#print kir(string_price)
'''




'''
import requests
from bs4 import BeautifulSoup
def texter(mylist, name):
    j=0
    result = []
    for item in mylist:
        result.append((float("".join(("".join(item.text[:-6].split(" "))).split(","))),str(name[j].text)))

        j +=1
    return result
request = requests.get('http://rayansaba.com/newshop6/category/cpus--processors--intel-/')
content = request.content
soup = BeautifulSoup(content, "html.parser")
element = soup.find_all("span",{"class":"price nowrap","itemprop":"price"},True)
name = soup.find_all("h5",{"itemprop":"name"},True)
print  texter(element , name)
'''
'''
import requests
from bs4 import BeautifulSoup
def texter(rank, team, play, score):
    result = []
    for i in range(len(rank)):
        result.append((rank[i].text, team[i].text, play[i].text, score[i].text))
    return result


request = requests.get('http://www.varzesh3.com/')
content = request.content
soup = BeautifulSoup(content, "html.parser")
rank = soup.find_all("li",{"class":"rank"},True)
teamname = soup.find_all("li",{"class":"teamname"},True)
score = soup.find_all("li",{"class":"score"},True)
play = soup.find_all("li",{"class":"play"},True)
print texter(rank, teamname, play, score)
'''

import threading
import requests
from bs4 import BeautifulSoup

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        pass


request = requests.get('http://store.steampowered.com/app/364360/?snr=1_7_7_230_150_1')
content = request.content
soup = BeautifulSoup(content, "lxml")
name = soup.find_all("div",{"class":"apphub_AppName"},True)
tmp = u''
print (name[0].text.encode("utf-8"))