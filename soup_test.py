from bs4 import BeautifulSoup

#headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36' }
headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' }

req = urllib.request.Request(
        url,
        data=None,
        headers=headers )

content = urllib.request.urlopen(req).read()
soup    = BeautifulSoup(content, 'html.parser')

odds    = soup.find('iframe', attrs={'id':'SportsbookIFrame'})
print(odds['src'])
