import json
from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment

link = 'https://community.startupnation.com/search?Search=trade+barrier'

def getPages(link):
    over=urlopen(link).read()
    soup = BeautifulSoup(over, features="lxml")

    Links = []
    Pages = soup.find('div',attrs={"class":"PageNav"}).find('nav')

    for page in Pages.findAll('a'):
        link = page.attrs['href']
        Links.append('https://www.thefastlaneforum.com/community/'+link)
    return Links

def getComments(Links):
    Pages = {}
    for link in Links:
        over=urlopen(link).read()
        soup = BeautifulSoup(over, features="lxml")
        Results = soup.findAll('li',attrs={"class":"searchResult post primaryContent"})
        Comments = []
        
        for res in Results:
            Dict = {}
            Dict['usernam'] = res.find('a',attrs={"class":"username"}).text
            Dict['title'] = res.find('h3',attrs={"class":"title"}).text
            Dict['Comment'] = res.find('blockquote',attrs={"class":"snippet"}).text
            Dict['DateTime'] = res.find('span',attrs={"class":"DateTime"})['title']
            Comments.append(Dict)
            
        Pages['Page'+str(Links.index(link))] = Comments
    return Pages

Links = getPages(link)
#Pages = getComments(getPages(link))

with open('Fastlane.json', 'w') as fp:
     json.dump(Pages, fp)

#with open('Fastlane.json', 'r') as fp:
#     Pages = json.load(fp)