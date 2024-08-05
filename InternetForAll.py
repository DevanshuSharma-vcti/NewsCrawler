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
import json #


    # Set path Selenium
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
s = Service(CHROMEDRIVER_PATH)
WINDOW_SIZE = "1920,1080"

    # Opti ons
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.get("https://www.internet4all.gov/news-and-media") #webpage url
#driver.maximize_window()


click_button = driver.find_element(By.XPATH, "//a[normalize-space()='View All Press Releases']") #click on button
click_button.click()

"""
click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
click_drop.click()
"""
file_path = "/home/vcti/kiran/Keywords/KW_Updated.json"

try:
    with open(file_path, "r") as jsonfile:
        KW_data = json.load(jsonfile)
        print("Read successful")
        # print(KW_data)
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

def function():
    global matchingKeyword
    Headingrows = driver.find_elements(By.CLASS_NAME,"views-row")
    count = 1
    for div_row in Headingrows:
        heading = div_row.find_element(By.XPATH, f"(//div[@class='headline-banner'])[{count}]").text #headingText
        print(heading)
        headingL = div_row.find_element(By.TAG_NAME , 'a').get_attribute('href') #heading links
        get_title = driver.title #sourceOfNews
        dateExtracted = div_row.find_element(By.XPATH, f"(//div[@class='date-type'])[{count}]").text # publishing date
        count += 1
        global final_date
        d = dateExtracted.replace(",", "")
        final_date = datetime.strptime(d,'%B %d %Y') # converts Date String into datetime object
        current_datetime = datetime.now()
        # print("Date diff :",current_datetime - final_date)
        if current_datetime - final_date < timedelta(weeks=2) : # can change the week according to requirement
            # print("First if 111111111111111111111111111111")
            required_keyword_present = False
            notrequired_keyword_present = False
            present_keywords = []
            for k in keywords:
                # print (k)
                if k.lower() in heading.lower():
                    print("K in lowered heading//////")
                    print("lower heading is :",heading.lower())
                    required_keyword_present =True
                    present_keywords.append(k)

                    # break
            for i in NRKeywords:
                if i in heading.lower():
                    print("Not requiredkeyword is also present")
                    print("Not required keyword is---->",i)
                    notrequired_keyword_present = True
                    break

            if required_keyword_present and (not notrequired_keyword_present):
                source.append(get_title)
                links.append(headingL)
                print("doing filtration")
                matchingKeyword = matchingKeyword+present_keywords
                filteredHeadings.append(heading)
                print("Filtered Headings are :",filteredHeadings)
                filteredDates.append(final_date.strftime("%m/%d/%Y"))


today = datetime.now()
function()
while today - final_date < timedelta(weeks=2):
    time.sleep(10)
    click_button = driver.find_element(By.XPATH, "//span[normalize-space()='Next']")#goes to next page
    click_button.click()
    function()
else:
    driver.close()

zipped = list(zip(filteredHeadings , filteredDates , matchingKeyword , links, source ))

df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
RunDate= datetime.today().strftime("%m/%d/%Y")
df['Date of running'] = RunDate
df['S.no'] = range(1,len(df)+1)
df['Agency']= 'Internet for All'
df= df[['S.no','News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency','Date of running']]
# print(df)
df.to_csv('InternetForAll.csv', index=False)


