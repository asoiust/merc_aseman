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


def make_list(my_list):
    result = []
    for item in my_list:
        result.append(item.text)
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
    result.update({'title':get_title(content),'sys':system_req(content),'price':get_price(content),
                   'details':get_details(content), 'description':get_description(content),
                   'tags':get_tags(content),'overall':get_overall(content),'date':get_rdate(content)})

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
    price = soup.find_all("div",{"class":"game_purchase_price"},True)
    return price[0].text.encode("utf-8")


def get_details(content):
    soup = BeautifulSoup(content, "lxml")
    details = soup.find_all("div",{"class":"details_block"},True)
    return details[0].text.encode("utf-8")


def get_description(content):
    soup = BeautifulSoup(content, "lxml")
    description = soup.find_all("div",{"class":"game_description_snippet"},True)
    return description[0].text.encode("utf-8")


def get_overall(content):
    soup = BeautifulSoup(content, "lxml")
    overall = soup.find_all("span",{"class":"game_review_summary positive"},True)
    return overall[0].text.encode("utf-8")


def get_tags(content):
    soup = BeautifulSoup(content, "lxml")
    tags = soup.find_all("a",{"class":"app_tag"},True)
    return make_list(tags)


def get_rdate(content):
    soup = BeautifulSoup(content, "lxml")
    rdate = soup.find_all("span",{"class":"date"},True)
    return rdate[0].text.encode("utf-8")


def get_discount(content):
    soup = BeautifulSoup(content, "lxml")
    discount = soup.find_all("span",{"class":"date"},True)
    return discount[0].text.encode("utf-8")

#print go_in_link(scrapper_first_layer('1')[0])
print go_in_link('http://store.steampowered.com/app/292030/?snr=1_7_7_230_150_1')
#div.discount_pct

