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
# final_date = None
    # Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.get("https://www.epa.gov/newsreleases/search") #webpage url
#driver.maximize_window()




"""
click_button = driver.find_element(By.XPATH, "//a[normalize-space()='View All Press Releases']") #click on button
click_button.click()
click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
click_drop.click()
"""



keywords = ["internet", "wifi", "broadband", "grant",'Cool and Connected program','Reconnect program','Distance learning','rural broadband']
NRKeywords =["Climate", "climate change" , "health"]

filteredHeadings = []
filteredDates = []
matchingKeyword = []
links = []
source = []


def functionnm(r):
    print(r)
    global matchingKeyword
    # div_rows = driver.find_elements(By.XPATH, "(//li[@class =usa-collection__body])")
    div_rows =driver.find_elements(By.CSS_SELECTOR,"div.usa-collection__body")
    a =[div_rows]
    print("before loop print",a)
    count = 1
    global final_date
    for div_row in div_rows:
        print(f"div_row {div_row}")
        heading = div_row.find_element(By.XPATH, f"(//h3[@class ='usa-collection__heading'])[{count}]").text #headingText
        headingL = div_row.find_element(By.TAG_NAME, 'a').get_attribute('href') #heading links
        get_title = driver.title #sourceOfNews
        dateExtracted = div_row.find_element(By.XPATH, f"(//li//div//ul//li//time)[{count}]").text # publishing date

        count += 1
        print(count)

        d = dateExtracted.replace(",", "")
        final_date = datetime.strptime(d,'%B %d %Y') # converts Date String into datetime object
        print(f"final_date 1 {final_date}")
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
                print("final date is------------------------------------------------------->",final_date)
                return final_date
functionnm("p")
# final_date = function()
# print(f"final_date {final_date}")
# today = datetime.now()

# while today - final_date < timedelta(weeks=2):
#     click_button = driver.find_element(By.XPATH, "//span[normalize-space()='Next']")#goes to next page
#     click_button.click()
#     function()
# else:
#     driver.close()

zipped = list(zip(filteredHeadings , filteredDates , matchingKeyword , links, source ))

df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
RunDate= datetime.today().strftime("%m/%d/%Y")
df['Date of running'] = RunDate
df['S.no'] = range(1,len(df)+1)
df['Agency']= 'Internet for All'
df= df[['S.no','News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency','Date of running']]
# print(df)
df.to_csv('Epa.csv', index=False)


