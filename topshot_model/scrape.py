from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import json
import requests
import time
import re
def scrape_data(url):
    # URL Validation
    if "nbatopshot" not in url: return False
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, url) is None: return False
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    moment = {}
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    # using try-except here because about 20+ out of 1000+ examples on the web are formatted differently
    # in the exception clause we're skiping those incorrectly formatted examples for now 
    try: 
        # PRICES
        results = soup.find('script', {'id': '__NEXT_DATA__'})
        lists = json.loads(results.text)
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
        d = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May': 5, 'June':6, 'Jun':6, 'July':7, 'Jul': 7, 'Aug':8, 'Sept':9, 'Sep': 9, 'Oct':10, 'Nov':11, 'Dec':12}
        dates = soup.find('span', {'class':'Label-sc-1c0wex9-0 iphjix'}).text.split()
        date = datetime.date(int(dates[2]), int(d.get(dates[0])), int(dates[1]))
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
    except (RuntimeError, TypeError, NameError, ValueError):
        return None
DRIVER_PATH = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.nbatopshot.com/search')
# scrolling down until we hit the very end of the page
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(2)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount==lenOfPage:
        match=True
c = driver.page_source
soup = BeautifulSoup(c, "html.parser")
linksDiv = soup.find('div', {'class': 'ThumbnailLayouts__ThumbnailGrid-sc-18xwycr-0 iCffwQ'})
links = linksDiv.find_all('a')
urls=[x['href'] for x in links]
source = driver.page_source
moments = list()
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
moments = []
for url in urls:
    fullURL = ('https://www.nbatopshot.com'+url)
    moment = scrape_data(fullURL)
    if not moment == None:
        moments.append(moment)
with open('data.json', 'w') as fout:
    json.dump(moments , fout)
