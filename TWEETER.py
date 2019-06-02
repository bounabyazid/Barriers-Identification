#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 07:29:15 2018

@author: polo
"""
import os
import tweepy #https://github.com/tweepy/tweepy
import sys
import json

import xlsxwriter

import pickle
import pandas as pd

#https://github.com/tweepy/tweepy

#Twitter API credentials

def load_api():
    with open('twitter_credentials.json') as cred_data:
         info = json.load(cred_data)
     
    CONSUMER_KEY = info['CONSUMER_KEY']
    CONSUMER_SECRET = info['CONSUMER_SECRET']
    ACCESS_TOKEN = info['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = info['ACCESS_TOKEN_SECRET']
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    return tweepy.API(auth, wait_on_rate_limit=True)

def process_tweet(tweet):  
    d = {}
    d['id_str'] = tweet.id_str
    d['text'] = tweet.text
    d['user'] = tweet['user']['screen_name']
    d['user_loc'] = tweet['user']['location']
    d['hashtags'] = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
    return d

def write_tweets(tweets, filename): 
    with open(filename, 'a') as f:
         for tweet in tweets:
             json.dump(tweet._json, f)
             f.write('\n')

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

def Search_Trade_Barrieres(query):
    api = load_api()
    queries = List_keywords()
    tweets = {}
    for query in queries:
        tweets[query] = api.search(query, count=200)
        
    with open('tweets.pkl', 'wb') as handle:
         pickle.dump(tweets, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return tweets#List_tweets

def get_tweets(keyword, numOfTweets):
    #https://www.programcreek.com/python/example/76301/tweepy.Cursor
    # Iterate through all tweets containing the given word, api search mode
    api = load_api()

    
    keywords = List_keywords()
    tweets = {}
    for keyword in keywords:
        listOfTweets = []
        for tweet in tweepy.Cursor(api.search, q=keyword).items(numOfTweets):
            # Add tweets in this format
            dict_ = {'Screen Name': tweet.user.screen_name,
                'User Name': tweet.user.name,
                'Tweet Created At': tweet.created_at,
                'Tweet Text': tweet.text,
                'User Location': tweet.user.location,
                'Tweet Coordinates': tweet.coordinates,
                'Retweet Count': tweet.retweet_count,
                'Retweeted': tweet.retweeted,
                'Phone Type': tweet.source,
                'Favorite Count': tweet.favorite_count,
                'Favorited': tweet.favorited,
                'Replied': tweet.in_reply_to_status_id_str
                }
            listOfTweets.append(dict_)
        tweets[keyword] = listOfTweets
        
    with open('Curssor tweets.pkl', 'wb') as handle:
         pickle.dump(tweets, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return tweets

def LoadTweets(file):
    Columns = ['Category', 'Type', 'keyword', 'Screen Name', 'User Name',
               'Tweet Text', 'Year', 'User Location', 'Tweet Coordinates']
                
    df = pd.DataFrame(columns=Columns)
    
    rows = []
    
    with open(file, 'rb') as handle:
         tweets = pickle.load(handle)

    DictFilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])

    wanted_keys = ('Screen Name','User Name','Tweet Text', 'Tweet Created At', 'User Location', 'Tweet Coordinates')
    
    for key in tweets.keys():
        for tweet in tweets[key]:
            row = ['','',key]+list(DictFilt(tweet, wanted_keys).values())
            rows.append(row)
    for row in rows:
        df.loc[len(df)] = row
    return tweets, df
         
#tweets = Search_Trade_Barrieres('')
#MessAround('tweets.pkl')


#tweets = get_tweets('trade barriers', 1000)
tweets, df = LoadTweets('Curssor tweets.pkl')         
