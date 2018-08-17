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

leagues = [
            {'league': '法甲', 'year': ['2018-2019'], 'max_stage': 38, 'url': 'http://zq.win007.com/cn/League/%s/11.html'},
            {'league': '英超', 'year': ['2018-2019'], 'max_stage': 38, 'url': 'http://zq.win007.com/cn/League/%s/36.html'},
            {'league': '中超', 'year': ['2018'], 'max_stage': 30, 'url': 'http://zq.win007.com/cn/League/%s/60.html'},
            {'league': '日职联', 'year': ['2018'], 'max_stage': 34, 'url': 'http://zq.win007.com/cn/SubLeague/%s/25.html'},
            ]

def get_stage(browser, wait, year, league):
    for stage in range(0, league['max_stage']):
        clicks = browser.find_elements(By.CSS_SELECTOR, '#showRound tr .lsm2')

        if (len(clicks) != league['max_stage']):
            print("页面按钮个数不对" + str(len(clicks)))
            sys.exit()

        clicks[stage].click()
        check = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#Table3')))
        time.sleep(random.randint(3, 5))
        ret = match.get_match(browser, year, league['league'], str(stage + 1))
        if ret == 'no_start':
            break

def index_year(year, league):
    print("正在爬取 ", league['league'], " 第", year, '年')
    browser = config.get_webdriver()
    wait = WebDriverWait(browser, 10)

    try:
        config.match_total = 0
        url = league['url'] %(year)
        print(url)
        browser.get(url)
        check = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#Table1')))
        get_stage(browser, wait, year, league)
        browser.close()
        print("总场数：" + str(config.match_total))
    except TimeoutException:
        index_year(year)

def main():
    for league in leagues:
        for year in league['year']:
            index_year(year, league)

if __name__ == '__main__':
    main()
