# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：get_detail.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/11/21 19:24 
'''
import requests
import lxml
from lxml import etree
import pymongo
from pymongo import MongoClient
import random
import time
import pyppeteer
from pyppeteer import launch
import asyncio


client = MongoClient("127.0.0.1",27017)
db = client["boss"]
collection = db["python"]
search_key = "href"
url_list = []
detail_list = []
browser = None
headers = {
    "User-Agent":
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Referer":
"https://www.zhipin.com/job_detail/",

}
async def go_to_page(url) :
    info = {}
    global browser
    if browser is None :
        browser = await launch({"headless":False,"args":"--disable-infobars"})
    # pages = await browser.pages()
    # for p in pages[:-1] :
    #     await p.close()
    page = await browser.newPage()
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    await page.waitFor(500)
    await page.goto(url)
    await asyncio.sleep(1)
    # await page.evaluate('document.cookie = ""')
    await page.waitForSelector("#main > div.job-box > div > div.job-detail > div:nth-child(1) > div.job-sec-text")
    detail = await page.Jeval("#main > div.job-box > div > div.job-detail > div:nth-child(1) > div.job-sec-text","node => node.innerText")
    # print(detail)
    info["detail"] = str(detail).strip()
    company_name = await page.Jeval("#main > div.job-box > div > div.job-sider > div.sider-company > div > a:nth-child(2)","node => node.title")
    info["company_name"] = company_name
    detail_list.append(info)
    await page.close()
    await page.waitFor(500)
    # await browser.close()



def get_random_time() :
    index = random.uniform(0.5,1)
    time.sleep(index)

def read_data(key) :
    values = collection.distinct(key=key)[:20]
    url_list = [str(value).lstrip("'") for value in values]
    return url_list

#def update_data() :



# def connect(url) :
#     session = requests.Session()
#     res = session.get(url=url,headers=headers)
#     # print(res.status_code)
#     html = res.text
#     print(html)
#     return html
#
# def parse(html) :
#     data = etree.HTML(html)
#     detail = data.xpath('//*[@class="job-sec-text"]/text()')
#     detail_list.append(detail)
#
# def show() :
#     print(detail_list)
#
async def main() :
    url_list = read_data(search_key)
    for url in url_list :
        await go_to_page(url)
    print(detail_list)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
