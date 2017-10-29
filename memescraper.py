import urllib2
import pprint
import re
from urllib import FancyURLopener
from bs4 import BeautifulSoup
import simplejson as json
class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
openurl = MyOpener().open
file = open("memez2.txt","w")
url = "https://www.reddit.com/r/memes/?count=75&after=t3_797y0p"
for i in range(1,100):
    url2 = "https://www.reddit.com/r/memes/.json" + url[31:]
    data = json.loads(openurl(url2).read())
    for i in data["data"]["children"]:
        file.write(i["data"]["preview"]["images"][0]["source"]["url"] + "\n")
    soup = BeautifulSoup(openurl(url).read(), "lxml")
    #print soup.find("class = next_button")
    next = soup.find('span', {'class':'next-button'})
    url = next.find('a')['href']
    print url





'''
with open('memes.json') as data_file:
    data = json.load(data_file)

for i in data["data"]["children"]:
    print i["data"]["preview"]["images"][0]["source"]["url"]
'''
