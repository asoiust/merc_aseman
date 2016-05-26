# -*- coding: utf-8 -*-
import threading
import requests
from bs4 import BeautifulSoup
import MySQLdb

class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        pass


def link_extractor(my_html):
    result = []
    for item in my_html:
        result.append(str(item.get('href')))
    return result


def scrapper_first_layer(page):
    url = 'http://store.steampowered.com/search/results?sort_by=_ASC&tags=-1&category1=998&page=%s&snr=1_7_7_230_7' % (page,)
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "lxml")
    my_html = soup.find_all("a",{"class":"search_result_row ds_collapse_flag"},True)
    return link_extractor(my_html)


def go_in_link(url):
    request = requests.get(url)
    content  = request.content
    result = dict()
    result.update({'title':get_title(content),'os':system_req(content),'price':get_price(content)})
    return result

def get_title(content):
    soup = BeautifulSoup(content, "lxml")
    game_title = soup.find_all("div",{"class":"apphub_AppName"},True)
    return game_title[0].text.encode("utf-8").decode('utf-8')


def system_req(content):
    soup = BeautifulSoup(content, "lxml")
    os = soup.find_all("div",{"data-os":"win"},True)
    return os[0].text.encode("utf-8")

def get_price(content):
    soup = BeautifulSoup(content, "lxml")
    os = soup.find_all("div",{"data-os":"win"},True)
    return os[0].text.encode("utf-8")



print go_in_link(scrapper_first_layer('1')[0])
