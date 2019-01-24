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
search_param = 'query=title-abs-key(big data)'  # for example

# headers
headers = dict()
headers['X-ELS-APIKey'] = ELSEVIER_API_KEY
headers['X-ELS-ResourceVersion'] = 'XOCS'
headers['Accept'] = 'application/json'

# request with first searching page
page_request = requests.get(api_resource + search_param, headers=headers)
# response to json
page = json.loads(page_request.content.decode("utf-8"))
# List of articles from this page
articles_list = page['search-results']['entry']

article = articles_list[0]

title = article['dc:title']
cit_count = article['citedby-count']
authors = article['dc:creator']
date = article['prism:coverDate']

article_url = article['prism:url']
# something like this:
# 'http://api.elsevier.com/content/abstract/scopus_id/84909993848'

article_request = requests.get(article_url + "?field=authkeywords", headers=headers)
article_keywords = json.loads(article_request.content.decode("utf-8"))
keywords = [keyword['$'] for keyword in article_keywords['abstracts-retrieval-response']['authkeywords']['author-keyword']]