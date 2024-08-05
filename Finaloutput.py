import pandas as pd
import time
import numpy as np
from pathlib import Path
import smtplib
import traceback
import re
# from NordCountry import connect_nord_vpn
# from NordDiss import disconnect_nord_vpn

# connect_nord_vpn("United States")
#/////////////////////////


# Define your email and SMTP server settings
smtp_server = 'smtp.office365.com'
# smtp_server = 'smtp-mail.outlook.com'
#smtp-mail.outlook.com
smtp_port = 587
smtp_username = 'news_crawler_info@velankaniecity.onmicrosoft.com'
smtp_password = 'nEr#Ler55'
sender_email = 'news_crawler_info@velankaniecity.onmicrosoft.com'
  # Fill in your sender email address
recipient_emails = ['devanshu.sharma@vcti.io']  # List of recipient email addresses
#, 'hariKrishna.p@vcti.io', 'rakshitha.hs@vcti.io'

def send_email(subject, message, recipient_email):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        email_text = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, recipient_email, email_text)
        server.quit()
        print(f"Email sent successfully to {recipient_email}.")
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {str(e)}")

for recipient in recipient_emails:
    try:
        import broadbandMoney
    except Exception as e:
        error_message = f"Error importing script1:\n{traceback.format_exc()}"
        send_email("BroadbandMoney Script Failed", error_message, recipient)


    try:
        import USDAPr
    except Exception as e:
        error_message = f"Please check build log below for error:\n{traceback.format_exc()}"
        send_email("USDAPr Failed", error_message, recipient)


    try:
        import NTIA
    except Exception as e:
        error_message = f"Please check build log below for error:\n{traceback.format_exc()}"
        send_email("NTIA Failed", error_message, recipient)
    try:
        import InternetForAll
    except Exception as e:
        error_message = f"Please check build log below for error:\n{traceback.format_exc()}"
        send_email("InternetForAll Failed", error_message, recipient)


    try:
        import ncta
    except Exception as e:
        error_message = f"Please check build log below for error:\n{traceback.format_exc()}"
        send_email("NCTA Failed", error_message, recipient)

    try:
        import USDcomm
    except Exception as e:
        error_message = f"Please check build log below for error:\n{traceback.format_exc()}"
        send_email("USDcomm Failed", error_message, recipient)

    try:
        import epa
    except Exception as e:
        error_message = f"Please check build log below for error:\n{traceback.format_exc()}"
        send_email("EPA Failed", error_message, recipient)

    try:
        import usdTreasury
    except Exception as e:
        error_message = f"Please check build log below for error:\n{traceback.format_exc()}"
        send_email("usdTreasury Failed", error_message, recipient)







#////////////////////////

# import broadbandMoney
# #import epa
# import InternetForAll
# import ncta
# import NIST
# import USDAPr
# import USDcomm
# import usdTreasury
# import NTIA
# import arc

#df1 = pd.read_csv("epa.csv")
df2 = pd.read_csv("USDcommerce.csv")
df3 = pd.read_csv("broadbandMoney.csv")
df4 = pd.read_csv("InternetForAll.csv")
df5 = pd.read_csv("NTIA_News.csv")
df6 = pd.read_csv("USDApr.csv")
df7 = pd.read_csv("usdTreasury.csv")
df8 = pd.read_csv("nist.csv")
df9 = pd.read_csv("ncta.csv")
# df10 = pd.read_csv("nrtc.csv")

df3 = df3.drop_duplicates(subset='News heading')
full_df = pd.concat([df2, df4, df5, df6, df7, df8, df9])
unique_df = full_df.drop_duplicates(keep='first')
print(df3)
# del unique_df[unique_df.columns[-1]]
# print(unique_df)
TodaysDate = time.strftime("%d-%m-%Y")

def state_finder(row):
    count = 1
    state_list = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                 'District of Columbia', 'Florida', 'Georgia' ,'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
                 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
                 'New Mexico','New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
                 'Puerto Rico','Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
                 'Virgin Islands','Rural Areas', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming','District of Colombia','American Samoa', 'Guam', 'Northern Mariana Islands']
    found_states = []
    for state in state_list:
        if state.lower() in row.lower():
            found_states.append(state)
            #'Minority Colleges and Universities','Rural Area'
    list1 = ['Minority Colleges and Universities', ' Minority-Serving Colleges and Universities']
    found_area = []
    for other in list1:
        if other.lower() in row.lower():
            found_area.append("clg")
    list2 = ['Tribal']
    tribal_found = []
    for t in list2:
        if t.lower() in row.lower():
            tribal_found.append(t)

    if found_states:
        print(found_states)
        return found_states
        print("???????????????????????????????????????????????????????????????????????????????????????????????")


    if found_area :
        print(found_area)
        return found_area
    if tribal_found:
        print(tribal_found)
        return tribal_found
    else:
        print("nonenonenonenonenonenonenonenonenonenonenonenonenonenonenonenonenonenonenonenonenonenonenonenone")
        return None

