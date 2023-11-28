# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：get_detail.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/11/21 19:24 
'''
import pymongo
from pymongo import MongoClient
import pyppeteer
from pyppeteer import launch
import asyncio
import time
import random

#获取30条详情并插入相应记录
client = MongoClient("127.0.0.1",27017)
db = client["boss"]
collection = db["java"]
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
num = 0


async def go_to_page(url) :
    info = {}
    global browser
    global num
    num += 1
    print(num)
    if browser is None :
        browser = await launch(headless=False,args=["--disable-infobars"])
    page = await browser.newPage()
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    await page.waitFor(500)
    await page.waitFor(2000)
    await page.goto(url)
    await page.evaluateOnNewDocument(
        '''() =>{ Object.defineProperties(navigator, { webdriver: { get: () => false } }) }'''
    )  # 修改浏览器环境，防止被检测为自动化测试工具
    await page.evaluate('document.cookie = ""')
    await page.waitFor(500)
    await asyncio.sleep(1)
    # await page.evaluate('document.cookie = ""')
    await page.waitForSelector("#main > div.job-box > div > div.job-detail > div:nth-child(1) > div.job-sec-text")
    detail = await page.Jeval("#main > div.job-box > div > div.job-detail > div:nth-child(1) > div.job-sec-text","node => node.innerText")
    print(detail)
    info["detail"] = str(detail).strip()
    detail_list.append(info)
    await page.close()
    await asyncio.sleep(1)
    await page.waitFor(500)
    if num >= 30 :
        num = 1
        await browser.close()

    # await browser.close()



def get_random_time() :
    index = random.uniform(0.5,1)
    time.sleep(index)

def read_data(key) :
    values = collection.find().sort('_id', pymongo.ASCENDING).limit(30)   #按_id值升序排序取出值
    url_list = [str(value["href"]).lstrip("'") for value in values]
    print(len(url_list))
    return url_list


async def run(url_list) :
    for url in url_list:
        await go_to_page(url)
        get_random_time()

async def main() :
    url_list = read_data(search_key)
    await run(url_list)

    # 获取集合中的所有文档
    documents = collection.find()

    # 遍历文档并为每个文档添加新字段
    for index, data in enumerate(detail_list):
        new_field_name = 'detail'
        new_field_value = data['detail']
        status = collection.update_one({'_id': documents[index]['_id']}, {'$set': {new_field_name: new_field_value}})
        if status.acknowledged :
            print("success")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
