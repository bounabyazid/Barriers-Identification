import re
import json
import time
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment

# imports
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os

link = "https://www.thefastlaneforum.com/community/search/36101691/?q=trade+barrier&o=date"
'https://community.startupnation.com/search?Search=russia+trade+barrier'

link2 = "https://www.tripadvisor.com/Airline_Review-d8729157-Reviews-Spirit-Airlines#REVIEWS"

def get_reviews():
    'https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25'
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)
                          
    driver.get(link)
    more_buttons = driver.find_elements_by_class_name("moreLink")
    for x in range(len(more_buttons)):
        if more_buttons[x].is_displayed():
           driver.execute_script("arguments[0].click();", more_buttons[x])
           time.sleep(1)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'lxml')
    reviews = []
    reviews_selector = soup.find_all('div', class_='reviewSelector')
        
    for review_selector in reviews_selector:
        review_div = review_selector.find('div', class_='dyn_full_review')
        if review_div is None:
            review_div = review_selector.find('div', class_='basic_review')
        review = review_div.find('div', class_='entry').find('p').get_text()
        review = review.strip()
        reviews.append(review)
    
    return reviews   

def getPages(link):
    over=urlopen(link).read()
    soup = BeautifulSoup(over, features="lxml")

    Links = []
    Pages = soup.find('div',attrs={"class":"PageNav"}).find('nav')

    for page in Pages.findAll('a'):
        link = page.attrs['href']
        Links.append('https://www.thefastlaneforum.com/community/'+link)
    return Links

def getMessages(link):
#    Pages = {}
#    for link in Links:
    over=urlopen(link).read()
    soup = BeautifulSoup(over, features="lxml")
    Results = soup.findAll('li')
    
    Comments = []

    for res in Results:
    
def getTopics(Links): 
    Pages = {}
    for link in Links:
        over=urlopen(link).read()
        soup = BeautifulSoup(over, features="lxml")
        Results = soup.findAll('li',attrs={"class":"searchResult post primaryContent"})
        Comments = []

        for res in Results:
            Dict = {}
            Dict['usernam'] = res.find('a',attrs={"class":"username"}).text
             
            title = str(res.find('h3',attrs={"class":"title"}).find('a'))
            
            if title.find('</span>'):
               start = title.find('</span>')+len('</span>')
               end = title.find("</a>")
               Dict['title'] = title[start:end]   
            else:            
                Dict['title'] = res.find('h3',attrs={"class":"title"}).text
            #Dict['Comment'] = res.find('blockquote',attrs={"class":"snippet"}).text
            Dict['link'] = 'https://www.thefastlaneforum.com/community/'+res.find('h3',attrs={"class":"title"}).find('a')["href"]
            #Dict['DateTime'] = res.find('span',attrs={"class":"DateTime"})['title']
            Comments.append(Dict)
            
        Pages['Page'+str(Links.index(link))] = Comments
    return Pages

getMessages(link)
#getTopics([link])
#Pages = getTopics(getPages(link))

#print(soup)
#with open('Fastlane.json', 'w') as fp:
#     json.dump(Pages, fp)

#with open('Fastlane.json', 'r') as fp:
#     Pages = json.load(fp)
