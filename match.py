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
import time
import random
import config
import save
from lxml import etree

def get_match_info(year, league, stage, text):
    match = {
        'year': year,
        'stage': stage,
        'league': league,
    }

    match['date'] = text[1].replace("\n", " ", 1)
    match['home_name'] = text[2].lstrip('21')
    match['away_name'] = text[4].lstrip('21')
    match['score'] = text[3]
    match['half_score'] = text[10]

    return match

def get_odds(url):
    odds_browser = config.get_webdriver()
    odds_wait = WebDriverWait(odds_browser, 10)

    try:
        odds_browser.get(url)
        odds_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#sel_showType')))

        select = Select(odds_browser.find_element_by_id("sel_showType"))
        select.select_by_value('1')
        odds_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#dataList')))

        html = etree.HTML(odds_browser.page_source)
        doc = pq(html)
        td = doc('#oddstr_281 td')

        text = []
        odds = {}
        for item in td.items():
            text.append(item.text())
        odds['start'] = text[2:5]

        text = []
        end_text = []
        next = td.parent().next()
        for item in next.items():
            end_text.append(item.text())
        text = end_text[0].split()
        odds['end'] = text[0:3]

    except TimeoutException:
        get_odds(url)
    time.sleep(random.randint(3, 8))
    odds_browser.close()
    return odds

def get_over_down(url):
    odds_browser = config.get_webdriver()
    odds_wait = WebDriverWait(odds_browser, 10)

    try:
        odds_browser.get(url)
        odds_wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#odds')))

        html = etree.HTML(odds_browser.page_source)
        doc = pq(html)
        tr = doc('#odds tbody tr')

        text = []
        odds = {}
        for item in tr.items():
            for td in item.find('td').items():
                result = re.search('Bet365', td.text())
                if result:
                    bet365 = td.parent()
                    for bet365_td in bet365.find('td').items():
                        text.append(bet365_td.text())
                    break

        if len(text) < 10:
            print("大小球赔率页面错误")
            sys.exit()
        odds['start'] = text[2:5]
        odds['end'] = text[8:11]

    except TimeoutException:
        get_over_down(url)
    time.sleep(random.randint(3, 8))
    odds_browser.close()
    return odds

def get_match(page, year, league, stage):
    html = etree.HTML(page.page_source)
    doc = pq(html)
    has_odds = False
    has_OD = False

    items = doc('#Table3 tr a').parent().parent()

    for item in items.items():
        text = []
        tds = item.find('td')
        a = tds.find('a')
        for td in tds.items():
            text.append(td.text())

        if len(text) == 11:
            match = get_match_info(year, league, stage, text)

            for item in a.items():
                url = item.attr('href')

                result = re.search('oddslist', url)
                if result:
                    has_odds = True
                    odds = []
                    odds = get_odds(url)
                    match['odds'] = odds

                result = re.search('OverDown', url)
                if result:
                    has_OD = True
                    over_down = get_over_down(url)
                    match['over_down'] = over_down

            if match:
                print(match)
                save.save_match(match)
        elif len(text) != 0:
            print("比赛数据错误")
            sys.exit()
    return match
