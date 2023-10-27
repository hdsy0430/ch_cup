# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：uc.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/10/24 15:20 
'''
import undetected_chromedriver as uc
from undetected_chromedriver import Chrome,ChromeOptions
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

options = ChromeOptions()
options.headless = False
options.add_argument("--no-sandbox")
driver = Chrome(options=options)

driver.get("https://scrape.center/")

wait = WebDriverWait(driver,10)
page = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="index"]/div/div/div[3]/div[11]')))
page.click()
time.sleep(2)

infos = []
windows = driver.window_handles
driver.switch_to.window(windows[-1])

# def is_exist (xpath) :
#     try :
#         new_page = wait.until(EC.visibility_of_element_located((By.XPATH,xpath)))
#         return True
#     except :
#         return False
xpath = '//*[@id="players"]/div/div/div'
try :
    divs = driver.find_element(by=By.XPATH,value=xpath)
    print("exist")
except :
    print("no such element")
info = {}
#for div in divs :
 #   info[""]


#driver.execute_script()
driver.quit()


