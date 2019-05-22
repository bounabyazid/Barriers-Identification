#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:46:30 2019

@author: polo
"""

import json
from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment

link = 'https://www.ukbusinessforums.co.uk/search/5243532/?q=trade+barrier&o=date'
link = 'https://www.ukbusinessforums.co.uk/search/5243710/?q=trade+barrier&o=date'

def getPages(link):
    over=urlopen(link).read()
    #print (over)
    soup = BeautifulSoup(over, features="lxml")

    Links = []
    Pages = soup.find('div',attrs={"class":"PageNav"}).find('nav')

    for page in Pages.findAll('a'):
        link = page.attrs['href']
        Links.append('https://www.ukbusinessforums.co.uk/'+link)
    return Links

def getComments(Links):
    Pages = {}
    for link in Links:
        over=urlopen(link).read()
        soup = BeautifulSoup(over, features="lxml")
        Results = soup.findAll('li',attrs={"class":"searchResult post primaryContent"})
        Comments = []
        
        for res in Results:
            Dict = {}
            Dict['usernam'] = res.find('a',attrs={"class":"username"}).text
            Dict['title'] = res.find('h3',attrs={"class":"title"}).text
            Dict['Comment'] = res.find('blockquote',attrs={"class":"snippet"}).text
            #Dict['DateTime'] = res.find('span',attrs={"class":"DateTime"})['title']
            Comments.append(Dict)
            
        Pages['Page'+str(Links.index(link))] = Comments
    return Pages

#Links = getPages(link)
Pages = getComments(getPages(link))

with open('UKBusiness.json', 'w') as fp:
     json.dump(Pages, fp)