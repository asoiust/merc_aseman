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


class second_leyer_thread(threading.Thread):
    def __init__(self, func, arg):
        threading.Thread.__init__(self)
        self.arg = arg
        self.func = func
        self.result = None

    def run(self):
        self.result = self.func(self.arg)

    def get_result(self):
        return self.result


def scrapper_ver5(page=1):
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
        link_in_pages += j.get_result()
    for link in link_in_pages:
        t = thread_scrap(go_in_link, link)
        second_layer_threads.append(t)
        t.start()
    for l in second_layer_threads:
        l.join()
        temp = l.get_result()
        results.append(temp)
        add_game(temp)
    return results
    #return True


def go_in_link_ver2(url):
    request = requests.get(url)
    content = request.content
    funcs = [get_title(content), get_purchase_price(content), get_details(content),
                 get_description(content), get_tags(content), get_overall(content), get_rdate(content)
                 , get_discount(content), get_before_discount(content), get_after_discount(content),
                 get_statistics(content), system_req(content)]
    result = dict()
    result.update({'title':funcs[0],'purchase_price': funcs[1],
                   'details':funcs[2], 'description':funcs[3],
                   'user_tags':funcs[4],'overall':funcs[5],'release_date':funcs[6],
                   'discount': funcs[7], 'original_price': funcs[8],
                   'after_discount': funcs[9], 'url': url})
    result.update(funcs[10])
    try:
        result.update(funcs[11])
    except TypeError:
        pass
    return result


def scrapper_ver4(page=1):
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
        link_in_pages += j.get_result()
        #print link_in_pages
    for link in link_in_pages:
        t = thread_scrap(go_in_link_ver2, link)
        second_layer_threads.append(t)
        t.start()
    for l in second_layer_threads:
        l.join()
        pre_result = l.get_result()
        results.append(pre_result)
        add_game(pre_result)
    return results
    #return True



def scrapper(page=1):
    link_in_pages = []
    results = []
    first_layer_threads = []
    second_layer_threads = []
    for i in range(page, page+1):
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
        # add_game(l.get_result())
    return results
    #return True


def final(page=1):
    temp = []
    for i in range(1, page+1):
        temp += scrapper(i)
    # return temp
    for item in temp:
        add_game(item)
    return True


def scrapper_ver3(page=1):
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
        link_in_pages += j.get_result()
    #for link in link_in_pages:
    #    t = thread_scrap(go_in_link, link)
    #    second_layer_threads.append(t)
    #    t.start()
    #for l in second_layer_threads:
    #    l.join()
    #    results.append(l.get_result())
        #add_game(l.get_result())
    print link_in_pages
    for link in link_in_pages:
        pre_result = go_in_link(link)
        results += pre_result
        add_game(pre_result)
    return results
    #return True



def scrapper_ver2(page=1):
    link_in_pages = []
    results = []
    second_layer_threads = []
    link_in_pages = scrapper_first_layer(str(page))
    #print link_in_pages
    for link in link_in_pages:
        t = thread_scrap(go_in_link, link)
        second_layer_threads.append(t)
        t.start()
    for l in second_layer_threads:
        l.join()
        results.append(l.get_result())
        #add_game(l.get_result())
    return results
    #return True


def final_ver2(pages):
    results = []
    threads = []
    for i in range(1, pages+1):
        t = thread_scrap(scrapper_ver2, str(i))
        threads.append(t)
        t.start()
    for j in threads:
        j.join()
        temp = j.get_result()
        results += temp
        add_game(temp)
    return results
    #return True


def link_extractor(my_html):
    result = []
    for item in my_html:
        result.append(str(item.get('href')).split("?")[0])
    return result


def make_list(my_list):
    result = []
    for item in my_list:
        result.append(item.text.replace('\t', '').replace('\n', '').replace('\r', ''))
    return result


def string_corrector(string):
    return string.replace('\t', '').replace('\n', '').replace('\r', '')


