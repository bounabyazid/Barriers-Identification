#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:45:53 2019

@author: polo
""" 
import os

import csv

import nltk
from nltk.corpus import stopwords
from gensim.utils import simple_preprocess

import pickle

import pandas as pd

from fuzzywuzzy import fuzz

#Dois = []
#Titles = []
#Absts = []
 
Tariff = {
		"Direction" : 0,
		"Purpose" : 0,
		"Time length" : 0,
		"Import restraints" : 0,
		"Rates" : 0,
		"Distribution points" : 0
        }

NonTariff = {
        "Government participation in trade" : 0,
		"Customs and entry procedures" : 0,
		"Product requirements" : 0,
		"Quotas" : 0,
		"Financial control" : 0
	   }
   
Barriers = {}

stop_words = stopwords.words('english')
sentences = []
def load_Barriers():
    for key in Tariff.keys():
        with open('Barriers/Tariff/'+key+'.txt', 'r') as f:
             Barriers[key] = f.readlines()

    for key in NonTariff.keys():
        with open('Barriers/NonTariff/'+key+'.txt', 'r') as f:
             Barriers[key] = f.readlines()
            
def LoadFileToList(filename):
    mylist = []
    with open('Data/'+filename, 'rb') as filehandle:  
         mylist = pickle.load(filehandle)
    return mylist

def PreprocessText(sentences):
    for sentence in sentences:
        words = []
        for w in simple_preprocess(sentence, deacc=True):
            if w not in stop_words:
               words.append(w)
    
        sentence = " ".join(words)
    #
    return sentences    
        
def Overlap2(setA,setB):
    overlap = 0
    for l in setA:
        for w in setB:
            #ratio = fuzz.ratio(l, w)
            ratio = fuzz.token_set_ratio(l, w)
            if ratio>70:
           #fuzz.token_set_ratio() 
               overlap += 1
               #print (str(ratio))
    #score  = overlap/(len(setA)+len(setB))
    return overlap

def Overlap(setA,setB):
    overlap = 0
    for l in setA:
        for w in setB:
            if fuzz.ratio(l, w) >= 85:
               fuzz.token_set_ratio() 
               overlap += 1
    score  = overlap/(len(setA)+len(setB))
    return score

def Compute_Proportion(text):
    #setB = PreprocessText(text)
    sentences = nltk.sent_tokenize(text)

    sentences = PreprocessText(sentences)
    setB = sentences
    for key in Tariff.keys():
        #print ('_____________'+key+'_____________')
        Tariff[key] = Overlap2(Barriers[key],PreprocessText(setB))
    for key in NonTariff.keys():
        #print ('_____________'+key+'_____________')
        NonTariff[key] = Overlap2(Barriers[key],PreprocessText(setB))
      
def Proportion_Journal(Articles):
    
    COLUMN_NAMES = ['Doi','Title','Abstract','Year']
    COLUMN_NAMES.extend(list(Tariff.keys()))
    COLUMN_NAMES.extend(list(NonTariff.keys()))

    df = pd.DataFrame(columns=COLUMN_NAMES)
    
    Dict = dict((key,value) for key, value in Articles.items() if Articles[key]['abstract'] is not None)
    
    for key in Dict.keys():
        data = [key,Dict[key]['title'],Dict[key]['abstract'],'2019']
        
        for Tkey in Tariff.keys():
            data.append(Tariff[Tkey])
        for NTkey in NonTariff.keys():
            data.append(NonTariff[NTkey])
            
        df.at[df.size+1] = data
        
        Tariff.fromkeys(Tariff, 0)
        NonTariff.fromkeys(NonTariff, 0)
        data.clear()
        df.to_csv('Journals-DataSet/Yazid.csv', sep=',', encoding='utf-8')
        
    return df         
#Absts = LoadFileToList('Abstracts.pkl')
load_Barriers()

abst = 'Chinese import tariffs. This link shows that China is reducing its import tariffs on luxury \
        foreign goods such as Scottish Whiskey from 10% to 5%. It is a sign Chinese government want \
        to encourage consumer spending. BBC – China cuts import tariffs'

#Compute_Proportion(abst)
Articles = LoadFileToList('Articles.pkl')  
df = Proportion_Journal(Articles)