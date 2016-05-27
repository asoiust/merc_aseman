# -*- coding: utf-8 -*-
import threading
import requests
from bs4 import BeautifulSoup
from database import *


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
        add_game(l.get_result())
    return results


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
                   'user_tags':get_tags(content),'overall':get_overall(content),'release_date':get_rdate(content),
                   'discount': get_discount(content), 'original_price': get_before_discount(content),
                   'after_discount': get_after_discount(content), 'url': url})
    print get_statistics(content)
    result.update(get_statistics(content))
    try:
        result.update(system_req(content))
    except TypeError:
        pass
    return result


def get_title(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        game_title = soup.find_all("div",{"class":"apphub_AppName"},True)
        return string_corrector(game_title[0].text.encode("utf-8").decode('utf-8'))
    except:
        return 'code1'


def system_req(content):
    soup = BeautifulSoup(content, "lxml")
    os = soup.find_all("div", {"data-os":"win"},True)
    try:
        details_string = os[0].text.encode("utf-8").replace("\r", ": ")              # All details in a string
    except Exception:
        return
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
        except ValueError:
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
            except ValueError:
                pre_result = None
            # Add to the result
            result.update({rec_attr_name[loop_counter]: pre_result})
            loop_counter += 1
    return result


def get_purchase_price(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        price = soup.find_all("div",{"class":"game_purchase_price"},True)
        price_string = string_corrector(price[0].text.encode("utf-8"))
        if price_string == 'Free To Play':
            return '0'
        price_string = price_string.split(" ")[0]
        price_string = price_string.replace("$", "")
        return price_string
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
        return '0'


def get_before_discount(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        before = soup.find_all("div",{"class":"discount_original_price"},True)
        before_string = string_corrector(before[0].text.encode("utf-8"))
        before_string = before_string.split(" ")[0]
        before_string = before_string.replace("$", "")
        return before_string
    except:
        return '0'


def get_after_discount(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        after = soup.find_all("div", {"class": "discount_final_price"},True)
        after_string = string_corrector((after[0].text.encode("utf-8"))).split(" ")[0]
        after_string = after_string.replace("$", "")
        return string_corrector(after[0].text.encode("utf-8"))
    except Exception:
        return '0'


def get_statistics(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        statistics = soup.find_all("span", {"class": "nonresponsive_hidden responsive_reviewdesc"},True)
        print statistics
        statics_list = string_corrector((statistics[0].text.encode("utf-8"))).split(" ")
        try:
            percent = statics_list[1].replace("%", "")
        except IndexError:
            print "KIR"
            print statics_list
            percent = "0"
        try:
            reviews = statics_list[4].replace(",", "")
        except IndexError:
            print "KIR"
            print statics_list
            reviews = "0"
        return {"statics": percent, "reviews": reviews}
    except:
        return {"statics": 0, "reviews": 0}



###############################################################################################
#FIRST LAYER

def discount_lister(dis_list):
    result = []
    for item in dis_list:
        if item.text == '':       #########dorostesh kon
            result.append("0%")
        else:
            result.append(string_corrector(item.text))
    return result


def price_lister(pr_list):
    result = []
    for item in pr_list:
        item = str(string_corrector(item.text))
        splited = item.split('%')
        if len(splited) == 2:
            result.append((splited[1].split("$")[1],splited[1].split("$")[2]))
        else:
            result.append(item)
    return result


def go_in_first_page(page):
    page = str(page)
    url = 'http://store.steampowered.com/search/results?sort_by=_ASC&tags=-1&category1=998&page=%s&snr=1_7_7_230_7' % (page,)
    request = requests.get(url)
    content = request.content
    result = dict()
    result.update({'title': get_title_first(content), 'rdate': get_rdate_first(content),
                   'price': get_price_first(content), 'discount': get_discount_first(content) })
    return result


def get_title_first(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        title = soup.find_all("span",{"class":"title"},True)
        return make_list(title)
    except:
        return 'code9'


def get_rdate_first(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        rdate = soup.find_all("div",{"class":"col search_released responsive_secondrow"},True)
        return make_list(rdate)
    except:
        return 'code10'


def get_price_first(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        price = soup.find_all("div",{"class":"col search_price_discount_combined responsive_secondrow"},True)
        return price_lister(price)
    except:
        return 'code11'


def get_discount_first(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        discount = soup.find_all("div",{"class":"col search_discount responsive_secondrow"},True)
        return discount_lister(discount)
    except:
        return 'code12'
# print go_in_first_page(1)
'''
game title : span.title
release date : div.col search_released responsive_secondrow     # First div with this classes
price : #parent div : div.col search_price_discount_combined responsive_secondrow
#container div class  : div.col search_price  responsive_secondrow
release date : div.col search_released responsive_secondrow   #first div
discount : span child of second div.col search_discount responsive_secondrow
before discount price: span.style="color: #888888;"
price : last div.col search_price discounted responsive_secondrow
'''
# print go_in_link(scrapper_first_layer('1')[0])
#print go_in_link('http://store.steampowered.com/app/292030/?snr=1_7_7_230_150_1')#  HANDLE SYS REQUIRE
#print go_in_link('http://store.steampowered.com/agecheck/app/359870/?snr=1_7_7_230_150_1') #####  HANDLE ALL DEFS
#.replace('\t','')
#span.class : nonresponsive_hidden responsive_reviewdesc
print scrapper(1)
#print str((repr(u'')))