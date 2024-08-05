import selenium
import time
import pandas as pd
import numpy as np
import os
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import datefinder
import json

    # Set path Selenium
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
print(os.path.exists(CHROMEDRIVER_PATH))
s = Service(CHROMEDRIVER_PATH)
WINDOW_SIZE = "1920,1080"

    # Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.get("https://www.epa.gov/newsreleases/search")
driver.maximize_window()
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
links =[]
source =[]

driver.maximize_window()
driver.get("https://www.epa.gov/newsreleases/search")
# print("***function yet to enter")


matchingKeyword = []


def date_converter(d1):
    finalDates = list(datefinder.find_dates(d1))
    if finalDates:
        return finalDates[0]
    else:
        return datetime.now()
def function():
    global matchingKeyword
    # print("in function???????????????????????????????????????????????????????????????????????????????????????????")


    div_rows = driver.find_elements(By.CSS_SELECTOR, "div.usa-collection__body")
    #div_rows = driver.find_elements(By.XPATH, "(//div[@class='usa-collection__body'])")


    count = 1
    # print("printing div_rows")
    # print(div_rows)
    for div_row in div_rows:
        # print("in for loop")
        # print({count}) //h3[@class="usa-collection__heading"]
        # heading = div_row.find_element(By.CSS_SELECTOR, f"(h3.usa-collection__heading)[{count}]").text
        heading = div_row.find_element(By.XPATH, f"(//h3[@class='usa-collection__heading'])[{count}]").text

        # print(heading)
        headingL = div_row.find_element(By.TAG_NAME, 'a').get_attribute('href')
        global get_title
        get_title = driver.title
        # print(get_title)
        dateExtracted = div_row.find_element(By.XPATH, f"(//li[@class='usa-collection__meta-item'])[{count}]").text
        # print(dateExtracted)
        count += 1



        d = dateExtracted.replace(",", "")
        # print(d)
        final_date = date_converter(d)

        # d = dateExtracted.replace(",", "")
        # get_title = get_title.replace("|","")
        # final_date_value = datetime.strptime(d, '%B %d %Y')
        # print(final_date_value)

        global current_datetime
        current_datetime = datetime.now()
        if current_datetime - final_date < timedelta(weeks=20):
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
                # return final_date
    # return None

# final_date_value = function()

function()

# today = datetime.now()
# while today - final_date < timedelta(weeks=20):
#     click_button = driver.find_element(By.XPATH, "//*[@id='__next']/div/section[1]/div[3]")#goes to next page
#     click_button.click()
#     function()
# else:
#     driver.close()
# while True:
#     # click_button = driver.find_element(By.XPATH, "//a[@title='Go to next page']//*[name()='svg']")
#     # click_button = driver.find_element(By.CSS_SELECTOR, "a.pager__link--next")
#     click_button = driver.find_elements(By.XPATH,"//a[@title='Go to next page']")
#     click_button.click()
#     a = "/themes/epa_theme/images/sprite.artifact.svg#angle-right"
#     for svg in click_button:
#         if svg.get_attribute('href') == a:
#             svg.click()
#             function()
# else:
#     final_date_value = function()
#     if not(final_date_value):
#         continue
#     if today - final_date_value >= timedelta(weeks=2):
#         driver.close()
#         break



zipped = list(zip(filteredHeadings , filteredDates , matchingKeyword , links, source ))

dfone = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
RunDate= datetime.today().strftime("%m/%d/%Y")
dfone['Date of running'] = RunDate
dfone['S.no'] = range(1,len(dfone)+1)
dfone['Agency']= 'EPA'
df= dfone[['S.no','News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency','Date of running']]

print(df)
#df.to_csv(f'{source}'+ '.csv', index=False)
dfone.to_csv("epa.csv", index=False)
driver.close()

