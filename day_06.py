# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：day_06.py
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
import time
import random
from lxml import etree
import pymongo
from pymongo import MongoClient

# 浏览器与对象初始化
options = uc.ChromeOptions()
options.headless = False
options.add_argument("--no-sandbox")
options.add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
driver = uc.Chrome(options=options)
actions = ActionChains(driver)
wait = WebDriverWait(driver, 10)

i = 0  # 用于计算页数

client = MongoClient('127.0.0.1', 27017)
db = client["boss"]
collection = db["deep_learning"]

url = "https://www.zhipin.com/hangzhou/"
base_xpath_1 = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li'
base_xpath_2 = '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li'


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
    get_random_time()
    input_element = driver.find_element(By.XPATH, '//*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/div[2]/p/input')
    time.sleep(2)
    actions.move_to_element(input_element)
    actions.click(input_element)
    get_random_time()
    actions.send_keys("深度学习")  # 输入
    get_random_time()
    actions.perform()

    element = driver.find_element(By.XPATH, '//*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/button')  # 点击搜索
    actions.move_to_element(element)
    actions.click()
    actions.perform()
    time.sleep(5)
    change_new_page()  # 切换页面

    # 处理可能出现的弹窗
    try:
        login_window = wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[9]/div[2]')))
        get_random_time()
        close_tab = driver.find_element(By.CSS_SELECTOR,
                                        'body > div.boss-login-dialog > div.boss-login-dialog-content > div.boss-login-dialog-header > span > i')
        time.sleep(1)
        close_tab.click()
        get_random_time()
    except:
        print("no login windows")
    return driver.page_source


# 切换至新页面
def change_new_page():
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    get_random_time()
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight/2);')
    time.sleep(1)

# 解析页面
def parse_page(html,base_xpath):
    tree = etree.HTML(html)
    infos = []
    lis = tree.xpath(base_xpath)
    for li in lis:
        info = {}
        info["job_name"] = li.xpath('div[1]/a/div[1]/span[1]/text()')
        info["address"] = li.xpath('div[1]/a/div[1]/span[2]/span/text()')
        info["salary"] = li.xpath('div[1]/a/div[2]/span/text()')
        info["company_name"] = li.xpath('div[1]/div/div[2]/h3/a/text()')
        info["demand"] = li.xpath('div[2]/ul/li/text()')
        infos.append(info)
    print(infos)
    save_data(infos)
    time.sleep(5)

def go_to_next():
    # next_page_1 = driver.find_element(By.CSS_SELECTOR,
    #                                   '#wrap > div.page-job-wrapper > div.page-job-inner > div > div.job-list-wrapper > div.search-job-result > div > div > div > a:nth-child(10)')
    # next_page_2 = driver.find_element(By.CSS_SELECTOR,'#wrap > div.page-job-wrapper > div.page-job-inner > div > div.job-list-wrapper > div.search-job-result > div > div > div > a:nth-child(11)')
    global i
    i += 1
    if i == 5 or i == 6 :
        next_page = driver.find_element(By.CSS_SELECTOR,
                                    '#wrap > div.page-job-wrapper > div.page-job-inner > div > div.job-list-wrapper > div.search-job-result > div > div > div > a:nth-child(11)')

    else:
        next_page = driver.find_element(By.CSS_SELECTOR,
                                      '#wrap > div.page-job-wrapper > div.page-job-inner > div > div.job-list-wrapper > div.search-job-result > div > div > div > a:nth-child(10)')

    actions.move_to_element(next_page)
    actions.click(next_page)
    actions.perform()
    get_random_time()
    time.sleep(3)
    change_new_page()
    new_url = driver.current_url
    print(new_url)
    time.sleep(3)
    new_page = driver.page_source
    parse_page(new_page, base_xpath_2)


    if i >= 10 :
        print("exceed")
        driver.quit()


def main():

    page = get_page(url)
    parse_page(page,base_xpath_1)
    while i < 10 :
        go_to_next()
if __name__ == '__main__':
    main()

