#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 11:07:42 2019

@author: Yazid Bounab
"""
#https://stackoverflow.com/questions/30513808/scopus-keywords-and-citations-crawling

import json
import requests
from Elsevier import ELSEVIER_API_KEY

api_resource = "https://api.elsevier.com/content/search/scopus?"
search_param = 'query=title-abs-key(trade barriers business)'

# headers
headers = dict()
headers['X-ELS-APIKey'] = ELSEVIER_API_KEY
headers['X-ELS-ResourceVersion'] = 'XOCS'
headers['Accept'] = 'application/json'

def get_Urls(page_request):
    page = json.loads(page_request.content.decode("utf-8"))
    #return [str(r['prism:url']) for r in page['search-results']["entry"] if r['openaccess'] == '1']
    return [str(r['prism:url']) for r in page['search-results']["entry"]]

def get_keyWords(article_url):
    article_request = requests.get(article_url + "?field=authkeywords", headers=headers)
    article_keywords = json.loads(article_request.content.decode("utf-8"))
    keywords = []
    if 'authkeywords' in article_keywords['abstracts-retrieval-response'].keys():
       keywords = [keyword['$'] for keyword in article_keywords['abstracts-retrieval-response']['authkeywords']['author-keyword']]
    return keywords

def Search_Quary():
    page_request = requests.get(api_resource + search_param, headers=headers)
    page = json.loads(page_request.content.decode("utf-8"))
    
    totalResults = int(page['search-results']['opensearch:totalResults'])
    itemsPerPage = int(page['search-results']['opensearch:itemsPerPage'])
    
    Urls = []
    startC = 0

    if totalResults > itemsPerPage:
       N = int(totalResults/itemsPerPage)
       i = 0
       while startC < itemsPerPage*N:
             print ('page '+str(i)+'/'+str(N))
             page_request = requests.get(api_resource + search_param+'&start='+str(startC), headers=headers)
             Urls.extend(get_Urls(page_request))
             startC += itemsPerPage
             i+=1
             
       print ('page '+str(i)+'/'+str(N))
       resp = requests.get(api_resource + search_param+'&start='+str(startC), headers=headers)
       Urls.extend(get_Urls(resp))
    else:
         resp = requests.get(api_resource + search_param+'&start='+str(startC), headers=headers)
         Urls = get_Urls(resp)
    
    return Urls
    
def get_all_keywords():
    keyWords = []
    for url in Urls:
        keyWords.extend(get_keyWords(url))
    return keyWords,

Urls = Search_Quary()
keywords = get_all_keywords()
