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
        result.append(item.text.replace('\t', '').replace('\n', '').replace('\r', ''))
    return result


def string_corrector(string):
    return string.replace('\t', '').replace('\n', '').replace('\r', '')


def scrapper_first_layer(page):
    url = 'http://store.steampowered.com/search/results?sort_by=_ASC&tags=-1&category1=998&page=%s&snr=1_7_7_230_7' % (page,)
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "lxml")
    my_html = soup.find_all("a",{"class":"search_result_row ds_collapse_flag"},True)
    return link_extractor(my_html)


def go_in_link(url):
    request = requests.get(url)
    content = request.content
    result = dict()
    result.update({'title':get_title(content),'purchase_price': get_purchase_price(content),
                   'details':get_details(content), 'description':get_description(content),
                   'tags':get_tags(content),'overall':get_overall(content),'date':get_rdate(content),
                   'discount': get_discount(content), 'before_discount_original': get_before_discount(content),
                   'after_discount': get_after_discount(content), 'statistics': get_statistics(content)})
    result.update(system_req(content))
    return result


def get_title(content):
    soup = BeautifulSoup(content, "lxml")
    game_title = soup.find_all("div",{"class":"apphub_AppName"},True)
    return string_corrector(game_title[0].text.encode("utf-8").decode('utf-8'))


def system_req(content):
    soup = BeautifulSoup(content, "lxml")
    os = soup.find_all("div", {"data-os":"win"},True)
    details_string = os[0].text.encode("utf-8").replace("\r", ": ")              # All details in a string
    minimum_system_str = details_string.split("\n\n\n\nRecommended")[0]
    try:
        recommended_system_str = details_string.split("\n\n\n\nRecommended")[1]
    except IndexError:
        recommended_system_str = ""
    result = dict()                             # The result dictionary
    minimum_system_list = minimum_system_str.split(": ")
    recommended_system_list = recommended_system_str.split(": ")
    # minimum system Requirements section
    # list of attributes names
    list_of_attr = ["OS", "Processor", "Memory", "Graphics", "DirectX", "Storage", "Additional Notes"]
    # list of minimum attributes names .
    min_attr_name = ["min_os", "min_processor", "min_memory", "min_graphics", "min_directx", "min_storage", "min_notes"]
    loop_counter = 0
    for attr in list_of_attr:
        try:
            pre_result = [minimum_system_list[minimum_system_list.index(attr) + 1]]
            if type(pre_result) == list:
                pre_result = pre_result[0]
        except TypeError:
            pre_result = [None]
        result.update({min_attr_name[loop_counter]: pre_result})                # Add result to the result dict
        loop_counter += 1

    # recommended system Requirements
    loop_counter = 0                                        # Restart counting
    if recommended_system_list:
        rec_attr_name = ["rec_os", "rec_processor", "rec_memory", "rec_graphics", "rec_directx", "rec_storage", "rec_notes"]
        for attr in list_of_attr:
            try:
                pre_result = recommended_system_list[recommended_system_list.index("Processor") + 1]
            except TypeError:
                pre_result = None
            # Add to the result
            result.update({rec_attr_name[loop_counter]: pre_result})
            loop_counter += 1
    return result


def get_purchase_price(content):
    soup = BeautifulSoup(content, "lxml")
    price = soup.find_all("div",{"class":"game_purchase_price"},True)
    return string_corrector(price[0].text.encode("utf-8"))


def get_details(content):
    soup = BeautifulSoup(content, "lxml")
    details = soup.find_all("div",{"class":"details_block"},True)
    return string_corrector(details[0].text.encode("utf-8"))


def get_description(content):
    soup = BeautifulSoup(content, "lxml")
    description = soup.find_all("div",{"class":"game_description_snippet"},True)
    return string_corrector(description[0].text.encode("utf-8"))


def get_overall(content):
    soup = BeautifulSoup(content, "lxml")
    overall = soup.find_all("span",{"class":"game_review_summary positive"},True)
    return string_corrector(overall[0].text.encode("utf-8"))


def get_tags(content):
    soup = BeautifulSoup(content, "lxml")
    tags = soup.find_all("a",{"class":"app_tag"},True)
    return make_list(tags)


def get_rdate(content):
    soup = BeautifulSoup(content, "lxml")
    rdate = soup.find_all("span",{"class":"date"},True)
    return string_corrector(rdate[0].text.encode("utf-8"))


def get_discount(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        discount = soup.find_all("div",{"class":"discount_pct"},True)
        return string_corrector(discount[0].text.encode("utf-8"))
    except:
        return '$none$'


def get_before_discount(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        before = soup.find_all("div",{"class":"discount_original_price"},True)
        return string_corrector(before[0].text.encode("utf-8"))
    except:
        return '$none$'


def get_after_discount(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        after = soup.find_all("div",{"class":"discount_final_price"},True)
        return string_corrector(after[0].text.encode("utf-8"))
    except:
        return '$none$'


def get_statistics(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        statistics = soup.find_all("span",{"class":"nonresponsive_hidden responsive_reviewdesc"},True)
        return string_corrector(statistics[0].text.encode("utf-8"))
    except:
        return 'code10'
print go_in_link(scrapper_first_layer('1')[0])
#print go_in_link('http://store.steampowered.com/app/292030/?snr=1_7_7_230_150_1')#  HANDLE SYS REQUIRE
#print go_in_link('http://store.steampowered.com/agecheck/app/359870/?snr=1_7_7_230_150_1') #####  HANDLE ALL DEFS
#.replace('\t','')
#span.class : nonresponsive_hidden responsive_reviewdesc