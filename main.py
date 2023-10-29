# import redis
# r = redis.Redis(host="127.0.0.1",port=6379,db=0)
# #r = redis.Redis(host='docker.for.win.localhost', port=6380,db=0)
# res = r.ping()
# if res :
#     # message ={
#     #     "school_2" : "hdu",
#     #     "year_2" : "2021",
#     #     "major_2" : "computer",
#     #     "sid_2" : "21052023",
#     #     "name_2" : "wsy"
#     # }
#     # r.mset(message)
#     print("success")
#     # m = r.mget("school_2","year_2","major_2","sid_2","name_2")
#     # print(m)
#
# else:
#     print("error")

import undetected_chromedriver as uc
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as  EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time

options = uc.ChromeOptions()
options.headless = False
options.add_argument("--no-sandbox")
driver = uc.Chrome(options=options)
driver.get("https://www.baidu.com/")
actions = ActionChains(driver)
wait = WebDriverWait(driver,10)

# element =wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="kw"]')))
# element.se
element = driver.find_element(By.XPATH,'//*[@id="kw"]')
actions.move_to_element(element)
actions.click_and_hold(element)
actions.send_keys("python")
actions.perform()
time.sleep(5)
