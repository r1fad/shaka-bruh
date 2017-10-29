from urllib import FancyURLopener
import json
from bs4 import SoupStrainer, BeautifulSoup
import time


#Class to provide custom user header to prevent
#blocking by Google\'s bot watchers.
class MyOpener(FancyURLopener):
  version = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
openurl = MyOpener().open

count = 0
url = 'https://www.reddit.com/r/dankmemes/?count=0&after=t3_798vdy'
myfile = open('dankmemes.txt','w')
while url:
    base_url = 'https://www.reddit.com/r/dankmemes/.json' + url[35:]
    page = BeautifulSoup(openurl(url).read(),"lxml")
    data = json.loads(openurl(base_url).read())
    for meme in data["data"]["children"]:
        meme_url = meme["data"]["url"]
        myfile.write(meme_url+"\n")
        count += 1
    next_button = page.find('span', {'class':'next-button'})
    url = next_button.find('a')['href']

print count
