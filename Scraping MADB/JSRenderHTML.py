import re
import json
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment

# imports
import pandas as pd
import os

import requests

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import pandas as pd

import sys  
from PySide.QtGui import *  
from PySide.QtCore import *  
from PySide.QtWebKit import QWebPage  
from lxml import html 

class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit()
    

def retrive(url):
    #This does the magic.Loads everything
    r = Render(url)  
    #result is a QString.
    page = r.frame.toHtml()

    soup = BeautifulSoup(page, 'html.parser')
    #Table = soup.find('table', class_='ng-scope ng-table')

    #DictTable = {}
    #for T in Table.find_all('span', class_='ng-binding sort-indicator'):
    #    print(T.text)

    TBody = soup.find('tbody')
    for T in TBody.find_all('a', class_='ng-binding'):
    #    print(T.text)
        print('https://madb.europa.eu/madb/'+T['href'])

    print('________________________________________________________________________')


    for Tr in TBody.find_all('tr', class_='ng-scope'):
        for T in Tr.find_all('td'):
            print(T.text)
        print('____________________________________')
    

    #for T in TBody.find_all('tr', class_='ng-scope'):
    #    print(T.text) ok
    

    #for T in TBody.find_all('td', data-title-text='Country'):
    #    print(T.text)

#def get_links(url):
    
retrive(urls[0])
