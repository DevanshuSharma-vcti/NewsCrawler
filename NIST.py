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
driver.get("https://www.nist.gov/news-events/news/search") #webpage url
#driver.maximize_window()

"""
click_button = driver.find_element(By.XPATH, "//a[normalize-space()='View All Press Releases']") #click on button
click_button.click()


click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
click_drop.click()
"""

Headingrows = driver.find_elements(By.XPATH, "(//div[@class='nist-teaser__content-wrapper'])")   #selects all the headings

keywords = ["internet", "wifi", "broadband", "grant",'Cool and Connected program','Reconnect program','Distance learning','rural broadband']
NRKeywords =["Climate", "climate change" , "health"]

filteredHeadings = []
filteredDates = []
matchingKeyword = []
links =[]
source =[]
def function():
    global matchingKeyword
    count = 1
    for div_row in Headingrows:
        heading = div_row.find_element(By.XPATH, f"(//h3[@class='nist-teaser__title'])[{count}]").text #headingText
        headingL = div_row.find_element(By.TAG_NAME , 'a').get_attribute('href') #heading links
        get_title = driver.title #sourceOfNews
        dateExtracted = div_row.find_element(By.XPATH, f"(//div[@class='daterange'])[{count}]").text # publishing date
        count += 1
        global final_date
        d = dateExtracted.replace(",", "")
        final_date = datetime.strptime(d,'%B %d %Y') # converts Date String into datetime object
        current_datetime = datetime.now()
        if current_datetime - final_date < timedelta(weeks=2) : # can change the week according to requirement
            for k in keywords:
                required_keyword_present = False
                notrequired_keyword_present = False
                present_keywords = []
                for k in keywords:
                    if k in heading.lower():
                        required_keyword_present = True
                        present_keywords.append(k)

                        # break
                for i in NRKeywords:
                    if i in heading.lower():
                        notrequired_keyword_present = True
                        break

                if required_keyword_present and (not notrequired_keyword_present):
                    source.append(get_title)
                    links.append(headingL)
                    matchingKeyword = matchingKeyword + present_keywords
                    filteredHeadings.append(heading)
                    filteredDates.append(final_date.strftime("%m/%d/%Y"))
today = datetime.now()
function()
while today - final_date < timedelta(weeks=2):
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
df['Agency']= 'NIST'
df= df[['S.no','News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency','Date of running']]

# print(df)
df.to_csv('nist.csv', index=False)


