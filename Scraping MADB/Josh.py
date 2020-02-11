#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tus Oct  7 11:00:00 2019
@author: Yazid BOUNAB
"""

import pickle
import pandas as pd

from senti_client import sentistrength

#  Media posters are impacted by the layout of the visual post.

senti = sentistrength('EN')

def Senti_List(List):
    Score = []
    for text in List:
        res = senti.get_sentiment(text)
        Score.append(res['neutral'])
    return Score

def Sentiments_Analysis():
    pickle_in = open("IAN.pkl","rb")
    IAN = pickle.load(pickle_in)

    for key in IAN.keys():
        IAN[key]['Sentiments'] = Senti_List(IAN[key]['Tweet_punct'].tolist())
        break
    return IAN
IAN = Sentiments_Analysis()
#pickle_out = open("QScores.pkl","wb")
#pickle.dump(QScores, pickle_out)
#pickle_out.close()