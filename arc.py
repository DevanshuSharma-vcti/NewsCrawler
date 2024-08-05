import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
# from webdriver_manager.opera import OperaDriverManager
from selenium import webdriver
import chromedriver_autoinstaller
import pandas as pd
from datetime import datetime
from datetime import timedelta
import datefinder

# Set path Selenium
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
s = Service(CHROMEDRIVER_PATH)
WINDOW_SIZE = "1920,1080"

# Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=s, options=chrome_options)
# # Set path Selenium
# WINDOW_SIZE = "1920,1080"
# opt = webdriver.ChromeOptions()
# opt.add_argument("--start-maximized")
# # opt.add_argument("--headless")
# opt.add_argument("--window-size=%s" % WINDOW_SIZE)
# opt.add_argument('--no-sandbox')
# chromedriver_autoinstaller.install()
# driver = webdriver.Chrome(options=opt)


def date_converter(d1):
    finalDates = list(datefinder.find_dates(d1))
    if finalDates:
        return finalDates[0]
    else:
        return datetime.now()


global filteredHeadings
global filteredDates
global matchingKeyword
global links
global source
filteredHeadings = []
filteredDates = []
matchingKeyword = []
links = []
source = []
keywords = ["internet", "wireless", "5g", "rfp", "fcc", "Federal Communications Commission", "wifi",
                        "broadband", "grant", 'Cool and Connected program', 'Reconnect program',
                        'Distance learning', 'rural broadband']
NRKeywords = ["Climate", "climate change", "health","hunger","Fire","Thunderstorm","vehicles","wind",
              "gust","storm","fielding","softball","berth","tournament","scholarship","school","Graduate",
              "Graduation","University","hazard","logging","dead","killed","Police","Fatal","crash","investigation",
              "arrested","truck","Detectives","Pedestrian","Collision","Radar"]

driver.get("https://www.arc.gov/newsroom/")
news_blocks = driver.find_elements(By.CLASS_NAME, "teaser__content")
print(news_blocks)
count = 1
for news_block in news_blocks:
    heading = news_block.find_element(By.CLASS_NAME,"teaser__title").text
    print(heading)
    get_title = driver.title
    count += 1
    heading_link = news_block.find_element(By.TAG_NAME, "a").get_attribute("href")
    print(heading_link)
    global dateExtracted
    try:
        dateExtracted = news_block.find_element(By.CLASS_NAME, "eyebrow").text
        print(dateExtracted)
        # dateExtracted = datefinder.find_dates(dateExtracted)
        # print(dateExtracted)
    except:
        print(None)
        dateExtracted = datetime.today()
    time.sleep(5)
    required_keyword_present = False
    notrequired_keyword_present = False
    present_keywords = []
    for k in keywords:
        if k in heading.lower():
            required_keyword_present = True
            present_keywords.append(k)
            # print(required_keyword_present)

            # break
    for i in NRKeywords:
        if i in heading.lower():
            notrequired_keyword_present = True
            break

    if required_keyword_present and (not notrequired_keyword_present):
        source.append(get_title)
        links.append(heading_link)
        print(links)
        matchingKeyword = matchingKeyword + present_keywords
        filteredHeadings.append(heading)
        print(filteredHeadings)
        filteredDates.append(dateExtracted)
        print(filteredDates)
zipped = list(zip(filteredHeadings, filteredDates, matchingKeyword, links))
# print(zipped)
df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'matchingKeyword', 'links'])
RunDate = datetime.today().strftime("%m/%d/%Y")
df['News Headings Short'] = df['News heading'].apply(lambda x: x[:100] + '...more' if len(x) > 100 else x)
df['Date of running'] = RunDate
df['S.no'] = range(1, len(df) + 1)
df['Agency'] = "ARC"
df = df[['S.no', 'Agency', 'News heading', 'matchingKeyword', 'links', 'Date of announcement', 'Date of running']]
print(df)
df.to_csv('arc.csv', index=False)
driver.close()


