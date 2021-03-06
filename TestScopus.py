#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 10:27:47 2019

@author: Yazid Bounab
"""
import csv
import json

import requests
import pandas as pd

from Elsevier import ELSEVIER_API_KEY
import xml.etree.ElementTree as ET

#https://api.elsevier.com/content/search/scopus?query='russian+finnish+barriers'&apiKey=50636289cfda4f5ed3eacdee69504721
#http://kitchingroup.cheme.cmu.edu/blog/2015/04/03/Getting-data-from-the-Scopus-API/

url = "https://api.elsevier.com/content/search/scopus?query='russian+finnish+barriers+business'"
#url = 'https://api.elsevier.com/content/search/scopus?query=title-abs-key(trade barriers business)'
def get_Results():
    url = "http://ieeexploreapi.ieee.org/api/v1/search/articles&index_terms=finnish"
    resp = requests.get(url+"?field=authkeywords", headers={'Accept':'application/json', 'X-ELS-APIKey': ELSEVIER_API_KEY})
    return resp.text.encode('utf-8')

def get_IDs(resp): 
    results = resp.json()
    return [[str(r['dc:identifier'])] for r in results['search-results']["entry"]]

def get_Text_scopus_ID(SCOPUS_ID):
    url = "http://api.elsevier.com/content/abstract/scopus_id/"+ SCOPUS_ID
    resp = requests.get(url, headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})
    results = json.loads(resp.text.encode('utf-8'))
    
def getScopus_IDs(): 
    url = 'https://api.elsevier.com/content/search/scopus?query=%27russian+finnish+trade+barriers%27&field=dc:identifier&apiKey=50636289cfda4f5ed3eacdee69504721'
    url = "https://api.elsevier.com/content/search/scopus?query='trade+barriers+business'&field=dc:identifier"
    resp = requests.get(url, headers={'Accept':'application/json', 'X-ELS-APIKey': ELSEVIER_API_KEY})

    results = resp.json()
    return [[str(r['dc:identifier'])] for r in results['search-results']["entry"]]

def get_Full_Text_DOI(doi):
    
    url = 'https://api.elsevier.com/content/abstract/doi/'+doi+'?field=authkeywords'
    
    print (url)
    #resp = requests.get("https://api.elsevier.com/content/article/doi/10.1016/j.ibusrev.2018.07.001?APIKey=50636289cfda4f5ed3eacdee69504721",
    resp = requests.get(url, headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})

    y = json.loads(resp.text)
    title = ''
    abstract = ''
    keyWords = ''
    if 'full-text-retrieval-response' in y.keys():
        title  = y['full-text-retrieval-response']['coredata']['dc:title']
        abstract = y['full-text-retrieval-response']['coredata']['dc:description']
        if 'authkeywords' in y['full-text-retrieval-response']['coredata'].keys():
            keyWords = y['full-text-retrieval-response']['coredata']['authkeywords']
            #keywords = [keyword['$'] for keyword in y['abstracts-retrieval-response']['authkeywords']['author-keyword']]
        print (title,abstract,keyWords)
    return title,abstract,keyWords

def get_Full_Text_DOI(doi):
    
    url = 'https://api.elsevier.com/content/article/doi/'+doi+'?field=authkeywords'
    
    print (url)
    #resp = requests.get("https://api.elsevier.com/content/article/doi/10.1016/j.ibusrev.2018.07.001?APIKey=50636289cfda4f5ed3eacdee69504721",
    resp = requests.get(url, headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})

    y = json.loads(resp.text)
    title = ''
    abstract = ''
    keyWords = ''
    if 'full-text-retrieval-response' in y.keys():
        title  = y['full-text-retrieval-response']['coredata']['dc:title']
        abstract = y['full-text-retrieval-response']['coredata']['dc:description']
        if 'authkeywords' in y['full-text-retrieval-response']['coredata'].keys():
            keyWords = y['full-text-retrieval-response']['coredata']['authkeywords']
        print (title,abstract,keyWords)
    return title,abstract,keyWords

def get_Abstract_Text_DOI(doi):
    
    url = 'https://api.elsevier.com/content/abstract/doi/'+doi+'?field=authkeywords'
    
    print (url)
    resp = requests.get(url, headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})

    page = json.loads(resp.text)
    title = ''
    abstract = ''
    keyWords = ''
    if 'full-text-retrieval-response' in page.keys():
        title  = page['full-text-retrieval-response']['coredata']['dc:title']
        abstract = page['full-text-retrieval-response']['coredata']['dc:description']
        if 'authkeywords' in page['full-text-retrieval-response']['coredata'].keys():
            keyWords = page['full-text-retrieval-response']['coredata']['authkeywords']
            #keywords = [keyword['$'] for keyword in y['abstracts-retrieval-response']['authkeywords']['author-keyword']]
        print (title,abstract,keyWords)
        
    keywords = [keyword['$'] for keyword in page['abstracts-retrieval-response']['authkeywords']['author-keyword']]
    return title,abstract,keyWords

def get_Titles_Abstracts_keyWords(Dois):
    Absts = []
    Titles = []
    keyWords = []
    for doi in Dois:
        print (doi)
        title,abstract,keys = get_Full_Text_DOI(doi)
        Titles.append(title)
        Absts.append(abstract)
        keyWords.append(keys)
    return Titles,Absts,keyWords

def get_Dois(resp):
    Dois = []
    y = json.loads(resp.text)
    if 'search-results' in y.keys():
       for entry in y['search-results']['entry']:
           #print (entry['dc:title'])
           if 'prism:doi' in entry.keys():
               #print(entry['prism:doi'])
               Dois.append(entry['prism:doi'])
    #return [[str(r['prism:doi'])] for r in results['search-results']["entry"]]
    return Dois

def Search_Quary():
    resp = requests.get(url, headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})
    
    y = json.loads(resp.text)
    
    totalResults = int(y['search-results']['opensearch:totalResults'])
    #print (y['search-results']['opensearch:startIndex'])
    itemsPerPage = int(y['search-results']['opensearch:itemsPerPage'])
    #print (len(y['search-results']['entry']))
    
    Dois = []
    startC = 0

    if totalResults > itemsPerPage:
       N = int(totalResults/itemsPerPage)
       i = 0
       while startC < itemsPerPage*N:
             print ('page '+str(i)+'/'+str(N))
             resp = requests.get(url+'&start='+str(startC), headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})
             Dois.extend(get_Dois(resp))
             startC += itemsPerPage
             i+=1
       print ('page '+str(i)+'/'+str(N))
       
       resp = requests.get(url+'&start='+str(startC), headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})
       Dois.extend(get_Dois(resp))
    else:
         resp = requests.get(url+'&start='+str(startC), headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})
         Dois = get_Dois(resp)
    
    #with open('Dois.txt', 'w') as f:
    #     f.write("\n".join(Dois))
    
    Titles,Absts,keyWords = get_Titles_Abstracts_keyWords(Dois)
    
    return Dois,Titles,Absts,keyWords

def Load_Dois():
    with open("Dois.txt") as f:
         Dois = f.readlines()

    df = pd.DataFrame({'Doi': Dois,'Scopus_Id':'','Title':'','Abstract' : '','Keywords':''})
    i=0
    for doi in Dois:
        df.at[i,'Title'],df.at[i,'Abstract'] = get_Full_Text_DOI(doi)

        i+=1
    
              
    #df.to_csv('Corpus.csv')
    return df

#Dois = Search_Quary()
#Titles,Absts = get_Titles_Abstracts(Dois)
#SC_IDS = getdocIDs()

#df = Load_Dois()

Dois,Titles,Absts,keyWords = Search_Quary()