def other_finder(row):
    count = 1
    list1 = ['Minority Colleges and Universities',' Minority-Serving Colleges and Universities']
    found_area = []
    for other in list1:
        if other.lower() in row.lower():
            found_area.append("clg")


    # return found_area if found_area else None
    # list1 = ['Minority Colleges and Universities',' Minority-Serving Colleges and Universities']
    #     found_area = []
    #     for other in list1:
    #         if other.lower() in row.lower():
    #             found_area.append("clg")
        # Otherwise, return the original value
    # return original_found_area

df3['News Headings Short'] = ""
df3['S_no'] = np.arange(1, len(df3) + 1)
# unique_df = unique_df.assign( S_no = range(len(unique_df)))
df3["State"] = df3["News heading"].apply(state_finder)
# df3["State"] = df3["State"].fillna("Article")
df3['Relevancy'] = " "
df3['News Headings Short'] = df3['News heading'].apply(lambda x: x[:100] + '...more' if len(x) > 100 else x)
df3 = df3[['S_no', 'Agency', 'Date of announcement', 'State', 'Date of running', 'News Headings Short', 'News heading','Matching keyword', 'links', 'Relevancy']]


unique_df['News Headings Short'] = ""
unique_df['S_no'] = np.arange(1, len(unique_df) + 1)
# unique_df = unique_df.assign( S_no = range(len(unique_df)))
# unique_df["State"] = unique_df["News heading"].apply(other_finder)
unique_df["State"] = unique_df["News heading"].apply(state_finder)
print("Found State or area is :",unique_df["State"])
unique_df = unique_df.explode('State').reset_index(drop=True)
word_to_replace = 'tribal'
replacement_string = 'Tribal Areas'

# Replace the word in the 'State' column (case-insensitive)
unique_df['State'] = unique_df['State'].str.replace(r'\b{}\b'.format(word_to_replace), replacement_string, regex=True, flags=re.IGNORECASE)
unique_df['Date of running'] = pd.to_datetime(unique_df['Date of running'])
unique_df['Date of running'] = unique_df['Date of running'].dt.strftime('%m/%d/%Y')
# unique_df["State"] = unique_df["State"].fillna("Article")
unique_df['Relevancy'] = " "
unique_df['News Headings Short'] = unique_df['News heading'].apply(lambda x: x[:100] + '...more' if len(x) > 100 else x)
unique_df = unique_df[
    ['S_no', 'Agency', 'Date of announcement', 'State', 'Date of running', 'News Headings Short', 'News heading',
     'Matching keyword', 'links', 'Relevancy']]

full_news = pd.concat([unique_df,df3], ignore_index=True)
full_news['Date of running'] = pd.to_datetime(full_news['Date of running'])
full_news['Date of running'] = full_news['Date of running'].dt.strftime('%m/%d/%Y')
# unique_df.to_csv('NewsHeadings'+f'{TodaysDate}'+'.csv', index=False)


fips_path = r'/home/vcti/kiran/FIPS'
obj1 = Path(fips_path)
if obj1.exists():
    fipsDF = pd.read_excel("FIPSdetails.xlsx")
    print("COLUMNS OF FIPS DATAFRAME AREEEEEEEEEEEEEEEEEEEEE::::",fipsDF.columns)



