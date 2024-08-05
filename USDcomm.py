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
driver.get("https://www.commerce.gov/news/press-releases") #webpage url
#driver.maximize_window()

"""
click_button = driver.find_element(By.XPATH, "//a[normalize-space()='View All Press Releases']") #click on button
click_button.click()


click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
click_drop.click()
"""
# driver.implicitly_wait(5)
# click_button = driver.find_element(By.XPATH, "//button[normalize-space()='Close subscription dialog']")
# click_button.click()
  #selects all the headings
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

click_button = driver.find_element(By.XPATH, "//*[@id='prefix-overlay-header']/button") #click on button
time.sleep(3)
click_button.click()


filteredHeadings = []
filteredDates = []
matchingKeyword = []
links =[]
source =[]
def function():
    count = 1
    global matchingKeyword
    Headingrows = driver.find_elements(By.XPATH, "(//div[@class='views-row'])")
    for div_row in Headingrows:
        heading = div_row.find_element(By.TAG_NAME , 'a').text #headingText
        headingL = div_row.find_element(By.TAG_NAME , 'a').get_attribute('href') #heading links
        get_title = driver.title #sourceOfNews
        dateExtracted = div_row.find_element(By.XPATH, f"(//time[normalize-space()])[{count}]").text # publishing date
        count += 1
        global final_date
        d = dateExtracted.replace(",", "")
        final_date = datetime.strptime(d,'%B %d %Y') # converts Date String into datetime object
        #final_date = final_date.strftime("%m/%d/%Y")
        current_datetime = datetime.now()
        if current_datetime - final_date < timedelta(weeks=2) : # can change the week according to requirement
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

    button = driver.find_elements(By.XPATH, "//span[@class='usa-pagination__link-text']")  # goes to next page
    time.sleep(2)
    button[-1].click()
    time.sleep(2)
    function()
    # button = driver.find_elements(By.XPATH, "//span[@class='usa-pagination__link-text']")#goes to next page
    # for b in button.text :
    #     if b.lower() == 'next':
    #         click_button = driver.find_element(By.XPATH, "//span[@class='usa-pagination__link-text']")
    #         click_button.click()
    #         function()
    #print(button)
    # if click_button.text == "Next":
    #     click_button.click()
    #     function()
else:
    driver.close()

zipped = list(zip(filteredHeadings , filteredDates , matchingKeyword , links, source ))
RunDate= datetime.today().strftime("%m/%d/%Y")
df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
df['Date of running'] = RunDate
df['Agency']= 'DOC'
df['S.no'] = range(1,len(df)+1)
df= df[['S.no','News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source','Agency','Date of running']]

# print(df)
df.to_csv('USDcommerce.csv', index=False)