def scrapper_first_layer(page):
    url = 'http://store.steampowered.com/search/results?sort_by=Released_DESC&tags=-1&category1=998&page=%s&snr=1_7_7_230_7' % (page,)
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "lxml")
    my_html = soup.find_all("a",{"class":"search_result_row ds_collapse_flag"},True)
    return link_extractor(my_html)


def threaded_calculator_one(content):
    functions = [get_title, get_purchase_price, get_details,
                 get_description, get_tags, get_overall, get_rdate
                 , get_discount, get_before_discount, get_after_discount,
                 get_statistics, system_req]
    result = []
    threads = []
    for item in functions:
        t = second_leyer_thread(item, content)
        threads.append(t)
        t.start()
    for j in threads:
        j.join()
        result.append(j.get_result())
    return result


def go_in_link(url):
    request = requests.get(url)
    content = request.content
    funcs = threaded_calculator_one(content)
    result = dict()
    result.update({'title':funcs[0],'purchase_price': funcs[1],
                   'details':funcs[2], 'description':funcs[3],
                   'user_tags':funcs[4],'overall':funcs[5],'release_date':funcs[6],
                   'discount': funcs[7], 'original_price': funcs[8],
                   'after_discount': funcs[9], 'url': url})
    result.update(funcs[10])
    try:
        result.update(funcs[11])
    except TypeError:
        pass
    return result