# print(unique_df)
path = r'/home/vcti/kiran/NewsCrawller/FederalNewsHeadings.xlsx'  # give the path of the newsHeadings.csv
obj = Path(path)
if obj.exists():
    # print("exist")
    df = pd.read_excel("FederalNewsHeading.xlsx")
    # news = df.append(unique_df,ignore_index = False)
    news = pd.concat([df, full_news], ignore_index=True)
    news["State"] = news["News heading"].apply(state_finder)
    news = news.explode('State').reset_index(drop=True)
    news["State"] = news["State"].fillna("Article")
    news['News heading1'] = news['News heading'].str.lower()  # Convert to lowercase
    news = news.drop_duplicates(subset='News heading1', keep='first')
    news["State"] = news["News heading"].apply(state_finder)
    # news["State"] = news["News heading"].apply(other_finder)

    news['Date of running'] = pd.to_datetime(news['Date of running'])
    news = news.sort_values(by="Date of running", ascending=True)
    news['Date of announcement'] = pd.to_datetime(news['Date of announcement'])

    # Format 'Date' to mm/dd/yyyy
    news['Date of running'] = news['Date of running'].dt.strftime('%m/%d/%Y')
    news['Date of announcement'] = news['Date of announcement'].dt.strftime('%m/%d/%Y')
    # news['Date of running'] = news['Date of running'].dt.date
    result = news.dtypes
    print(result)


    # news = news.drop_duplicates(subset='News heading')
    # print(news)
    news['S-no'] = np.arange(1, len(news) + 1)
    news = news[
        ['S-no', 'Agency', 'Date of announcement', 'State', 'Date of running', 'News Headings Short', 'News heading',
         'Matching keyword', 'links', 'Relevancy']]
    news = news.drop_duplicates(subset='News Headings Short', keep='first')
    news.to_excel("before_duplicate.xlsx")
    def duplicate_rows(news):
        rows = []
        for index, row in news.iterrows():
            states = row['State']
            if isinstance(states, list):
                for state in states:
                    new_row = row.copy()
                    new_row['State'] = state
                    print(new_row)
                    rows.append(new_row)
            else:
                rows.append(row)
        return pd.DataFrame(rows)


    # Duplicate rows based on states
    expanded_news_df = duplicate_rows(news)

    # Reset index if needed
    expanded_news_df.reset_index(drop=True, inplace=True)
    print("expanded df is :",expanded_news_df)
    expanded_news_df.to_excel("federal_news_headings_Demo.xlsx",index=False)


    # globals()[news] = expanded_news_df.copy()
    # news = pd.merge(news, fipsDF[['State\xa0or equivalent', 'State FIPS']],left_on='State Name',right_on='State\xa0or equivalent', how='left')
    news = pd.merge(expanded_news_df, fipsDF[['State\xa0or equivalent', 'State FIPS']],left_on='State', right_on='State\xa0or equivalent', how='left')
    news['State FIPS'] = news['State FIPS'].apply(lambda x: '{:02d}'.format(int(x)) if pd.notna(x) and isinstance(x, (int, float)) else '')
    news = news.explode('State').reset_index(drop=True)
    print("Columns are :-",news.columns)
    news.to_excel('FederalNewsHeadings.xlsx', index=False)
    word_to_replace2 = 'clg'
    replacement_string2 = 'Minority Colleges and Universities'

    # Replace the word in the 'State' column (case-insensitive)
    # unique_df['State'] = unique_df['State'].str.replace(r'\b{}\b'.format(word_to_replace2), replacement_string2,regex=True, flags=re.IGNORECASE)
    print(unique_df['State'])

    new_column_names = {'S-no':'S-no','News Headings Short':'News Headings Short','State FIPS': 'state_geoid', 'State': 'state_name/area of interest', 'Agency': 'agency',
                        'Date of announcement': 'date_of_press_release', 'News heading': 'news_headings',
                        'links': 'links', 'Date of running': 'date_of_running', 'Matching keyword': 'matching_keyword',
                        'Relevancy': 'relevancy'}
    news = news.rename(columns=new_column_names)
    # news = add_states_to_news(news)
    print("Columns are :-", news.columns)



    colsToKeep = ['state_geoid','state_name/area of interest','agency','date_of_press_release','news_headings','links','date_of_running','matching_keyword','relevancy']
    # # news[['state_geoid','state_name','agency','date_of_press_release','news_headings','links','date_of_running','matching_keyword','relevancy']]
    news["state_name/area of interest"] = news["state_name/area of interest"].fillna("Article")
    # news = news.drop_duplicates(subset=['state_name/area of interest', 'news_headings'],keep='first')
    news['state_name/area of interest'] = news['state_name/area of interest'].str.replace(r'\b{}\b'.format(word_to_replace), replacement_string, regex=True,flags=re.IGNORECASE)
    news['state_name/area of interest'] = news['state_name/area of interest'].str.replace(r'\b{}\b'.format(word_to_replace2), replacement_string2,regex=True, flags=re.IGNORECASE)
    # news = pd.merge(news, fipsDF[['State\xa0or equivalent', 'State FIPS']], left_on='state_name/area of interest',right_on='State\xa0or equivalent', how='left')
    news = news.drop_duplicates(subset=['state_name/area of interest', 'news_headings'],keep='first')
    news['date_of_press_release'] = pd.to_datetime(news['date_of_press_release'])
    news['date_of_press_release'] = news['date_of_press_release'].dt.strftime('%m/%d/%Y')
    news[colsToKeep].to_excel("federal_news_headings.xlsx",index=False)
    news.to_excel("federal.xlsx",index=False)

    # news.to_excel("federal_news_headings.xlsx",index=False)

    # print(news.columns)
    # , mode = 'a'
else:
    new_df.to_excel('FederalNewsHeadings.xlsx', index=False)
# unique_df.to_csv( 'NewsHeadings.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d)" )))

# disconnect_nord_vpn()
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++Completed+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")