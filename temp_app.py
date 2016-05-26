# -*- coding: utf-8 -*-
import threading
import requests
from bs4 import BeautifulSoup


class thread_scrap(threading.Thread):
    def __init__(self, func, arg):
        threading.Thread.__init__(self)
        self.arg = arg
        self.func = func
        self.result = []

    def run(self):
        self.result = self.func(self.arg)

    def get_result(self):
        return self.result


def scrapper(page=1):
    link_in_pages = []
    results = []
    first_layer_threads = []
    second_layer_threads = []
    for i in range(1, page+1):
        t = thread_scrap(scrapper_first_layer, str(i))
        first_layer_threads.append(t)
        t.start()
    for j in first_layer_threads:
        j.join()
        link_in_pages.append(j.get_result())
    for k in range(len(link_in_pages)):
        for link in link_in_pages[k]:
            t = thread_scrap(go_in_link, link)
            second_layer_threads.append(t)
            t.start()
    for l in second_layer_threads:
        l.join()
        results.append(l.get_result())
    print results


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
    try:
        soup = BeautifulSoup(content, "lxml")
        game_title = soup.find_all("div",{"class":"apphub_AppName"},True)
        return string_corrector(game_title[0].text.encode("utf-8").decode('utf-8'))
    except:
        return 'code1'


def system_req(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        os = soup.find_all("div", {"data-os":"win"},True)
        details_string = os[0].text.encode("utf-8").replace("\r", ": ")              # All details in a string
        minimum_system_str = details_string.split("\n\n\n\nRecommended")[0]
        try:
            recommended_system_str = details_string.split("\n\n\n\nRecommended")[1]
        except IndexError:
            recommended_system_str = ""
        minimum_system_list = minimum_system_str.split(": ")
        recommended_system_list = recommended_system_str.split(": ")
        # minimum system Requirements
        min_os = minimum_system_list[minimum_system_list.index("OS") + 1]
        min_processor = minimum_system_list[minimum_system_list.index("Processor") + 1]
        min_memory = minimum_system_list[minimum_system_list.index("Memory") + 1]
        min_graphics = minimum_system_list[minimum_system_list.index("Graphics") + 1]
        min_directx = minimum_system_list[minimum_system_list.index("DirectX") + 1]
        min_storage = minimum_system_list[minimum_system_list.index("Storage") + 1]
        min_notes= minimum_system_list[minimum_system_list.index("Additional Notes") + 1]


        # result dictionary
        result = {"min_os": min_os, "min_processor": min_processor, "min_memory": min_memory, "min_graphics": min_graphics}
        result.update({"min_directs": min_directx, "min_storage": min_storage, "min_notes": min_notes})

        # recommended system Requirements
        if recommended_system_list:
            rec_os = recommended_system_list[recommended_system_list.index("OS") + 1]
            rec_processor = recommended_system_list[recommended_system_list.index("Processor") + 1]
            rec_memory = recommended_system_list[recommended_system_list.index("Memory") + 1]
            rec_graphics = recommended_system_list[recommended_system_list.index("Graphics") + 1]
            rec_directx = recommended_system_list[recommended_system_list.index("DirectX") + 1]
            rec_storage = recommended_system_list[recommended_system_list.index("Storage") + 1]
            rec_notes = recommended_system_list[recommended_system_list.index("Additional Notes") + 1]
            # Add to the result
            result = {"rec_os": rec_os, "rec_processor": rec_processor, "rec_memory": rec_memory, "rec_graphics": rec_graphics}
            result.update({"rec_directs": rec_directx, "rec_storage": rec_storage, "rec_notes": rec_notes})
        return result
    except:
        return {'system_req': 'no access'}


def get_purchase_price(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        price = soup.find_all("div",{"class":"game_purchase_price"},True)
        return string_corrector(price[0].text.encode("utf-8"))
    except:
        return 'code2'


def get_details(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        details = soup.find_all("div",{"class":"details_block"},True)
        return string_corrector(details[0].text.encode("utf-8"))
    except:
        return 'code3'


def get_description(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        description = soup.find_all("div",{"class":"game_description_snippet"},True)
        return string_corrector(description[0].text.encode("utf-8"))
    except:
        return 'code4'


def get_overall(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        overall = soup.find_all("span",{"class":"game_review_summary positive"},True)
        return string_corrector(overall[0].text.encode("utf-8"))
    except:
        return 'code5'


def get_tags(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        tags = soup.find_all("a",{"class":"app_tag"},True)
        return make_list(tags)
    except:
        return 'code6'


def get_rdate(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        rdate = soup.find_all("span",{"class":"date"},True)
        return string_corrector(rdate[0].text.encode("utf-8"))
    except:
        return 'code7'


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
        return 'code8'


#print go_in_link(scrapper_first_layer('1')[0])
#print go_in_link('http://store.steampowered.com/app/292030/?snr=1_7_7_230_150_1')#  HANDLE SYS REQUIRE
#print go_in_link('http://store.steampowered.com/agecheck/app/359870/?snr=1_7_7_230_150_1') #####  HANDLE ALL DEFS
#.replace('\t','')
#span.class : nonresponsive_hidden responsive_reviewdesc
scrapper(1)