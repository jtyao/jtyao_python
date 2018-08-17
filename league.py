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
{'league': '日职联', 'year': ['2016'], 'max_stage': 34, 'url': 'http://zq.win007.com/cn/SubLeague/%s/25.html'},
            {'league': '法甲', 'year': ['2018-2019'], 'max_stage': 38, 'url': 'http://zq.win007.com/cn/League/%s/11.html'},
            {'league': '英超', 'year': ['2018-2019'], 'max_stage': 38, 'url': 'http://zq.win007.com/cn/League/%s/36.html'},
            {'league': '西甲', 'year': ['2018-2019'], 'max_stage': 38, 'url': 'http://zq.win007.com/cn/League/%s/31.html'},
            {'league': '德甲', 'year': ['2018-2019'], 'max_stage': 34, 'url': 'http://zq.win007.com/cn/League/%s/8.html'},
            {'league': '意甲', 'year': ['2018-2019'], 'max_stage': 38, 'url': 'http://zq.win007.com/cn/League/%s/34.html'},
            {'league': '捷甲', 'year': ['2018-2019'], 'max_stage': 30, 'url': 'http://zq.win007.com/cn/League/%s/137.html'},
            {'league': '中超', 'year': ['2018'], 'max_stage': 30, 'url': 'http://zq.win007.com/cn/League/%s/60.html'},

            ]

def get_sub_stage(browser, wait, year, league, parent_stage):
    clicks = browser.find_elements(By.CSS_SELECTOR, '#showRound tr .lsm2')
    stage_count = len(clicks)
    if stage_count == 0:
        ret = match.get_match(browser, year, league['league'], parent_stage)
    else:
        for stage in range(0, stage_count):
            clicks = browser.find_elements(By.CSS_SELECTOR, '#showRound tr .lsm2')

            clicks[stage].click()
            check = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#Table3')))
            time.sleep(random.randint(3, 5))

            if parent_stage == None:
                stage_str = str(stage + 1)
            else:
                stage_str = parent_stage

            ret = match.get_match(browser, year, league['league'], stage_str)
            if ret == 'no_start':
                break
    return ret

def get_stage(browser, wait, year, league):
    clicks = browser.find_elements(By.CSS_SELECTOR, '#SubSelectDiv td[class^="cupmatch_rw2"]')
    stage_count = len(clicks)
    if stage_count == 0:
        get_sub_stage(browser, wait, year, league, None)
    else:
        for stage in range(0, stage_count):
            clicks = browser.find_elements(By.CSS_SELECTOR, '#SubSelectDiv td[class^="cupmatch_rw2"]')
            stage_str = clicks[stage].text
            clicks[stage].click()

            check = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#Table3')))
            time.sleep(random.randint(3, 5))

            ret = get_sub_stage(browser, wait, year, league, stage_str)
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
