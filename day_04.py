# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：day_04.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/10/10 15:16 
'''
import asyncio  # 异步编程库
import random  # 随机数生成库
import csv  # CSV文件处理库
from pyppeteer import launch  # 网页自动化测试库
from lxml import etree  # XML和HTML解析库
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

#爬取boss招聘信息

class Boss(object):
    def __init__(self):
         self.data_list = list()  # 数据列表
         self.infos = {}

    def screen_size(self):
        """使用tkinter获取屏幕大小"""
        import tkinter  # GUI工具库
        tk = tkinter.Tk()  # 创建窗口
        width = tk.winfo_screenwidth()  # 获取屏幕宽度
        height = tk.winfo_screenheight()  # 获取屏幕高度
        tk.quit()  # 关闭窗口
        return width, height  # 返回屏幕宽度和高度

    async def main(self):
        try:
            browser = await launch(
                headless=False,  # 是否无头模式（可见/不可见浏览器）
                userDataDir="./config",  # 用户数据目录（用于保持浏览器会话）
                args=['--disable-infobars', '--window-size=1366,768', '--no-sandbox']  # 启动参数
            )

            page = await browser.newPage()  # 创建新页面
            width, height = self.screen_size()  # 获取屏幕大小
            await page.setViewport({'width': width, 'height': height})  # 设置页面视口大小

            await page.goto(
                'https://www.zhipin.com/?city=100010000&ka=city-sites-100010000')  # 打开目标网页
            await page.evaluateOnNewDocument(
                '''() =>{ Object.defineProperties(navigator, { webdriver: { get: () => false } }) }'''
            )  # 修改浏览器环境，防止被检测为自动化测试工具
            await page.evaluate('document.cookie = ""')
            await asyncio.sleep(5)  # 等待页面加载

            # 查询数据岗位
            await page.type(
                '#wrap > div.column-search-panel > div > div > div.search-form > form > div.search-form-con > p > input',
                '大数据'
                '', {'delay': self.input_time_random() - 50}
            )  # 在搜索框中输入关键词
            await asyncio.sleep(2)  # 等待输入完成

            # 点击搜索按钮
            await page.click('#wrap > div.column-search-panel > div > div > div.search-form > form > button')
            await asyncio.sleep(5)  # 等待搜索结果加载


            xpath = '//div[@class="boss-login-dialog-content"]'
            try :
                element = await page.waitForXPath(xpath,{"timeout": 5000})
                await page.waitForSelector("body > div.boss-login-dialog > div.boss-login-dialog-content > div.boss-login-dialog-header > span > i")
                await page.waitFor(500)
                await asyncio.sleep(2)
                await page.click("body > div.boss-login-dialog > div.boss-login-dialog-content > div.boss-login-dialog-header > span > i")
                await asyncio.sleep(2)
            except :
                print("没有出现登录弹窗")


            i =0
            while True:
                await asyncio.sleep(2)  # 等待页面加载
                content = await page.content()  # 获取页面内容
                html = etree.HTML(content)  # 解析页面内容
                self.parse_html(html)  # 解析内容
                await page.click(
                    '#wrap > div.page-job-wrapper > div.page-job-inner > div > div.job-list-wrapper > div.search-job-result > div > div > div > a:nth-child(10)'
                )  # 点击下一页按钮
                await asyncio.sleep(3)  # 等待页面加载
                i += 1
                print(i)
                # boss直聘限制翻页为10页，分省分批次抓取
                if i >= 10:
                    break
            self.save_data()
        except Exception as a:
            print(a)


    def input_time_random(self):
        return random.randint(100, 151)  # 生成随机的输入延迟时间

    def parse_html(self, html):
        li_list = html.xpath('//div[@class="search-job-result"]//ul[@class="job-list-box"]/li')  # 获取职位列表

        for li in li_list:

            job_name = li.xpath('.//span[@class="job-name"]/text()')[0]  # 工作名称
            job_salary = li.xpath('.//div[@class="job-info clearfix"]/span/text()')[0]  # 薪资待遇
            company_name = li.xpath('.//div[@class="company-info"]//h3/a/text()')[0]  # 公司名称
            # job_exp = li.xpath('.//div[@class="job-info clearfix"]/ul/li/text()')[0]  # 年限要求
            job_address = li.xpath('.//span[@class="job-area"]/text()')[0]  # 工作地点
            # welfare = ' '.join(li.xpath('.//div[@class="info-desc"]/text()'))  # 福利待遇
            self.infos["job_name"] = job_name
            self.infos["job_salary"] = job_salary
            self.infos["company_name"] = company_name
            # self.infos["job_exp"] = job_exp
            self.infos["job_address"] = job_address
            # self.infos["welfare"] = welfare

            demand = ''
            span_list = li.xpath('.//div[@class="job-card-footer clearfix"]/ul[@class="tag-list"]')
            for span in span_list:
                demand = ' '.join(span.xpath('./li/text()'))  # 任职需求

            self.infos["demand"] = demand
            #self.infos["number"] = i
            self.data_list.append(self.infos)

            # print(job_name, job_salary, job_address, job_exp, company_name, demand, welfare)

        print(self.data_list)

            # with open('boss_data.csv', encoding='utf-8', mode='a', newline='') as f:
            #     csv_writer = csv.writer(f)
            #     # csv_writer.writerow([job_name, job_salary, job_address, job_exp, company_name, demand, welfare])  # 保存数据
            #     csv_writer.writerow(self.data_list)
    def save_data(self) :
        client = MongoClient("127.0.0.1",27017)
        DB = client["boss"]
        collection = DB["spider data"]
        for data in self.data_list :
            data["_id"] = ObjectId()
            collection.insert_one(data)
        # status = collection.insert_many(self.data_list)
        # if status.acknowledged :
        #     print("successfully")
        # else:
        #     print("failed")





    def run(self):
        asyncio.get_event_loop().run_until_complete(self.main())  # 运行异步任务
        self.save_data()


if __name__ == '__main__':
    # with open('new.csv', encoding='utf-8', mode='a', newline='') as f:
    #     csv_writer = csv.writer(f)
    #     csv_writer.writerow(['job_name', 'job_salary', 'job_address', 'job_exp', 'company_name', 'demand', 'welfare'])

    comment = Boss()
    data = []
    data = comment.data_list
    comment.run()
    comment.save_data(data)