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
from selenium.webdriver.common.action_chains import ActionChains
import time
from lxml import etree

options = ChromeOptions()
options.headless = False
options.add_argument("--no-sandbox")
driver = Chrome(options=options)
actions = ActionChains(driver)
driver.get("https://scrape.center/")
size = driver.get_window_size()
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
time.sleep(2)

wait = WebDriverWait(driver,10)
page = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="index"]/div/div/div[3]/div[11]/a/div[1]')))
actions.move_to_element(page)
actions.click().perform()
driver.execute_script('')
# page.click_safe()
time.sleep(5)

infos = []
windows = driver.window_handles
driver.switch_to.window(windows[-1])

# page_source = driver.page_source
# tree = etree.HTML(page_source)
# divs = tree.xpath('//*[@id="players"]/div/div/div/div/div/div')
# for div in divs :
#     name = div.xpath('div[2]/h3/text()')
#     height = div.xpath('div[2]/p[1]/span/text()')
#     weight = div.xpath('div[2]/p[2]/span/text()')
#     print(name,height,weight)


players = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="players"]/div/div/div/div/div/div/div[2]')))
players = driver.find_elements(By.XPATH,'//*[@id="players"]/div/div/div/div/div/div/div[2]')
for player in players :
    print(player.text)
info = {}
names = driver.find_elements_recursive(By.XPATH,'//*[@id="players"]/div/div/div/div/div/div/div[2]/h3')
hs = driver.find_elements_recursive(By.XPATH,'//*[@id="players"]/div/div/div/div/div/div/div[2]/p[1]/span')
ws = driver.find_elements_recursive(By.XPATH,'//*[@id="players"]/div/div/div/div/div/div/div[2]/p[2]/span')
for name,h,w in zip(names,hs,ws):
    info["name"] = name.text
    info["height"] = h.text
    info["weight"] = w.text
    infos.append(info)
print(infos)
print("宽度",size["width"])
print("高度",size["height"])


time.sleep(2)
#driver.execute_script()
driver.quit()


