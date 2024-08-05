import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import multiprocessing
from pathlib import Path
from selenium.webdriver.chrome.options import Options
from itertools import islice

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
s = Service(CHROMEDRIVER_PATH)
WINDOW_SIZE = "1920,1080"

# Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=s, options=chrome_options)


def FileMerger():
    df1 = pd.read_csv("epa.csv")
    df2 = pd.read_csv("USDcommerce.csv")
    df3 = pd.read_csv("broadbandMoney.csv")
    df4 = pd.read_csv("InternetForAll.csv")
    df5 = pd.read_csv("NTIA_News.csv")
    df6 = pd.read_csv("USDApr.csv")
    df7 = pd.read_csv("usdTreasury.csv")
    df8 = pd.read_csv("nist.csv")
    df9 = pd.read_csv("ncta.csv")

    full_df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9])
    unique_df = full_df.drop_duplicates(keep='first')
    # del unique_df[unique_df.columns[-1]]
    print(unique_df)
    TodaysDate = time.strftime("%d-%m-%Y")

    def state_finder(row):
        count = 1
        state_list = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                      'District of columbia', 'Florida', 'Georgia', 'Guam' 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
                      'Iowa',
                      'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
                      'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
                      'New Mexico',
                      'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
                      'Puerto Rico',
                      'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
                      'Virgin Islands', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
        for state in state_list:
            if state.lower() in row.lower():
                print(type(row.lower()))
                return state

    unique_df['News Headings Short'] = ""
    unique_df['S_no'] = np.arange(1, len(unique_df) + 1)
    # unique_df = unique_df.assign( S_no = range(len(unique_df)))
    unique_df["State"] = unique_df["News heading"].apply(state_finder)
    unique_df["State"] = unique_df["State"].fillna("Others")
    unique_df['Relevancy'] = " "
    unique_df['News Headings Short'] = unique_df['News heading'].apply(
        lambda x: x[:100] + '...more' if len(x) > 100 else x)
    unique_df = unique_df[
        ['S_no', 'Agency', 'Date of announcement', 'State', 'Date of running', 'News Headings Short', 'News heading',
         'Matching keyword', 'links', 'Relevancy']]
    # unique_df.to_csv('NewsHeadings'+f'{TodaysDate}'+'.csv', index=False)

    print(unique_df)
    #path = '/home/vcti/Devanshu/FederalNewsHeadings.csv'  # give the path of the newsHeadings.csv
    path = '/home/vcti/kiran/NewsCrawller/FederalNewsHeadingsX.csv'  # give the path of the newsHeadings.csv
    obj = Path(path)
    if obj.exists():
        df = pd.read_csv("FederalNewsHeadingsX.csv")
        # news = df.(unique_df,ignore_index = False)
        news = pd.concat([df, unique_df], ignore_index=True)
        print(news)
        # news.to_csv("duplicates.csv")
        # print(dff.columns) full_df.drop_duplicates(keep='first')
        # news = pd.merge(df, unique_df, on='column_name')
        news = news.drop_duplicates(subset='links')
        print(news)
        news['S-no'] = np.arange(1, len(news) + 1)
        news = news[
            ['S-no', 'Agency', 'Date of announcement', 'State', 'Date of running', 'News Headings Short',
             'News heading',
             'Matching keyword', 'links', 'Relevancy']]
        news.to_csv('FederalNewsHeadingsX.csv', index=False)
        print(news.columns)
        # , mode = 'a'
    else:
        unique_df.to_csv('FederalNewsHeadingsX.csv', index=False)

