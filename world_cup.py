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

match_year = ['2018']
browser = config.get_webdriver()
wait = WebDriverWait(browser, 10)

def get_stage1(year, stage):
    print("stage1")
    for group in range(0, 8):
        clicks = browser.find_elements(By.CSS_SELECTOR, '#showRound tr .lsm2')
        if (len(clicks) != 9):
            print("小组页面按钮个数不对")
            sys.exit()

        clicks[group].click()
        check = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainTableDiv')))
        print(group)
        time.sleep(random.randint(3, 8))
        match.get_match(browser, year, "世界杯", stage)

def get_stage(year):
    for stage in range(0, 6):
        clicks = browser.find_elements(By.CSS_SELECTOR, '#SubSelectDiv td[class^="cupmatch_rw2"]')

        if (len(clicks) != 6):
            print("页面按钮个数不对" + str(len(clicks)))
            sys.exit()

        clicks[stage].click()
        check = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainTableDiv')))
        time.sleep(random.randint(3, 8)) 

        if stage == 0:
            get_stage1(year, "小组赛")
        elif stage == 1:
            match.get_match(browser, year, "世界杯", "16强")
        elif stage == 2:
            match.get_match(browser, year, "世界杯", "8强")
        elif stage == 3:
            match.get_match(browser, year, "世界杯", "4强")
        elif stage == 4:
            match.get_match(browser, year, "世界杯", "季军赛")
        elif stage == 5:
            match.get_match(browser, year, "世界杯", "决赛")


def index_year(year):
    print("正在爬取第", year, '年')
    try:
        config.match_total = 0
        url = 'http://zq.win007.com/cn/CupMatch/%s/75.html' %(year)
        browser.get(url)
        check = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#SubSelectDiv')))
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
