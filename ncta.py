from builtins import print

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
# driver.get("https://www.epa.gov/newsreleases/search")
# driver.maximize_window()
"""""
click_button = driver.find_element(By.XPATH, "//div[@class='Typography_h2Desc__3043B BlogPages_viewMoreEvents__TkkAa']")
click_button.click()

click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
click_drop.click()
"""""
div_rows = driver.find_elements(By.XPATH, "(//div[@class='usa-collection__body'])")
file_path = "/home/vcti/kiran/Keywords/KW_Updated.json"

try:
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
driver.maximize_window()
driver.get("https://www.ncta.com/whats-new")
def function():
    global matchingKeyword



    div_rows = driver.find_elements(By.XPATH, "(//div[@class='story-item__content-wrap'])")
    count = 1
    for div_row in div_rows:
        #heading = div_row.find_element(By.XPATH, f"(//h3[@class ='usa-collection__heading'])[{count}]").text
        heading = div_row.find_element(By.TAG_NAME, 'a').text
        headingL = div_row.find_element(By.TAG_NAME, 'a').get_attribute('href')
        get_title = driver.title
        dateExtracted = div_row.find_element(By.XPATH, f"(//div[@class='story-item__date'])[{count}]").text
        count += 1
        global final_date
        d = dateExtracted.replace(",", "")
        # print("***d***")
        # print(d)
        # print("****")
        final_date = datetime.strptime(d, '%B %d %Y')
        # print("final date - ")
        # print(final_date)
        get_title= get_title.replace("—","-")
        global current_datetime
        current_datetime = datetime.now()
        if current_datetime - final_date < timedelta(weeks=2):
            required_keyword_present = False
            notrequired_keyword_present = False
            present_keywords = []
            for k in keywords:
                if k in heading.lower():
                    required_keyword_present =True
                    present_keywords.append(k)

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
                filteredDates.append(final_date.strftime("%m/%d/%Y"))
today = datetime.now()
function()


while today - final_date < timedelta(weeks=2):
    click_button = driver.find_element(By.XPATH, "//span[contains(text(),'››')]")#goes to next page
    click_button.click()
    function()
else:
    driver.close()




zipped = list(zip(filteredHeadings , filteredDates , matchingKeyword , links, source ))

df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
RunDate= datetime.today().strftime("%m/%d/%Y")
# print(type(RunDate))
# print(RunDate)
df['Date of running'] = RunDate
df['Agency']= 'NCTA'
df['S.no'] = range(1,len(df)+1)
df= df[['S.no','News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency','Date of running']]
# print(df)
df.to_csv('ncta.csv', index=False)
#driver.close()