def BroadbandMoney():
    # Set path Selenium
    # CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    # s = Service(CHROMEDRIVER_PATH)
    # WINDOW_SIZE = "1920,1080"
    #
    # # Options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(service=s, options=chrome_options)

    driver.get("https://www.broadband.money/blog")
    driver.maximize_window()

    click_button = driver.find_element(By.XPATH,
                                       "//div[@class='Typography_h2Desc__3043B BlogPages_viewMoreEvents__TkkAa']")
    click_button.click()
    """""
    click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
    click_drop.click()
    """""
    div_rows = driver.find_elements(By.XPATH, "(//section[@class='blog_previewPostContianer__3c3Nb'])")

    keywords = ["internet", "wifi", "broadband", "grant", 'Cool and Connected program', 'Reconnect program',
                'Distance learning', 'rural broadband']
    NRKeywords = ["Climate", "climate change", "health"]

    filteredHeadings = []
    filteredDates = []
    matchingKeyword = []
    links = []
    source = []

    def function():
        global matchingKeyword
        count = 1
        for div_row in div_rows:
            heading = div_row.find_element(By.XPATH, f"(//div[@class='blog_postContent__-KLYd'])[{count}]").text
            headingL = div_row.find_element(By.TAG_NAME, 'a').get_attribute('href')
            get_title = driver.title
            dateExtracted = div_row.find_element(By.XPATH, f"(//p[@class='Typography_pDate__1n2CG'])[{count}]").text
            count += 1
            global final_date
            d = dateExtracted.replace(",", "")
            final_date = datetime.strptime(d, '%B %d %Y')
            current_datetime = datetime.now()
            if current_datetime - final_date < timedelta(weeks=2):
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

    function()

    zipped = list(zip(filteredHeadings, filteredDates, matchingKeyword, links, source))

    df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
    RunDate = datetime.today().strftime("%m/%d/%Y")
    df['Date of running'] = RunDate
    df['S.no'] = range(1, len(df) + 1)
    df['Agency'] = 'Broadband Money'
    df = df[['S.no', 'News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency', 'Date of running']]
    print(df)
    df.to_csv('broadbandMoney.csv')
    driver.close()

