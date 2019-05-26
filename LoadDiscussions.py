#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:06:53 2019

@author: polo
"""
import os
import json
import numpy as np
from scipy import mean
from fuzzywuzzy import fuzz
from nltk.tokenize import sent_tokenize


def List_Dirs(MainDir):
    return [ f for f in os.listdir(MainDir)]# if os.path.isfile(os.path.join(destdir,f)) ]
 
def List_Files(directory, extension, path=False):
    if path:
       return [ os.path.abspath(os.path.join(directory, f)) for f in os.listdir(directory) if f.endswith('.' + extension)]
    else:
        return (f for f in os.listdir(directory) if f.endswith('.' + extension))

def List_Dirs_and_Files(MainDir, extension, path):
    SubDirs = List_Dirs(MainDir)
    Files = []
    for Sub in SubDirs:
        Files.extend(List_Files(MainDir+'/'+Sub, extension, path))
    return SubDirs, Files

def Barriers_Keywords():
    MainDir = '/home/polo/.config/spyder-py3/Barriers Identification/Barriers DashBoard/Barriers'

    Barriers = dict((Sub,{}) for Sub in List_Dirs(MainDir))

    for Sub in Barriers.keys():
        Files = List_Files(MainDir+'/'+Sub, 'txt', path=False)
        Barriers[Sub] = dict((F.replace('.txt',''),{}) for F in Files)
        
        for F in Barriers[Sub].keys():
            with open(MainDir+'/'+Sub+'/'+F+'.txt', 'r') as f:
                 keywords = f.read().strip().split('\n')
                 Barriers[Sub][F] = dict((keyword,0) for keyword in keywords)
    return Barriers
                
def List_keywords():
    MainDir = '/home/polo/.config/spyder-py3/Barriers Identification/Barriers DashBoard/Barriers'

    SubDirs, Files = List_Dirs_and_Files(MainDir, 'txt', path=True)
    keywords = list()
    
    for File in Files:
        with open(File, 'r') as f:
             keywords.extend(f.read().strip().split('\n'))
    return list(set(keywords))
   
def Load_Discussions(JasonFile):
    with open(JasonFile, 'r') as fp:
         Pages = json.load(fp)
    MsgList = []
    for Page in Pages.values():
        #print(Page['title'],'\n_______________\n')
        for ListMsg in Page['Pages'].values():
            for text in ListMsg:
                sentences = sent_tokenize(text)
                for sentence in sentences:
                    if len(sentence) > 2:
                       MsgList.append(sentence)
    return MsgList 
    
def keywords_Discussion_Matching():
    keywords = List_keywords()
    MsgList = Load_Discussions('Fastlane.json')
    
    keywordsDict = dict((key,list()) for key in keywords)

    #Str1 = ' '.join(map(str, MsgList))
    for Str1 in keywords:
        Ratio = list()
        Partial_Ratio = list()
        Token_Sort_Ratio = list()
        Token_Set_Ratio = list()
        
        for Str2 in MsgList:
            Ratio.append(fuzz.ratio(Str1.lower(),Str2.lower()))
            Partial_Ratio.append(fuzz.partial_ratio(Str1.lower(),Str2.lower()))
            Token_Sort_Ratio.append(fuzz.token_sort_ratio(Str1,Str2))
            Token_Set_Ratio.append(fuzz.token_set_ratio(Str1,Str2))
            
        keywordsDict[Str1] = [Ratio,Partial_Ratio,Token_Sort_Ratio,Token_Set_Ratio]    
        #print(Ratio)
        #print(Partial_Ratio)
        #print(Token_Sort_Ratio)
        #print(Token_Set_Ratio)
        print ('\n_______________'+Str1+'______________\n')
    return keywordsDict

def keywords_Frequencies(JasonFile):
    with open(JasonFile, 'r') as f:
         keywordsDict = json.load(f)
    Dictionary = {}
    #keys = ['Ratio','Partial_Ratio','Token_Sort_Ratio','Token_Set_Ratio']
    #new_dict = dict(zip(keys, values))
    for keyword in keywordsDict.keys():
        Frequencies = list()
        for Ratios in keywordsDict[keyword]:
            Ratio = list(set(Ratios))
            Frequency = sum([1 for R in Ratio if R > round(mean(Ratio),2)])
            
            Frequencies.append(Frequency)
        Dictionary[keyword] = Frequencies    
    return Dictionary

def Sum_Dictionary(Dict,N):
    a = np.array(list(Dict.values()))
    Sum = np.sum(a, axis=0).tolist()[N]
    return Sum

def Trade_Barriers_Proportion(N):
    Dictionary = keywords_Frequencies('keywordsDict.json')
    Barriers = Barriers_Keywords()
    
    Sum = Sum_Dictionary(Dictionary,N)
    
    for Type in Barriers.keys():
        for Barrier in Barriers[Type].keys():
            for keyword in Barriers[Type][Barrier].keys():
                Barriers[Type][Barrier][keyword] = Dictionary[keyword][N] /Sum  
    return Barriers
 
#keywordsDict = keywords_Discussion_Matching()

Barriers = Trade_Barriers_Proportion(0)
