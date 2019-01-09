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

#https://api.elsevier.com/content/search/scopus?query='russian+finnish+barriers'&apiKey=50636289cfda4f5ed3eacdee69504721

def get_scopus_info():
    
    url = ("https://api.elsevier.com/content/search/scopus?query=%27finnish%27"+"?field=title")
    #url = ("http://api.elsevier.com/content/search/scopus?query=Similarity"+ "?field=title")
    resp = requests.get(url, headers={'Accept':'application/json', 'X-ELS-APIKey': ELSEVIER_API_KEY})

    return json.loads(resp.text.encode('utf-8'))

#results = get_scopus_info()

def get_Results():
    #url = "http://ieeexploreapi.ieee.org/api/v1/search/articles&index_terms=finnish"
    url = "https://api.elsevier.com/content/search/scopus?query=%27russian+finnish+barriers%27"
    resp = requests.get(url+"?field=authkeywords", headers={'Accept':'application/json', 'X-ELS-APIKey': ELSEVIER_API_KEY})
    return resp.text.encode('utf-8')

def test():
    resp = requests.get("https://api.elsevier.com/content/search/scopus?query=%27russian+finnish+barriers%27",
                    headers={'Accept':'text/xml',
                             'X-ELS-APIKey': ELSEVIER_API_KEY})

    #print (resp.headers)
    xmltxt=resp.content
    testId = XML (xmltxt).find("testId").text
    
def json_parse():
    resp = requests.get("https://api.elsevier.com/content/search/scopus?query=%27russian+finnish+barriers%27",
                    headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})
    #with open('data.json', 'w', encoding='utf-8') as outfile:
    #     json.dump(resp.json(), outfile)
    y = json.loads(resp.text)
    
    print (y['search-results']['opensearch:totalResults'])
    print (y['search-results']['opensearch:startIndex'])
    print (y['search-results']['opensearch:itemsPerPage'])
    
    for child in resp.getchildren():
        print(child.text)
#json_parse()

def parseXML(): 
    resp = requests.get("https://api.elsevier.com/content/search/scopus?query=%27russian+finnish+barriers%27",
                    headers={'Accept':'text/xml','X-ELS-APIKey': ELSEVIER_API_KEY})
    #with open('data.json', 'w', encoding='utf-8') as outfile:
    #     json.dump(resp.json(), outfile)

    # create element tree object 
    tree = ET.parse(resp.text) 
  
    # get root element 
    root = tree.getroot() 
  
    # create empty list for news items 
    newsitems = [] 
  
    # iterate news items 
    for item in root.findall('./search-results/entry'):
        print(item)

parseXML()