def epa():
    # Set path Selenium
    # CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    # s = Service(CHROMEDRIVER_PATH)
    # WINDOW_SIZE = "1920,1080"
    #
    # # Options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get("https://www.epa.gov/newsreleases/search")
    driver.maximize_window()
    """""
    click_button = driver.find_element(By.XPATH, "//div[@class='Typography_h2Desc__3043B BlogPages_viewMoreEvents__TkkAa']")
    click_button.click()

    click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
    click_drop.click()
    """""
    div_rows = driver.find_elements(By.XPATH, "(//div[@class='usa-collection__body'])")

    keywords = ["internet", "wifi", "broadband", "grant", 'Cool and Connected program', 'Reconnect program',
                'Distance learning', 'rural broadband']
    NRKeywords = ["Climate", "climate change", "health"]

    filteredHeadings = []
    filteredDates = []
    matchingKeyword = []
    links = []
    source = []
    driver.maximize_window()
    driver.get("https://www.epa.gov/newsreleases/search")

    def function():
        global matchingKeyword
        div_rows = driver.find_elements(By.XPATH, "(//div[@class='usa-collection__body'])")
        count = 1
        for div_row in div_rows:
            heading = div_row.find_element(By.XPATH, f"(//h3[@class ='usa-collection__heading'])[{count}]").text
            headingL = div_row.find_element(By.TAG_NAME, 'a').get_attribute('href')
            global get_title
            get_title = driver.title
            dateExtracted = div_row.find_element(By.XPATH, f"(//li//div//ul//li//time)[{count}]").text
            count += 1
            global final_date
            d = dateExtracted.replace(",", "")
            get_title = get_title.replace("|", "")
            final_date = datetime.strptime(d, '%B %d %Y')

            global current_datetime
            current_datetime = datetime.now()
            if current_datetime - final_date < timedelta(weeks=2):
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

    function()

    today = datetime.now()
    if today - final_date < timedelta(weeks=2):
        click_button = driver.find_element(By.XPATH, "//a[@title='Go to next page']//*[name()='svg']")
        click_button.click()
        function()

    zipped = list(zip(filteredHeadings, filteredDates, matchingKeyword, links, source))

    dfone = pd.DataFrame(zipped,
                         columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
    RunDate = datetime.today().strftime("%m/%d/%Y")
    dfone['Date of running'] = RunDate
    dfone['S.no'] = range(1, len(dfone) + 1)
    dfone['Agency'] = 'EPA'
    df = dfone[
        ['S.no', 'News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency', 'Date of running']]

    print(df)
    # df.to_csv(f'{source}'+ '.csv', index=False)
    dfone.to_csv("epa.csv", index=False)
    driver.close()


def InternetForAll():
    # Set path Selenium
    # CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    # s = Service(CHROMEDRIVER_PATH)
    # WINDOW_SIZE = "1920,1080"
    #
    # # Options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get("https://www.internet4all.gov/news-and-media")  # webpage url
    # driver.maximize_window()

    click_button = driver.find_element(By.XPATH, "//a[normalize-space()='View All Press Releases']")  # click on button
    click_button.click()

    """
    click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
    click_drop.click()
    """

    keywords = ["internet", "wifi", "broadband", "grant", 'Cool and Connected program', 'Reconnect program',
                'Distance learning', 'rural broadband']
    NRKeywords = ["Climate", "climate change", "health"]

    filteredHeadings = []
    filteredDates = []
    matchingKeyword = []
    links = []
    source = []

    def function():
        global matchingKeyword
        Headingrows = driver.find_elements(By.CLASS_NAME, "views-row")  # selects all the headings
        count = 1
        for div_row in Headingrows:
            heading = div_row.find_element(By.XPATH, f"(//div[@class='headline-banner'])[{count}]").text  # headingText
            headingL = div_row.find_element(By.TAG_NAME, "a").get_attribute('href')  # heading links
            get_title = driver.title  # sourceOfNews
            dateExtracted = div_row.find_element(By.XPATH,
                                                 f"(//div[@class='date-type'])[{count}]").text  # publishing date
            count += 1
            global final_date
            d = dateExtracted.replace(",", "")
            final_date = datetime.strptime(d, '%B %d %Y')  # converts Date String into datetime object
            current_datetime = datetime.now()
            if current_datetime - final_date < timedelta(weeks=15):  # can change the week according to requirement
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
    while today - final_date < timedelta(weeks=15):
        click_button = driver.find_element(By.XPATH, "//span[normalize-space()='Next']")  # goes to next page
        click_button.click()
        function()
    else:
        driver.close()

    zipped = list(zip(filteredHeadings, filteredDates, matchingKeyword, links, source))

    df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
    RunDate = datetime.today().strftime("%m/%d/%Y")
    df['Date of running'] = RunDate
    df['S.no'] = range(1, len(df) + 1)
    df['Agency'] = 'Internet for All'
    df = df[['S.no', 'News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency', 'Date of running']]
    print(df)
    df.to_csv('InternetForAll.csv', index=False)


def ncta():
    # Set path Selenium
    # CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    # s = Service(CHROMEDRIVER_PATH)
    # WINDOW_SIZE = "1920,1080"
    #
    # # Options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(service=s, options=chrome_options)
    # driver.get("https://www.epa.gov/newsreleases/search")
    # driver.maximize_window()
    """""
    click_button = driver.find_element(By.XPATH, "//div[@class='Typography_h2Desc__3043B BlogPages_viewMoreEvents__TkkAa']")
    click_button.click()

    click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
    click_drop.click()
    """""
    div_rows = driver.find_elements(By.XPATH, "(//div[@class='usa-collection__body'])")

    keywords = ["internet", "wifi", "broadband", "grant", 'Cool and Connected program', 'Reconnect program',
                'Distance learning', 'rural broadband']
    NRKeywords = ["Climate", "climate change", "health"]

    filteredHeadings = []
    filteredDates = []
    matchingKeyword = []
    links = []
    source = []
    driver.maximize_window()
    driver.get("https://www.ncta.com/whats-new")

    def function():
        global matchingKeyword

        div_rows = driver.find_elements(By.XPATH, "(//div[@class='story-item__content-wrap'])")
        count = 1
        for div_row in div_rows:
            # heading = div_row.find_element(By.XPATH, f"(//h3[@class ='usa-collection__heading'])[{count}]").text
            heading = div_row.find_element(By.TAG_NAME, 'a').text
            headingL = div_row.find_element(By.TAG_NAME, 'a').get_attribute('href')
            get_title = driver.title
            dateExtracted = div_row.find_element(By.XPATH, f"(//div[@class='story-item__date'])[{count}]").text
            count += 1
            global final_date
            d = dateExtracted.replace(",", "")
            final_date = datetime.strptime(d, '%B %d %Y')
            get_title = get_title.replace("—", "-")
            global current_datetime
            current_datetime = datetime.now()
            if current_datetime - final_date < timedelta(weeks=2):
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
        click_button = driver.find_element(By.XPATH, "//span[contains(text(),'››')]")  # goes to next page
        click_button.click()
        function()
    else:
        driver.close()

    zipped = list(zip(filteredHeadings, filteredDates, matchingKeyword, links, source))

    df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
    RunDate = datetime.today().strftime("%m/%d/%Y")
    print(type(RunDate))
    print(RunDate)
    df['Date of running'] = RunDate
    df['Agency'] = 'NCTA'
    df['S.no'] = range(1, len(df) + 1)
    df = df[['S.no', 'News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency', 'Date of running']]
    print(df)
    df.to_csv('ncta.csv', index=False)
    # driver.close()

def nist():
    # Set path Selenium
    # CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    # s = Service(CHROMEDRIVER_PATH)
    # WINDOW_SIZE = "1920,1080"
    #
    # # Options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get("https://www.nist.gov/news-events/news/search")  # webpage url
    # driver.maximize_window()

    """
    click_button = driver.find_element(By.XPATH, "//a[normalize-space()='View All Press Releases']") #click on button
    click_button.click()


    click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
    click_drop.click()
    """

    Headingrows = driver.find_elements(By.XPATH,
                                       "(//div[@class='nist-teaser__content-wrapper'])")  # selects all the headings

    keywords = ["internet", "wifi", "broadband", "grant", 'Cool and Connected program', 'Reconnect program',
                'Distance learning', 'rural broadband']
    NRKeywords = ["Climate", "climate change", "health"]

    filteredHeadings = []
    filteredDates = []
    matchingKeyword = []
    links = []
    source = []

    def function():
        global matchingKeyword
        count = 1
        for div_row in Headingrows:
            heading = div_row.find_element(By.XPATH,
                                           f"(//h3[@class='nist-teaser__title'])[{count}]").text  # headingText
            headingL = div_row.find_element(By.TAG_NAME, 'a').get_attribute('href')  # heading links
            get_title = driver.title  # sourceOfNews
            dateExtracted = div_row.find_element(By.XPATH,
                                                 f"(//div[@class='daterange'])[{count}]").text  # publishing date
            count += 1
            global final_date
            d = dateExtracted.replace(",", "")
            final_date = datetime.strptime(d, '%B %d %Y')  # converts Date String into datetime object
            current_datetime = datetime.now()
            if current_datetime - final_date < timedelta(weeks=2):  # can change the week according to requirement
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
        click_button = driver.find_element(By.XPATH, "//span[normalize-space()='Next']")  # goes to next page
        click_button.click()
        function()
    else:
        driver.close()

    zipped = list(zip(filteredHeadings, filteredDates, matchingKeyword, links, source))
    df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
    RunDate = datetime.today().strftime("%m/%d/%Y")
    df['Date of running'] = RunDate
    df['S.no'] = range(1, len(df) + 1)
    df['Agency'] = 'NIST'
    df = df[['S.no', 'News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency', 'Date of running']]

    print(df)
    df.to_csv('nist.csv', index=False)


def ntia():
    # Set path Selenium
    # CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    # s = Service(CHROMEDRIVER_PATH)
    # WINDOW_SIZE = "1920,1080"
    #
    # # Options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(service=s, options=chrome_options)
    """""
    click_button = driver.find_element(By.XPATH, "//span[normalize-space()='News']")
    click_button.click()

    click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
    click_drop.click()
    """""

    keywords = ["internet", "wifi", "broadband", "grant", 'Cool and Connected program', 'Reconnect program',
                'Distance learning', 'rural broadband']
    NRKeywords = ["Climate", "climate change", "health"]

    filteredHeadings = []
    filteredDates = []
    matchingKeyword = []
    links = []
    source = []
    driver.get("https://ntia.gov/newsroom?type=press_releases&tid=All&page=0")

    def function():
        global matchingKeyword

        driver.maximize_window()
        div_rows = driver.find_elements(By.XPATH, "(//div[@class='views-row'])")
        count = 1
        for div_row in div_rows:
            # heading = div_row.find_element(By.XPATH, f"(//h2[@class='field-content'])[{count}]").text
            heading = div_row.find_element(By.TAG_NAME, 'a').text

            headingL = div_row.find_element(By.TAG_NAME, 'a').get_attribute('href')

            get_title = driver.title
            dateExtracted = div_row.find_element(By.XPATH,
                                                 f"(//span[@class='views-created-dot-type--created'])[{count}]").text
            count += 1

            d = dateExtracted.replace(",", "")
            global final_date
            final_date = datetime.strptime(d, '%B %d %Y')
            current_datetime = datetime.now()
            if current_datetime - final_date < timedelta(weeks=15):
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

    function()

    today = datetime.now()
    if today - final_date < timedelta(weeks=15):
        click_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next ›')]")
        click_button.click()
        function()

    zipped = list(zip(filteredHeadings, filteredDates, matchingKeyword, links, source))

    df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
    RunDate = datetime.today().strftime("%m/%d/%Y")
    df['Date of running'] = RunDate
    df['S.no'] = range(1, len(df) + 1)
    df['Agency'] = 'NTIA'
    df = df[['S.no', 'News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency', 'Date of running']]

    print(df)
    df.to_csv('NTIA_News.csv')
    driver.close()

def usdAPr():
    # Set path Selenium
    # CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    # s = Service(CHROMEDRIVER_PATH)
    # WINDOW_SIZE = "1920,1080"
    #
    # # Options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(service=s, options=chrome_options)
    # driver.get("https://www.nist.gov/news-events/news/search")  # webpage url
    driver.get("https://www.usda.gov/media/press-releases")  # webpage url
    # driver.maximize_window()
    driver.refresh()
    """

    click_button = driver.find_element(By.XPATH, "//span[normalize-space()='News']")
    click_button.click()

    click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
    click_drop.click()
    """

    # print(Headingrows).text
    # Headingrows = driver.find_elements(By.CSS_SELECTOR, "li.news-releases-item")   #selects all the headings

    keywords = ["internet", "wifi", "broadband", "grant", 'Cool and Connected program', 'Reconnect program',
                'Distance learning', 'rural broadband']
    NRKeywords = ["Climate", "climate change", "health"]

    filteredHeadings = []
    filteredDates = []
    matchingKeyword = []
    links = []
    source = []

    def function():
        global matchingKeyword
        Headingrows = driver.find_elements(By.XPATH, "(//li[@class='news-releases-item'])")  # selects all the headings

        count = 1
        for div_row in Headingrows:
            heading = div_row.find_element(By.TAG_NAME, 'a').text  # headingText
            # heading = div_row.find_element(By.XPATH, f"(//a[@id])[{count}]").text  # headingText
            headingL = div_row.find_element(By.TAG_NAME, 'a').get_attribute('href')  # heading links
            get_title = driver.title  # sourceOfNews
            dateExtracted = div_row.find_element(By.XPATH,
                                                 f"(//div[@class='news-release-date'])[{count}]").text  # publishing date
            count += 1
            global final_date
            d = dateExtracted.replace(",", "")
            final_date = dt.strptime(d, '%b %d %Y')  # converts Date String into datetime object
            current_da = dt.now()
            if current_da - final_date < timedelta(weeks=2):  # can change the week according to requirement
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

    today = dt.now()
    function()

    while today - final_date < timedelta(weeks=2):
        click_button = driver.find_element(By.XPATH, "//span[normalize-space()='Next']")  # goes to next page
        click_button.click()
        function()
    else:
        driver.close()

    zipped = list(zip(filteredHeadings, filteredDates, matchingKeyword, links, source))

    df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
    df['Date of running'] = today
    df['S.no'] = range(1, len(df) + 1)
    df['Agency'] = 'USDA'
    df = df[['S.no', 'News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency', 'Date of running']]
    print(df)
    df.to_csv('USDApr.csv', index=False)


def usdCom():
    # Set path Selenium
    # CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    # s = Service(CHROMEDRIVER_PATH)
    # WINDOW_SIZE = "1920,1080"
    #
    # # Options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(service=s, options=chrome_options)
    # driver.get("https://www.nist.gov/news-events/news/search")  # webpage url)
    driver.get("https://www.commerce.gov/news/press-releases")  # webpage url
    # driver.maximize_window()

    """
    click_button = driver.find_element(By.XPATH, "//a[normalize-space()='View All Press Releases']") #click on button
    click_button.click()


    click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
    click_drop.click()
    """
    # driver.implicitly_wait(5)
    # click_button = driver.find_element(By.XPATH, "//button[normalize-space()='Close subscription dialog']")
    # click_button.click()
    # selects all the headings

    keywords = ["internet", "wifi", "broadband", "grant", 'Cool and Connected program', 'Reconnect program',
                'Distance learning', 'rural broadband']
    NRKeywords = ["Climate", "climate change", "health"]

    filteredHeadings = []
    filteredDates = []
    matchingKeyword = []
    links = []
    source = []

    def function():
        count = 1
        global matchingKeyword
        Headingrows = driver.find_elements(By.XPATH, "(//div[@class='views-row'])")
        for div_row in Headingrows:
            heading = div_row.find_element(By.TAG_NAME, 'a').text  # headingText
            headingL = div_row.find_element(By.TAG_NAME, 'a').get_attribute('href')  # heading links
            get_title = driver.title  # sourceOfNews
            dateExtracted = div_row.find_element(By.XPATH,
                                                 f"(//time[normalize-space()])[{count}]").text  # publishing date
            count += 1
            global final_date
            d = dateExtracted.replace(",", "")
            final_date = datetime.strptime(d, '%B %d %Y')  # converts Date String into datetime object
            # final_date = final_date.strftime("%m/%d/%Y")
            current_datetime = datetime.now()
            if current_datetime - final_date < timedelta(weeks=2):  # can change the week according to requirement
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
        button = driver.find_elements(By.XPATH, "//span[@class='usa-pagination__link-text']")  # goes to next page
        button[-1].click()
        time.sleep(2)
        function()
        # button = driver.find_elements(By.XPATH, "//span[@class='usa-pagination__link-text']")#goes to next page
        # for b in button.text :
        #     if b.lower() == 'next':
        #         click_button = driver.find_element(By.XPATH, "//span[@class='usa-pagination__link-text']")
        #         click_button.click()
        #         function()
        # print(button)
        # if click_button.text == "Next":
        #     click_button.click()
        #     function()
    else:
        driver.close()

    zipped = list(zip(filteredHeadings, filteredDates, matchingKeyword, links, source))
    RunDate = datetime.today().strftime("%m/%d/%Y")
    df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
    df['Date of running'] = RunDate
    df['Agency'] = 'DOC'
    df['S.no'] = range(1, len(df) + 1)
    df = df[['S.no', 'News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source', 'Agency',
             'Date of running']]

    print(df)
    df.to_csv('USDcommerce.csv', index=False)


def usdTreasury():
    # Set path Selenium
    # CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    # s = Service(CHROMEDRIVER_PATH)
    # WINDOW_SIZE = "1920,1080"
    #
    # # Options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get("https://www.nist.gov/news-events/news/search")  # webpage url
    """""
    driver.get("https://www.epa.gov/newsreleases/search")
    driver.maximize_window()

    click_button = driver.find_element(By.XPATH, "//div[@class='Typography_h2Desc__3043B BlogPages_viewMoreEvents__TkkAa']")
    click_button.click()

    click_drop = driver.find_element(By.XPATH, "//span[normalize-space()='Press Releases']")
    click_drop.click()
    """""

    keywords = ["internet", "wifi", "broadband", "grant", 'Cool and Connected program', 'Reconnect program',
                'Distance learning', 'rural broadband']
    NRKeywords = ["Climate", "climate change", "health"]

    filteredHeadings = []
    filteredDates = []
    matchingKeyword = []
    links = []
    source = []

    driver.get("https://home.treasury.gov/news/press-releases")
    driver.maximize_window()

    def function():
        global matchingKeyword
        div_rows = driver.find_elements(By.XPATH, "(//div[@class='usa-collection__body'])")

        div_rows = driver.find_elements(By.XPATH, "(//h3[@class='featured-stories__headline'])")
        count = 1
        for div_row in div_rows:
            # heading = div_row.find_element(By.XPATH, f"(//h3[@class ='usa-collection__heading'])[{count}]").text
            heading = div_row.find_element(By.TAG_NAME, 'a').text
            headingL = div_row.find_element(By.TAG_NAME, 'a').get_attribute('href')
            get_title = driver.title
            dateExtracted = div_row.find_element(By.XPATH, f"(//span[@class='date-format'])[{count}]").text
            count += 1
            global final_date
            d = dateExtracted.replace(",", "")
            final_date = datetime.strptime(d, '%B %d %Y')

            global current_datetime
            current_datetime = datetime.now()
            if current_datetime - final_date < timedelta(weeks=2):
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
    today = datetime.now()
    if today - final_date < timedelta(weeks=2):
        click_button = driver.find_element(By.XPATH, "//img[@alt='Right arrow']")
        click_button.click()
        function()

    zipped = list(zip(filteredHeadings, filteredDates, matchingKeyword, links, source))

    df = pd.DataFrame(zipped, columns=['News heading', 'Date of announcement', 'Matching keyword', 'links', 'Source'])
    RunDate = datetime.today().strftime("%m/%d/%Y")
    df['Date of running'] = RunDate
    df['S.no'] = range(1, len(df) + 1)
    df['Agency'] = 'DOC'
    df = df[['S.no', 'News heading', 'Date of announcement', 'Matching keyword', 'links', 'Agency', 'Date of running']]
    print(df)
    df.to_csv('usdTreasury.csv', index=False)
    driver.close()


# if __name__ == '__main__':
#     processes = [
#         multiprocessing.Process(target=BroadbandMoney()),
#         multiprocessing.Process(target=epa()),
#         multiprocessing.Process(target=InternetForAll()),
#         multiprocessing.Process(target=ncta()),
#         multiprocessing.Process(target=nist()),
#         multiprocessing.Process(target=ntia()),
#         multiprocessing.Process(target=usdAPr()),
#         multiprocessing.Process(target=usdCom()),
#         multiprocessing.Process(target=usdTreasury())
#     ]
#
#     for process in processes:
#         process.start()
#
#     for process in processes:
#         process.join()
if __name__ == '__main__':
    processes = [
        multiprocessing.Process(target=BroadbandMoney()),
        #multiprocessing.Process(target=epa()),
        #multiprocessing.Process(target=InternetForAll()),
        #multiprocessing.Process(target=ncta()),
        #multiprocessing.Process(target=nist()),
        #multiprocessing.Process(target=ntia()),
        #multiprocessing.Process(target=usdAPr()),
        multiprocessing.Process(target=usdCom()),
        multiprocessing.Process(target=usdTreasury())
    ]

    batch_size = 1  # Number of processes to run concurrently

    for i in range(0, len(processes), batch_size):
        batch = processes[i:i+batch_size]
        for process in batch:
            process.start()

        for process in batch:
            process.join()

FileMerger()