from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
import sys
from pyquery import PyQuery as pq
import re
from selenium.webdriver.support.select import Select
import match
import time
import random
import config

match_year = ['2018-2019']
browser = config.get_webdriver()
wait = WebDriverWait(browser, 10)


def get_stage(year):
    for stage in range(0, 38):
        clicks = browser.find_elements(By.CSS_SELECTOR, '#showRound tr .lsm2')

        if (len(clicks) != 38):
            print("页面按钮个数不对" + str(len(clicks)))
            sys.exit()

        clicks[stage].click()
        check = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#Table3')))
        time.sleep(random.randint(3, 8))
        ret = match.get_match(browser, year, "英超", str(stage + 1))
        if ret == 'no_start':
            break

def index_year(year):
    print("正在爬取第", year, '年')
    try:
        config.match_total = 0
        url = 'http://zq.win007.com/cn/League/%s/36.html' %(year)
        browser.get(url)
        check = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#Table1')))
        get_stage(year)
        browser.close()
        print("总场数：" + str(config.match_total))
    except TimeoutException:
        index_year(year)

def main():
    for i in match_year:
        index_year(i)

if __name__ == '__main__':
    main()
