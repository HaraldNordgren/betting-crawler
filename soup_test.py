#!/usr/bin/env python3

#from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
import urllib, sys

class MyOpener(urllib.request.FancyURLopener):
    version = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'

urllib._urlopener = MyOpener()

url = 'https://www.nordicbet.com/sv/odds#/#?cat=&reg=&sc=3'

#myopener = MyOpener()
#content = myopener.open(url)
#sys.exit(0)

#headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36' }
#headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' }
#headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' }
#headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0' }

content         = urllib.request.urlopen(url).read()
soup            = BeautifulSoup(content, 'html.parser')
sys.exit(0)

#req = urllib.request.Request(url, headers=headers)

#content = urllib.request.urlopen(req).read()
soup    = BeautifulSoup(content, 'html.parser')

odds    = soup.find('iframe', attrs={'id':'SportsbookIFrame'})
print(odds['src'])
