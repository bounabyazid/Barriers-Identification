from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment

link = "https://www.thefastlaneforum.com/community/search/36101691/?q=trade+barrier&o=date"

def getPages(link):
    over=urlopen(link).read()
    #print (over)
    soup = BeautifulSoup(over, features="lxml")

    Links = []
    Pages = soup.find('div',attrs={"class":"PageNav"}).find('nav')

    for page in Pages.findAll('a'):
        link = page.attrs['href']
        #print (link,'\n.......................\n')
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
            #print (res.find('blockquote',attrs={"class":"snippet"}).text,'\n________________________\n')
            Comments.append(res.find('blockquote',attrs={"class":"snippet"}).text)
            Pages[Links.index(link)] = Comments
    return Pages

Pages = getComments(getPages(link))

'https://community.startupnation.com/search?Search=russia+trade+barrier'