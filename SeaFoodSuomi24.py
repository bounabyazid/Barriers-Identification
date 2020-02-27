#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 04:46:24 2020

@author: Yazid BOUNAB
"""
import pickle
from urllib.request import urlopen
from bs4 import BeautifulSoup

BaseLink = 'https://keskustelu.suomi24.fi'
Section = 'ruoka-ja-juoma/kala-ja-ayriaiset'

def getReplyofReplay(element):
    Replies = []
    elements = element.find_all('p')
    for elem in elements:
        Replies.append(elem.text)
        Replies.extend(getReplyofReplay(elem))
    return list(set(Replies))

def getReplies(link):
    Replies = []
    print(link)
    soup = BeautifulSoup(urlopen(link), 'lxml')
    Table = soup.find('section', class_='ThreadComments__ThreadCommentsContainer-xoykri-1 bBdsfj')
    Table = Table.find('ul', class_='ThreadComments__CommentsList-xoykri-3 fPfGZn')
    for replay in Table.find_all('li'):
        Replies.append(replay.find('p').text)
        Replies.extend(getReplyofReplay(replay))
    return list(set(Replies))

def getPage(PageNumber):
    page = {}
    Discussions = []
    link = BaseLink+'/'+Section+'?page='+PageNumber
    soup = BeautifulSoup(urlopen(link), 'lxml')
    Table = soup.find('div', class_='row threads-list-container')
    
    page['page'+PageNumber] = []    
    for Discussion in Table.find_all('li', class_='thread-list-item thread-list-item-small'):
        Data = {}
        
        Data['Title'] = Discussion.find('div', class_='thread-list-item-title text-overflow').text
        Data['Link'] = Discussion.find('a', class_='thread-list-item-container')['href']
        Data['Date'] = Discussion.find('div', class_='thread-list-item-timestamp text-secondary text-bold-2 smaller pull-right').text
        Data['Text'] = Discussion.find('div', class_='thread-list-item-body text-black text-overflow').text
        Data['Replies'] = getReplies(Data['Link'])
        
        Discussions.append(Data)

    return Discussions

def getAllPages(BaseLink,Section):
    pages = {}
    link = BaseLink+'/'+Section
    soup = BeautifulSoup(urlopen(link), 'lxml')
    NbPages = int(soup.find('span', class_='pagination-page-count').text)

    for PageNumber in range(1,NbPages+1):
        print('_________________',PageNumber,'_________________')
        pages['page'+str(PageNumber)] = getPage(PageNumber=str(PageNumber))
    return pages

pages = getAllPages(BaseLink,Section)

pickle_out = open("Fish and SeaFood.pkl","wb")
pickle.dump(pages, pickle_out)
pickle_out.close()