def get_title(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        game_title = soup.find_all("div",{"class":"apphub_AppName"},True)
        return string_corrector(game_title[0].text.encode("utf-8").decode('utf-8'))
    except:
        return '0'


def system_req(content):
    soup = BeautifulSoup(content, "lxml")
    os = soup.find_all("div", {"data-os":"win"},True)
    try:
        if len(os) == 1:
            details_string = os[0].text.encode("utf-8").replace("\r", ": ")              # All details in a string
        else:
            details_string = os[-1].text.encode("utf-8").replace("\r", ": ")  # All details in a string
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
            if attr in minimum_system_list:
                pre_result = [minimum_system_list[minimum_system_list.index(attr) + 1]]
            else:
                pre_result = [""]
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
                if attr in recommended_system_list:
                    pre_result = recommended_system_list[recommended_system_list.index(attr) + 1]
                else:
                    pre_result = [""]
            except ValueError:
                pre_result = None
            # Add to the result
            result.update({rec_attr_name[loop_counter]: pre_result})
            loop_counter += 1
    return result


def get_purchase_price(content):
    try:
        # print content
        soup = BeautifulSoup(content, "lxml")
        price = soup.find_all("div",{"class":"game_purchase_price price"},True)
        #print "kir"
        #print price
        price_string = string_corrector(price[0].text.encode("utf-8"))
        # if type(price_string) == str:
        #     return '0'
        #print price_string
        price_string = price_string.split(" ")[0]
        price_string = price_string.replace("$", "")
        return price_string
    except:
         return '0'


def genre_exrtreactor(my_string):
    temp = my_string.split("Genre:")
    temp2 = string_corrector(repr(temp[1]))
    temp3 = temp2.split('Developer:')
    temp4 = temp3[0].replace(" ", "")
    return temp4[1:]


def get_details(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        details = soup.find_all("div",{"class":"details_block"},True)
        #print repr(details[0].text)
        return genre_exrtreactor(str(string_corrector(details[0].text.encode("utf-8"))))
    except:
        return '0'


def get_description(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        description = soup.find_all("div",{"class":"game_description_snippet"},True)
        return string_corrector(description[0].text.encode("utf-8"))
    except:
        return '0'


def get_overall(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        overall = soup.find_all("span",{"class":"game_review_summary positive"},True)
        return string_corrector(overall[0].text.encode("utf-8"))
    except:
        return '0'


def get_tags(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        tags = soup.find_all("a",{"class":"app_tag"},True)
        return make_list(tags)
    except:
        return '0'


def get_rdate(content):
    try:
        months_name = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        soup = BeautifulSoup(content, "lxml")
        rdate = soup.find_all("span",{"class":"date"},True)
        date_list= string_corrector(rdate[0].text.encode("utf-8")).split(" ")
        result = date_list[2] + "-" + str(months_name.index(date_list[1].replace(",", "")) + 1) + "-" + date_list[0]
        return result
    except:
        return '0-0-0'


def get_discount(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        discount = soup.find_all("div",{"class":"discount_pct"},True)
        return string_corrector(discount[0].text.encode("utf-8")).replace("-","").replace("%","")
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
        return after_string
    except Exception:
        return '0'


def get_statistics(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        statistics = soup.find_all("span", {"class": "nonresponsive_hidden responsive_reviewdesc"},True)
        statics_list = string_corrector((statistics[0].text.encode("utf-8"))).split(" ")
        try:
            percent = statics_list[1].replace("%", "")
        except IndexError:
            percent = "0"
        try:
            reviews = statics_list[4].replace(",", "")
        except IndexError:
            reviews = "0"
        return {"static": percent, "reviews": reviews}
    except:
        return {"static": 0, "reviews": 0}



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
        # print splited
        if len(splited) == 2:
            result.append((splited[1].split("$")[1], splited[1].split("$")[2]))
        else:
            result.append((item,))
    return result


def first_layer_pages_scrapper(page=1):   #maybe u need this
    results = []
    threads = []
    for i in range(1,page+1):
        t = thread_scrap(go_in_first_page, i)
        threads.append(t)
        t.start()
    for j in threads:
        j.join()
        results.append(j.get_result())
    add_summary(results)
    return results  #age khasti extractor ro bardar


def threaded_calculator_two(content):
    functions = [get_title_first, get_rdate_first, get_price_first, get_discount_first, get_pics_first]
    result = []
    threads = []
    for item in functions:
        t = second_leyer_thread(item, content)
        threads.append(t)
        t.start()
    for j in threads:
        j.join()
        result.append(j.get_result())
    return result


def go_in_first_page(page):
    page = str(page)
    url = 'http://store.steampowered.com/search/results?sort_by=Released_DESC&tags=-1&category1=998&page=%s&snr=1_7_7_230_7' % (page,)
    request = requests.get(url)
    content = request.content
    urls = scrapper_first_layer(page)
    funcs = threaded_calculator_two(content)
    result = dict()
    result.update({'title': funcs[0], 'rdate': funcs[1],

                   'price': funcs[2], 'discount': funcs[3], 'url': urls, 'pics': funcs[4]})
    return result


def get_pics_first(content):
    try:
        result = []
        soup = BeautifulSoup(content, "lxml")
        pic = soup.find_all("img",{},True)
        for item in pic:
            result.append(item.get('src'))
        return result
    except:
        return '0'


def get_title_first(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        title = soup.find_all("span",{"class":"title"},True)
        return make_list(title)
    except:
        return 'code1'


def get_rdate_first(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        rdate = soup.find_all("div",{"class":"col search_released responsive_secondrow"},True)
        return make_list(rdate)
    except:
        return '0'


def get_price_first(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        price = soup.find_all("div",{"class":"col search_price_discount_combined responsive_secondrow"},True)
        # print "kir"
        # print price
        return price_lister(price)
    except:
        return '0'


def get_discount_first(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        discount = soup.find_all("div",{"class":"col search_discount responsive_secondrow"},True)
        return discount_lister(discount)
    except:
        return '0'


def extractor(my_list):
    url = []
    discount = []
    title = []
    price = []
    rdate = []
    for item in my_list:
        url += item['url']
        title += item['title']
        price += item['price']
        rdate += item['rdate']
        discount += item['discount']
    return [url, discount, title, price, rdate]



####################################################################################################
#SEMAPHORE VERSION


class semaphore_thread(threading.Thread):
    def __init__(self, func, arg, semaphore):
        threading.Thread.__init__(self)
        self.arg = arg
        self.func = func
        self.result = []
        self.semaphore = semaphore

    def run(self):
        self.semaphore.acquire()
        try:
            self.result = self.func(self.arg)

        finally:
            self.semaphore.release()

    def get_result(self):
        return self.result


def go_in_link_ver3(url):
    request = requests.get(url)
    content = request.content
    funcs = threaded_calculator_one(content)
    result = dict()
    result.update({'title':funcs[0],'purchase_price': funcs[1],
                   'details':funcs[2], 'description':funcs[3],
                   'user_tags':funcs[4],'overall':funcs[5],'release_date':funcs[6],
                   'discount': funcs[7], 'original_price': funcs[8],
                   'after_discount': funcs[9], 'url': url})
    result.update(funcs[10])
    try:
        result.update(funcs[11])
    except TypeError:
        pass
    #add_game(result)
    #print result
    return result



def scrapper_ver6(page=1):
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
        link_in_pages += j.get_result()
        #print link_in_pages
    #semaphore = threading.BoundedSemaphore(15)
    semaphore = threading.Semaphore(10)
    #counter = 0
    for link in link_in_pages:
        t = semaphore_thread(go_in_link_ver3, link, semaphore)
        second_layer_threads.append(t)
        t.start()
        #counter += 1
        #print counter
    for l in second_layer_threads:
        l.join()
        pre_result = l.get_result()
        results.append(pre_result)
        print pre_result
        add_game(pre_result)
    #return results
    return True




###############################################################
#SEMAPHPORE FIRST LAYER

def first_layer_pages_scrapper_with_sema(page=1):   #maybe u need this
    results = []
    threads = []
    for i in range(1,page+1):
        #semaphore = threading.BoundedSemaphore(5)
        semaphore = threading.Semaphore(5)
        t = semaphore_thread(go_in_first_page, i, semaphore)
        threads.append(t)
        t.start()
    for j in threads:
        j.join()
        results.append(j.get_result())
    add_summary(results)
    return results  #age khasti extractor ro bardar




##################################################################
#LAB

def lab_gpu():
    url = 'http://www.futuremark.com/hardware/gpu'
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "lxml")
    my_html = soup.find_all("a",{"class":"productnameBold"},True)
    results = []
    for item in my_html:
        results.append(item.text)
    return results

def lab_gpu2():
    url = 'http://www.surlix.com/us/pc/11-full-ranking-gpus.php'
    request = requests.get(url)
    content = request.content
    #print content
    soup = BeautifulSoup(content, "lxml")
    my_html = soup.find_all("a",{},True)
    results = []
    for item in my_html:
        results.append(str(item.text.encode('utf-8')))
    add_gpu(results[18:-3])
    return results[18:-3]


def lab_cpu2():
    url = 'http://www.surlix.com/us/pc/5-full-ranking-processors.php'
    request = requests.get(url)
    content = request.content
    #print content
    soup = BeautifulSoup(content, "lxml")
    my_html = soup.find_all("a",{},True)
    results = []
    for item in my_html:
        results.append(str(item.text.encode('utf-8')))
    add_cpu(results[18:-3])
    return results[18:-3]




##########################################################################################
#realese date



def scrapper_first_layer_release_date(page):
    url = 'http://store.steampowered.com/search/results?sort_by=Released_DESC&tags=-1&category1=998&page=%s' % (page,)
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "lxml")
    my_html = soup.find_all("a",{"class":"search_result_row ds_collapse_flag"},True)
    return link_extractor(my_html)[:3]



def go_in_first_page_release_date(page):
    page = str(page)
    url = 'http://store.steampowered.com/search/results?sort_by=Released_DESC&tags=-1&category1=998&page=%s' % (page,)
    request = requests.get(url)
    content = request.content
    urls = scrapper_first_layer_release_date(page)
    funcs = threaded_calculator_two(content)
    result = dict()
    result.update({'title': funcs[0][:3], 'rdate': funcs[1][:3],

                   'price': funcs[2][:3], 'discount': funcs[3][:3], 'url': urls, 'pics': funcs[4][:3]})
    return result



def scrapper_ver7(page=1):
    link_in_pages = []
    results = []
    first_layer_threads = []
    second_layer_threads = []
    for i in range(1, page+1):
        t = thread_scrap(scrapper_first_layer_release_date, str(i))
        first_layer_threads.append(t)
        t.start()
    for j in first_layer_threads:
        j.join()
        link_in_pages += j.get_result()
        #print link_in_pages
    #semaphore = threading.BoundedSemaphore(15)
    semaphore = threading.Semaphore(10)
    #counter = 0
    for link in link_in_pages[:3]:
        t = semaphore_thread(go_in_link_ver3, link, semaphore)
        second_layer_threads.append(t)
        t.start()
        #counter += 1
        #print counter
    for l in second_layer_threads:
        l.join()
        pre_result = l.get_result()
        results.append(pre_result)
        add_game(pre_result)
    return results
    #return True


def first_layer_pages_scrapper_with_sema_release_date(page=1):   #maybe u need this
    results = []
    threads = []
    for i in range(1,page+1):
        #semaphore = threading.BoundedSemaphore(5)
        semaphore = threading.Semaphore(5)
        t = semaphore_thread(go_in_first_page_release_date, i, semaphore)
        threads.append(t)
        t.start()
    for j in threads:
        j.join()
        results.append(j.get_result())
    add_summary(results)
    return results  #age khasti extractor ro bardar

def updater():
    scrapper_ver7()
    first_layer_pages_scrapper_with_sema_release_date()
    return True



def go_in_link_ver4(url):
    request = requests.get(url)
    content = request.content
    funcs = threaded_calculator_one(content)
    result = dict()
    result.update({'title':funcs[0],'purchase_price': funcs[1],
                   'details':funcs[2], 'description':funcs[3],
                   'user_tags':funcs[4],'overall':funcs[5],'release_date':funcs[6],
                   'discount': funcs[7], 'original_price': funcs[8],
                   'after_discount': funcs[9], 'url': url})
    result.update(funcs[10])
    try:
        result.update(funcs[11])
    except TypeError:
        pass
    add_game(result)
    return result



#print scrapper_ver6(1)                          baziha
#print first_layer_pages_scrapper_with_sema(1)      summary
#print go_in_link_ver4(url)          vorood be safheye bazi khas va gereftan etelaat
#print updater()               3bazi avval


















#print go_in_first_page_release_date(1)

#print updater()
#print scrapper_first_layer_release_date('1')



#print scrapper_ver6(100)

print scrapper_ver6(342)

#print scrapper_ver7(1)
#print first_layer_pages_scrapper_with_sema(2)
#print lab_cpu2()
#print lab_gpu2()

# print first_layer_pages_scrapper_with_sema(50)
#print scrapper_ver6(10)

# print first_layer_pages_scrapper_with_sema(10)

# print scrapper_ver6(350)


#print go_in_link_ver3('http://store.steampowered.com/app/364360/')
#print go_in_link_ver3('http://store.steampowered.com/app/369990/')
#print first_layer_pages_scrapper(1)
#print go_in_first_page(1)
#print go_in_link(scrapper_first_layer('1')[2])

#print go_in_first_page(1)

#print go_in_link(scrapper_first_layer('1')[1])

# print go_in_link('http://store.steampowered.com/app/292030/?snr=1_7_7_230_150_1')#  HANDLE SYS REQUIRE
# print go_in_link(1'http://store.steampowered.com/agecheck/app/359870/?snr=1_7_7_230_150_1') #####  HANDLE ALL DEFS
#.replace('\t','')
#span.class : nonresponsive_hidden responsive_reviewdesc

#print scrapper(1)

#print scrapper(1)
#print final(2)
#print str((repr(u'')))
#print scrapper_ver2(1)


#print scrapper_ver4(1)
#print scrapper_ver5(1)
#print go_in_link('http://store.steampowered.com/app/252950/?snr=1_7_7_230_150_1')


#'http://store.steampowered.com/search/results?sort_by=_ASC&tags=-1&category1=998&page=%s&snr=1_7_7_230_7'
