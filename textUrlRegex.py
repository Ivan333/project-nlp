import sys
import urllib2
import re
from bs4 import BeautifulSoup


url = 'http://www.makdenes.org/content/article/27562059.html'
req = urllib2.Request(url, headers={'User-Agent' : 'Magic Browser'})
html = urllib2.urlopen(req).read()

soup = BeautifulSoup(html, "lxml")

for script in soup(['script','style']):
    script.extract()

text = soup.get_text()

text = text.split("\n")

f = open("text.txt","w")
for line in text:
    line = line.strip()
    if len(line) > 50:
        f.write(line.encode("utf-8") + "\n\n")
f.close()
