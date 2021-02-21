from contextlib import contextmanager
from functools import lru_cache
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

import fire

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import os
import json
import re

@lru_cache
def get_driver():
    #try:
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    return driver
    #finally:
        #driver.quit()

def get_data_from_url(url):

    # URL Validation
    logger.info(f"url: {url}")

    if "nbatopshot" not in url:
        logger.info("invalid url")
        return None

    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, url) is None:
        logger.info("invalid url")
        return None

    moment = {}

    driver = get_driver()
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    # PRICES
    results = soup.find('script', {'id': '__NEXT_DATA__'})
    lists = json.loads(results.string)
    props = lists['props']['pageProps']['moment']
    moment['min'] = float(props['priceRange']['min'])
    moment['max'] = float(props['priceRange']['max'])

    # PLAYER
    moment['player'] = soup.find('h1', {'class': 'Heading__H2-kksint-1 gcacpp'}).text
    moment['action'] = soup.find('h2', {'class': 'Text-sc-179eaht-0 kBJFOy'}).text

    # COUNTS
    moment['num'] = int(soup.find('span', {'class': 'Heading__H3-kksint-2 iZrhpZ'}).text)
    collectorsDiv = soup.find('div', {'class': 'UserStockAndSeller__StyledRoot-sc-1sq21bh-0 jZrKdp'})
    moment['numCollectors'] = int(collectorsDiv.find('span', {'class': 'Text-sc-179eaht-0 UserStockAndSeller__StyledText-sc-1sq21bh-4 btAjbQ'}).text.split()[0])
    moment['numSale'] = int(collectorsDiv.find('span', {'class': 'Heading__H4-kksint-3 UserStockAndSeller__Count-sc-1sq21bh-1 hQzWLl hCJKtG'}).text)

    # AGE
    d = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May': 5, 'June':6, 'July':7, 'Aug':8, 'Sep': 9, 'Oct':10, 'Nov':11, 'Dec':12}
    dates = soup.find('span', {'class':'Label-sc-1c0wex9-0 iphjix'}).text.split()
    date = datetime.date(int(dates[2]), d.get(dates[0]), int(dates[1]))
    today = date.today()
    moment['cardAge'] = (today - date).days

    # SCORES
    playerGameScoresTable = soup.find('table', {'id':'playerGameScores'})
    playerGameScores = playerGameScoresTable.find_all('td', {'class': 'Label-sc-1c0wex9-0 Tablestyles__Cell-xih7iu-0 ebXDLw fNBBpY'})
    moment['plusMinusGame'] = float(playerGameScores[-1].text)

    playerSeasonAverageScoresTable = soup.find('table', {'id':'playerSeasonAverageScores'})
    playerSeasonAverageScores = playerSeasonAverageScoresTable.find_all('td', {'class':'Label-sc-1c0wex9-0 Tablestyles__Cell-xih7iu-0 ebXDLw fNBBpY'})
    moment['plusMinusSeason'] = float(playerSeasonAverageScores[-1].text)

    driver.quit()
    return moment

def format_row(data):
    values = [data['cardAge'], data['num'], data['numCollectors'], data['plusMinusGame'], data['plusMinusSeason']]
    return values
    # return list(data.values())

def train():
    ...

@lru_cache
def load_model():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MLR_model_v1.pickle")
    from statsmodels.iolib.smpickle import load_pickle
    model = load_pickle(path)
    return model

def evaluate(url = None):
    d = get_data_from_url(url)
    inputs = format_row(d)
    model = load_model()
    res = model.predict(inputs)
    logger.info(f"prediction: {res[0]}")
    return res[0]

def main():
    fire.Fire(dict(
        evaluate=evaluate,
        train=train,
        get=get_data_from_url,
    ))

if __name__ == "__main__":
    main()
