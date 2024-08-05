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
from pathlib import Path
import json
# driver = webdriver.Firefox()

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




driver.get("https://www.broadband.money/blog")
driver.maximize_window()

# click_button = driver.find_element(By.XPATH, "//*[@id='__next']/div/section[1]/div[3]")
# print(click_button)
# click_button.click()
# print("clicked!")
"""""
click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
click_drop.click()
"""""
div_rows = driver.find_elements(By.XPATH, "(//section[@class='blog_previewPostContianer__3c3Nb'])")
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
def function():
    global matchingKeyword
    count = 1
    H_count = 1
    try:
        for div_row in div_rows:
            if count < 88:
                # try:
                #     heading = div_row.find_element(By.XPATH, f"(//h3[@class='Typography_h3PreviewPostTitleLong__2eura'])[{count}]").text
                #     print(heading)
                # except:
                #     heading = div_row.find_element(By.XPATH,f"(//h3[@class='Typography_h3PreviewPostTitle__56xLj'])[{count}]").text
                #     print(heading)
                heading = div_row.find_element(By.TAG_NAME,'h3').text
                print("Heading is: "+heading)
                headingL = div_row.find_element(By.TAG_NAME , 'a').get_attribute('href')
                print("Heading link is: "+headingL)
                get_title = driver.title
                dateExtracted = div_row.find_element(By.XPATH, f"(//p[@class='Typography_pDate__1n2CG'])[{count}]").text
                # print(dateExtracted)
                # print(count)
                count += 1
                global final_date
                d = dateExtracted.replace(",", "")
                final_date = datetime.strptime(d,'%B %d %Y')
                current_datetime = datetime.now()
                if current_datetime - final_date < timedelta(weeks=10) :
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
            else:
                break

    except Exception as err:
        print(error)
function()
# today = datetime.now()
# while today - final_date < timedelta(weeks=10):
#     print("inside date parameter......................")
#     # click_button = driver.find_element(By.XPATH, "//*[@id='__next']/div/section[1]/div[3]")#goes to next page
#     click_button = driver.find_element(By.CSS_SELECTOR, "div.Typography_h2Desc__3043B")
#     click_button.click()
#     function()
# else:
#     driver.close()

zipped = list(zip(filteredHeadings , filteredDates , matchingKeyword , links, source ))
df1 = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
RunDate= datetime.today().strftime("%m/%d/%Y")
df1['Date of running'] = RunDate

path = r'/home/vcti/kiran/NewsCrawller/broadbandMoney1.csv'  # give the path of the newsHeadings.csv
obj = Path(path)
if obj.exists():
    print("exist")

    df = pd.read_csv("broadbandMoney1.csv")
    # df['Agency'] = 'Broadband Money'
    df['S.no'] = range(1, len(df) + 1)
    # news = df.append(unique_df,ignore_index = False)
    news = pd.concat([df, df1], ignore_index=True)
    # print(news)
    # news.to_csv("duplicates.csv")
    # print(dff.columns) full_df.drop_duplicates(keep='first')
    # news = pd.merge(df, unique_df, on='column_name')
    # news = news.drop_duplicates(subset='links')
    #news = pd.concat([news, df3], ignore_index='True')
    news = news.drop_duplicates(subset='News heading')
    # print(news)
    news['S-no'] = np.arange(1, len(news) + 1)
    nees= news['Agency'] = 'Broadband Money'
    news = news[['S-no','News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency','Date of running']]
    news.to_csv('broadbandMoney.csv', index=False)
    news.to_csv('broadbandMoney1.csv', index=False)
    print(news)
    # print("BB done")
    # print(news.columns)
    # , mode = 'a'
else:

    #df['Date of running'] = RunDate
    print("in else")
    df1['S.no'] = range(1, len(df1) + 1)
    df1['Agency'] = 'Broadband Money'
    df1 = df1[['S.no', 'News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency', 'Date of running']]
    df1.to_csv('broadbandMoney1.csv', index=False)
    df1.to_csv('broadbandMoney.csv', index=False)

# df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
# RunDate= datetime.today().strftime("%m/%d/%Y")
# df['Date of running'] = RunDate
# df['S.no'] = range(1,len(df)+1)
# df['Agency']= 'Broadband Money'
# df= df[['S.no','News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency','Date of running']]
# print(df)
# df.to_csv('broadbandMoney.csv')
driver.close()

