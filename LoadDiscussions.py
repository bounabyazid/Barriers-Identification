#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:06:53 2019

@author: polo
"""
import os
import json
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
    
def Trade_Barriers_Proportion():
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
keywordsDict = Trade_Barriers_Proportion()