#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 10:51:02 2019

@author: Yazid Bounab
"""

import requests
import json
from Elsevier import ELSEVIER_API_KEY

#query = 'https://api.elsevier.com/content/abstract/doi/10.1016/S0014-5793(01)03313-0?apiKey='+ELSEVIER_API_KEY
#resp = requests.get(query)
                    #headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})
#print ("http://api.elsevier.com/content/author?author_id=7004212771&view=metrics",
#                    headers={'Accept':'application/json','X-ELS-APIKey': ELSEVIER_API_KEY})
#print (json.dumps(resp.json(), sort_keys=True, indent=4, separators=(',', ': ')))

base_URL = "http://api.elsevier.com/content/search/scopus?query=finnish"
resp0 = requests.get("http://api.elsevier.com/content/search/scopus?query=AFFIL\
                    %28university+AND+physics+AND+united+kingdom%29+AND+SUBJAREA%28PHYS%29\
                    &field=affiliation", headers={'Accept' : 'application/json', 
                     'X-ELS-APIKey' : ELSEVIER_API_KEY})
resp = requests.get(base_URL, headers={'Accept' : 'application/json', 'X-ELS-APIKey' : ELSEVIER_API_KEY})
results = resp.json()

#return 
print([[str(r['affiliation'])] for r in results['search-results']["entry"]])

#print(json.dumps(resp.json(),
 #                sort_keys=True,
  #               indent=4, separators=(',', ': ')))