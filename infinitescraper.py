from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
import time

chromeOptions = Options()
chromeOptions.headless = True
driver = webdriver.Chrome('C:/Users/User/Desktop/New folder/WebScrape/chromedriver.exe', options=chromeOptions)
driver.get('https://www.goat.com/sneakers')

last_height = driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(5)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height

soup = BeautifulSoup(driver.page_source, 'lxml')
product_card = soup.find_all('div', class_='GridStyles__GridCellWrapper-sc-1cm482p-0 biZBPm')

df = pd.DataFrame({'Name': [], 'Release Date': [], 'Price': [], 'Links': []})
for product in product_card:
    try:
        name = product.find('div', class_='GridCellProductInfo__Name-sc-17lfnu8-3 hfCoWX').text
        date = product.find('div', class_='GridCellProductInfo__Year-sc-17lfnu8-2 jJQboW').text
        price = product.find('div', class_='GridCellProductInfo__Price-sc-17lfnu8-6 gsZMPb').text
        link = product.find('a', class_='GridCellLink__Link-sc-2zm517-0 dcMqZE').get('href')
        full_link = 'https://www.goat.com'+link
        df = pd.concat([df, pd.DataFrame({'Name': [name], 'Release Date': [date], 'Price': [price], 'Links': [full_link]})])
    except:
        pass
print(f"Scraped {len(df)} posts.")
df.to_csv('sneakers_list.csv', index=False)
