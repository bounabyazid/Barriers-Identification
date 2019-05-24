import re
import json
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment

# imports
import pandas as pd
import os

link = "https://www.thefastlaneforum.com/community/search/36101691/?q=trade+barrier&o=date"
'https://community.startupnation.com/search?Search=russia+trade+barrier'

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
    over=urlopen(link).read()
    soup = BeautifulSoup(over, features="lxml")

    Pages = {}
    Links = [link]
    
    NPages = soup.find('div',attrs={"class":"PageNav"})
    if NPages:
       nbpages = NPages.find('span',attrs={"class":"pageNavHeader"}).text
       nbpages = nbpages.replace('Page ','')
       nbpages = nbpages.replace(' of ','-')

       #start = nbpages[0:nbpages.index('-')]
       end = nbpages[nbpages.index('-')+1:None]
       fix = NPages.find('nav').find('a',attrs={"class":"currentPage"})['href']
       
       if 'page-' in fix:
          fix = fix[0:fix.index('page-')]
           
       #print (fix)
       for i in range(2,int(end)+1):
#           Links.append(link+'page-'+str(i))
           Links.append('https://www.thefastlaneforum.com/community/'+fix+'page-'+str(i))
#    if len(Links) == 0:           
    for link in Links:
        #print (link,'\n________________________\n')
        over=urlopen(link).read()
        soup = BeautifulSoup(over, features="lxml")
        Results = soup.find('ol',attrs={"class":"messageList xbMessageModern"}).findAll('li',attrs={'class':'message'})
        
        Comments = []

        for res in Results:
            Comments.append(res.find('article').text.strip())
        Pages['Page'+str(Links.index(link))] = Comments
        #Pages.append(Comments)
    return Pages
    
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
            print(Dict['link'])
            Dict['Pages'] = getMessages(Dict['link'])
            
            #Dict['DateTime'] = res.find('span',attrs={"class":"DateTime"})['title']
            #Comments.append(Dict)
            
            Pages['Page'+str(Links.index(link))] = Dict
    return Pages

#link = 'https://www.thefastlaneforum.com/community/threads/where-i-have-been-this-time-and-why-im-famous-at-wells-fargo.70026/'
#link = 'https://www.thefastlaneforum.com/community/posts/746756/'

#pages = getMessages(link)

#getTopics([link])
Pages = getTopics(getPages(link))

#print(soup)
#with open('Fastlane.json', 'w') as fp:
#     json.dump(Pages, fp)

#with open('Fastlane.json', 'r') as fp:
#     Pages = json.load(fp)
