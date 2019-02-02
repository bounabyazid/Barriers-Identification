#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 10:47:27 2019

@author: polo
"""
import csv
import json
#import xplore

import urllib.request

import pandas as pd

import xml.etree.ElementTree as ET

key = 'cu63czs28tuf38d74cypnv4u'
    
def get_Results():
    outputType = 'json'
    outputDataFormat = 'raw'
    resultSetMax = 27833
    resultSetMaxCap = 27833
    startRecord = 1
    sortOrder = 'asc'
    sortField = 'article_title'
    
    url = "http://ieeexploreapi.ieee.org/api/v1/search/articles"
    url += '?apikey=' + str(key)
    url += '&format='+ str(outputType)
    url += '&max_records=' + str(resultSetMax)
    url += '&start_record=' + str(startRecord)
    url += '&sort_order=' + str(sortOrder)
    url += '&sort_field=' + str(sortField)
    url += '&abstract=barriers'
    
    resp = urllib.request.urlopen(url).read()
    resp = json.loads(resp) 
    #print (resp.keys())['totalfound']

    totalResults = int(resp['total_records'])
    print (totalResults)
    
    Titles = []
    Abstracts = []
    keywords = []

    #print(resp['articles'][4]['index_terms']['ieee_terms']['terms'])
    for article in resp['articles']:
        Titles.append(article['title'])
        Abstracts.append(article['abstract'])
        if 'ieee_terms' in article['index_terms'].keys():
            keywords.append(article['index_terms']['ieee_terms']['terms'])

    #print(titles)
    return Titles, Abstracts, keywords 

Titles, Abstracts, keywords = get_Results()
