import selenium
import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json


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

"""""
click_button = driver.find_element(By.XPATH, "//span[normalize-space()='News']")
click_button.click()

click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
click_drop.click()
"""""

file_path = "/home/vcti/kiran/Keywords/KW_Updated.json"

try:
    print("in try")
    with open(file_path, "r") as jsonfile:
        KW_data = json.load(jsonfile)
        print("Read successful")
        print(KW_data)
except FileNotFoundError:
    print(f"File not found at path: {file_path}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")

keywords = (KW_data["Required Keywords"])
NRKeywords = (KW_data["Not Required Keywords"])

filteredHeadings = []
filteredDates = []
matchingKeyword = []
links =[]
source =[]
driver.get("https://ntia.gov/newsroom?type=press_releases&tid=All&page=0")
def function():
    global matchingKeyword
    driver.maximize_window()
    div_rows = driver.find_elements(By.XPATH, "(//div[@class='views-row'])")
    count = 1
    for div_row in div_rows:
    #heading = div_row.find_element(By.XPATH, f"(//h2[@class='field-content'])[{count}]").text
        heading = div_row.find_element(By.TAG_NAME,'a').text
        print(heading)
        headingL = div_row.find_element(By.TAG_NAME, 'a').get_attribute('href')
        get_title = driver.title
        dateExtracted = div_row.find_element(By.XPATH, f"(//span[@class='views-created-dot-type--created'])[{count}]").text
        count += 1

        d = dateExtracted.replace(",", "")
        global final_date
        final_date = datetime.strptime(d, '%B %d %Y')
        current_datetime = datetime.now()
        if current_datetime - final_date < timedelta(weeks=7):
            required_keyword_present = False
            notrequired_keyword_present = False
            present_keywords = []
            for k in keywords:
                if k in heading.lower():
                    required_keyword_present =True
                    present_keywords.append(k)
                    print("kw present in --",k)

                    # break
            for i in NRKeywords:
                if i in heading.lower():
                    notrequired_keyword_present = True
                    break

            if required_keyword_present and (not notrequired_keyword_present):
                source.append(get_title)
                links.append(headingL)
                matchingKeyword = matchingKeyword+present_keywords
                filteredHeadings.append(heading)
                print("filtered headings are =",heading)
                filteredDates.append(final_date.strftime("%m/%d/%Y"))






function()

today = datetime.now()
if today - final_date < timedelta(weeks=2):
    click_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next ›')]")
    click_button.click()
    function()

zipped = list(zip(filteredHeadings , filteredDates , matchingKeyword , links, source ))

df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
RunDate= datetime.today().strftime("%m/%d/%Y")
df['Date of running'] = RunDate
df['S.no'] = range(1,len(df)+1)
df['Agency']= 'NTIA'
df= df[['S.no','News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency','Date of running']]

print(df)
df.to_csv('NTIA_News.csv')
driver.close()

