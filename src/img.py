
from PIL import Image
import urllib, cStringIO
from random import randint

f = open("memez.txt","r")
memez = f.readlines()




URL = memez[randint(0,len(memez))]
file = cStringIO.StringIO(urllib.urlopen(URL).read())
img = Image.open(file)
basewidth = 1500
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)

img.show()
