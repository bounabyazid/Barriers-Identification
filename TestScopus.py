#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 10:27:47 2019

@author: Yazid Bounab
"""
import requests
import json
from Elsevier import ELSEVIER_API_KEY
import xml.etree.ElementTree as ET

#https://api.elsevier.com/content/search/scopus?query='russian+finnish+barriers'&apiKey=
#http://kitchingroup.cheme.cmu.edu/blog/2015/04/03/Getting-data-from-the-Scopus-API/

def get_Results():
    url = "http://ieeexploreapi.ieee.org/api/v1/search/articles&index_terms=finnish"
    resp = requests.get(url+"?field=authkeywords", headers={'Accept':'application/json', 'X-ELS-APIKey': ELSEVIER_API_KEY})
    return resp.text.encode('utf-8')

def get_Dois(resp):
    Dois = []
    y = json.loads(resp.text)
    for entry in y['search-results']['entry']:
        #print (entry['dc:title'])
        if 'prism:doi' in entry.keys():
            #print(entry['prism:doi'])
            Dois.append(entry['prism:doi'])
    return Dois

def get_Dois2(resp): 
    results = resp.json()
    return [[str(r['prism:doi'])] for r in results['search-results']["entry"]]

def get_IDs(resp): 
    results = resp.json()
    return [[str(r['dc:identifier'])] for r in results['search-results']["entry"]]

def get_Text_DOI(doi):
    print (doi)
    #resp = requests.get("https://api.elsevier.com/content/article/doi/10.1016/j.ibusrev.2018.07.001?APIKey=",
    resp = requests.get("https://api.elsevier.com/content/article/doi/"+doi,
                headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})

    y = json.loads(resp.text)
    title=''
    abstract=''
    if 'full-text-retrieval-response' in y.keys():
        title  = y['full-text-retrieval-response']['coredata']['dc:title']
        abstract = y['full-text-retrieval-response']['coredata']['dc:description']
        #print (title,abstract)
    return title,abstract

def get_Text_scopus_ID(SCOPUS_ID):
    url = "http://api.elsevier.com/content/abstract/scopus_id/"+ SCOPUS_ID
    resp = requests.get(url, headers={'Accept':'application/json','X-ELS-APIKey': MY_API_KEY})
    results = json.loads(resp.text.encode('utf-8'))
    
def json_parse():
    #resp = requests.get("https://api.elsevier.com/content/search/scopus?query=%27russian+finnish+barriers%27",
    url = "https://api.elsevier.com/content/search/scopus?query='russian+finnish+trade+barriers'"
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
       
       while startC < itemsPerPage*N:
             resp = requests.get(url+'&start='+str(startC), headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})
             Dois.extend(get_Dois2(resp))
             startC += itemsPerPage

       resp = requests.get(url+'&start='+str(startC), headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})
       Dois.extend(get_Dois(resp))
    else:
         resp = requests.get(url+'&start='+str(startC), headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})
         Dois = get_Dois(resp)
    
    return Dois#,Titles,Absts

#Dois,Titles,Absts = json_parse()

Dois = json_parse()

#title,abstract = getText('10.1016/j.ibusrev.2018.07.001')
#title,abstract = getText('10.1111/j.1533-8525.1995.tb00443.x')

#Absts = []
#Titles = []
#for doi in Dois:
#    title,abstract = get_Text_DOI(doi)
#    Absts.append(abstract)
#    Titles.append(title)

def getdocIDs(): 
    url = 'https://api.elsevier.com/content/search/scopus?query=%27russian+finnish+trade+barriers%27&field=dc:identifier&apiKey='
    url = "https://api.elsevier.com/content/search/scopus?query='russian+finnish+trade+barriers'&field=dc:identifier"
    resp = requests.get(url, headers={'Accept':'application/json', 'X-ELS-APIKey': ELSEVIER_API_KEY})

    results = resp.json()
    return [[str(r['dc:identifier'])] for r in results['search-results']["entry"]]

SC_IDS = getdocIDs()

