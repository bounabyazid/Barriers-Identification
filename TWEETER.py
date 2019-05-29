#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 07:29:15 2018

@author: polo
"""
import tweepy #https://github.com/tweepy/tweepy
import csv
import sys
import json

import xlsxwriter
import tweepy 

#https://github.com/tweepy/tweepy

#Twitter API credentials

CONSUMER_KEY = 't1Ek5mAT0FAz92spNP17Qlrlk'
CONSUMER_SECRET = 'LvG5kTtSRX8l0QboweGqRFn3PM5gHpzV4QHF1ZMvUGvrEWgQF9'
ACCESS_TOKEN = '2931812891-akZSXEvx1cZVipK4qNmmVlJ03d18a4Umn1bH938'
ACCESS_TOKEN_SECRET = 'V92DE1iNOLUtdigJLwVgqoSdTW9FEeF7dUc90F9xJrazM'

def process_tweet(tweet):  
    d = {}
    #d['hashtags'] = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
    d['text'] = tweet.text
    d['user'] = tweet['user']['screen_name']
    d['user_loc'] = tweet['user']['location']
    return d

def Search_Trade_Barrieres():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
     
    tweets = api.search('trade barriers', count=200)
    List_tweets = [[tweet.id_str, tweet.created_at, tweet.coordinates, tweet.user.location ,tweet.geo, tweet.source, tweet.text] for tweet in tweets]
 
    #for tweet in List_tweets:
    #    Dict = {'created_at' : '', 'id': '', 'id_str': '', 'text': '', 'user': {}, 'entities': {}}
    #    [tweet.id_str, tweet.created_at, tweet.coordinates,tweet.geo,tweet.source,tweet.text]
    
    return List_tweets
    
outtweets = Search_Trade_Barrieres()