#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 16:53:10 2019
@author: polo
"""
#50636289cfda4f5ed3eacdee69504721
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
    return [str(r['prism:url']) for r in page['search-results']["entry"] if r['openaccess'] == '1']

def get_keyWords(article_url):
    article_request = requests.get(article_url + "?field=authkeywords", headers=headers)
    article_keywords = json.loads(article_request.content.decode("utf-8"))
    return [keyword['$'] for keyword in article_keywords['abstracts-retrieval-response']['authkeywords']['author-keyword']]
        
def get_Full_Text_DOI(doi):
    url = 'https://api.elsevier.com/content/abstract/doi/'+doi
    print (url)
    resp = requests.get(url, headers=headers)

    page = json.loads(resp.text)
    title = ''
    abstract = ''
    if 'full-text-retrieval-response' in page.keys():
        title  = page['full-text-retrieval-response']['coredata']['dc:title']
        abstract = page['full-text-retrieval-response']['coredata']['dc:description']
        print (title,abstract)
    return title,abstract
    
def get_Dois(page_request):
    Dois = []
    page = json.loads(page_request.content.decode("utf-8"))
    if 'search-results' in y.keys():
       for entry in page['search-results']['entry']:
           if entry['openaccess'] == '1':
               #print (entry['dc:title'])
               if 'prism:doi' in entry.keys():
                   #print(entry['prism:doi'])
                   Dois.append(entry['prism:doi'])
    #return [[str(r['prism:doi'])] for r in results['search-results']["entry"]]
    return Dois
    
    
def Search_Quary():
    page_request = requests.get(api_resource + search_param, headers=headers)
    page = json.loads(page_request.content.decode("utf-8"))
    
    totalResults = int(page['search-results']['opensearch:totalResults'])
    itemsPerPage = int(page['search-results']['opensearch:itemsPerPage'])
    
    Dois = []
    Urls = []
    startC = 0

    if totalResults > itemsPerPage:
       N = int(totalResults/itemsPerPage)
       i = 0
       while startC < itemsPerPage*N:
             print ('page '+str(i)+'/'+str(N))
             resp = requests.get(api_resource + search_param+'&start='+str(startC), headers=headers)
             #Dois.extend(get_Dois(resp))
             Urls.extend(get_Urls(resp))
             startC += itemsPerPage
             i+=1
             
       print ('page '+str(i)+'/'+str(N))
       resp = requests.get(api_resource + search_param+'&start='+str(startC), headers=headers)
       #Dois.extend(get_Dois(resp))
       Urls.extend(get_Urls(resp))
    else:
         resp = requests.get(api_resource + search_param+'&start='+str(startC), headers=headers)
         #Dois = get_Dois(resp)
         Urls = get_Urls(resp)
    
    #Titles,Absts = get_Full_Text_DOI(doi)(Dois)
    
    keyWords = []
    for url in Urls:
        keyWords.extend(get_keyWords(url))
    return keyWords,#Dois,Titles,Absts,keyWords

keyWords = Search_Quary()

print (keyWords)