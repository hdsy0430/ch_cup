# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：get_data.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/10/29 13:42 
'''
import undetected_chromedriver as uc
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
from lxml import etree
import pymongo
from pymongo import MongoClient
import asyncio

# 浏览器与对象初始化
options = uc.ChromeOptions()
# proxy_server = "127.0.0.1:7890"
# options.add_argument(f'--proxy-server={proxy_server}')
options.headless = False
options.add_argument("--no-sandbox")
#options.add_argument("--auto-open-devtools-for-tabs")          #开发者模式
options.add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
driver = uc.Chrome(options=options)
driver.implicitly_wait(5)
actions = ActionChains(driver)
wait = WebDriverWait(driver, 10)

i = 0  # 用于计算页数
j = 1  #用于计算悬浮标签数
client = MongoClient('127.0.0.1', 27017)
db = client["boss"]
collection = db["python"]

url = "https://www.zhipin.com/hangzhou/"
#url = 'https://www.zhipin.com/beijing/'
base_url = "'https://www.zhipin.com"
base_xpath_1 = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li'
base_xpath_2 = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li'

detail_url = []

# hover_xpath = f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[{j}]/div[1]/a/div[1]/span[1]'



# 设置随机等待时间
def get_random_time():
    wait_time = random.uniform(1, 3)
    time.sleep(wait_time)

def save_data(data):
    status = collection.insert_many(data)
    if status.acknowledged:
        print("success")
    else:
        print("failed")

# 访问目标网站
def get_page(url):
    driver.get(url)
    driver.delete_all_cookies()
    driver.execute_script("navigator.webdriver = false;")
    driver.delete_all_cookies()
    # get_random_time()
    input_element = driver.find_element(By.XPATH, '//*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/div[2]/p/input')
    time.sleep(1)
    actions.move_to_element(input_element)
    actions.click(input_element)
    get_random_time()
    actions.send_keys("python")  # 输入
    get_random_time()
    actions.perform()

    element = driver.find_element(By.XPATH, '//*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/button')  # 点击搜索
    actions.move_to_element(element)
    actions.click()
    actions.perform()
    time.sleep(5)
    change_new_page()  # 切换至页面

    # 处理可能出现的弹窗
    '''try:
        login_window = wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[9]/div[2]')))
        get_random_time()
        close_tab = driver.find_element(By.CSS_SELECTOR,
                                        'body > div.boss-login-dialog > div.boss-login-dialog-content > div.boss-login-dialog-header > span > i')
        time.sleep(1)
        close_tab.click()
        # get_random_time()
    except:
        print("no login windows")'''
    html = driver.page_source
    return html


# 切换至新页面
def change_new_page():
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    get_random_time()
    time.sleep(1)

'''def get_hover_text(link_xpath,num) :
    new_html_text_list =[]
    #hover_elements = driver.find_elements(By.XPATH,link_xpath)
    hover_element = driver.find_element(By.XPATH,hover_xpath)
    #for hover_element in hover_elements :
    # actions.move_to_element(hover_element)
    # actions.perform()
    # driver.implicitly_wait(5)
    driver.execute_script(
        "arguments[0].dispatchEvent(new MouseEvent('mouseover', { bubbles: true, cancelable: true, view: window }));",
        hover_element)
    driver.implicitly_wait(5)
    xpath =  f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[{num}]/div[1]/a/div[3]/div[2]'
    element = driver.find_element(By.XPATH,xpath)
    time.sleep(3)
    target_text =  element.text
    print(target_text)
    new_html_text_list.append(target_text)
    move_to_center()
    time.sleep(3)
    return new_html_text_list '''


'''def move_to_center() :
    width = driver.execute_script("return window.innerWidth")
    height = driver.execute_script("return window.innerHeight")
    actions.move_by_offset(10,0)
    actions.perform()
    get_random_time()'''
# 解析页面
def parse_page(html,base_xpath):
    global j
    index = 0
    infos = []
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight/2);')

    tree = etree.HTML(html)
    lis = tree.xpath(base_xpath)
    for li in lis:
        info = {}
        info["job_name"] = li.xpath('div[1]/a/div[1]/span[1]/text()')
        info["address"] = li.xpath('div[1]/a/div[1]/span[2]/span/text()')
        info["salary"] = li.xpath('div[1]/a/div[2]/span/text()')
        info["company_name"] = li.xpath('div[1]/div/div[2]/h3/a/text()')
        info["skill_demand"] = li.xpath('div[2]/ul/li/text()')
        info["company_tag"] = li.xpath('div[1]/div/div[2]/ul/li/text()')
        info["exp_demand"] = li.xpath('div[1]/a/div[2]/ul/li/text()')
        href = li.xpath('div[1]/a/@href')
        # print(href)
        need_href = [base_url + h for h in href]
        for i in need_href :
            info["href"] = i
            detail_url.append(i)
        # new_html_text_list = get_hover_text(hover_xpath, index + 1)
        # info["detail"] = new_html_text_list[index]
        infos.append(info)
        index += 1
        j += 1
    print(infos)

    # print(need_href)
    save_data(infos)
    time.sleep(5)


def go_to_next():
    next_page_xpath = '//*[@class="options-pages"]/a[last()]'
    global i
    i += 1
    # if i == 5 or i == 6 :
    #     next_page = driver.find_element(By.CSS_SELECTOR,
    #                                 '#wrap > div.page-job-wrapper > div.page-job-inner > div > div.job-list-wrapper > div.search-job-result > div > div > div > a:nth-child(11)')
    #
    # else:
    #     next_page = driver.find_element(By.CSS_SELECTOR,
    #                                   '#wrap > div.page-job-wrapper > div.page-job-inner > div > div.job-list-wrapper > div.search-job-result > div > div > div > a:nth-child(10)')
    '''elements = driver.find_elements(By.CSS_SELECTOR,
        '#wrap > div.page-job-wrapper > div.page-job-inner > div > div.job-list-wrapper > div.search-job-result > div > div > div > a')
    next_page_css = elements[-1]'''
    # next_page = next_page_css
    next = driver.find_element(By.XPATH,next_page_xpath)
    actions.move_to_element(next)
    actions.click(next)
    actions.perform()
    get_random_time()
    time.sleep(3)
    change_new_page()
    new_url = driver.current_url
    print(new_url)
    time.sleep(3)
    new_page = driver.page_source
    parse_page(new_page, base_xpath_2)


    if i >= 9 :
        print("exceed")
        driver.quit()


def main():
    page =  get_page(url)
    parse_page(page,base_xpath_1)
    while i < 9 :
        go_to_next()

if __name__ == '__main__':
   main()
