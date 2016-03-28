# project-nlp


TODO:
MK	corpus
- Crawl	web	sites	from provided	list	od	domains. Remove	duplicate	sites.
		(http://nlp.finki.ukim.mk/domeni.txt )
- Crawl	web	site	till	4th level.	Root	page	is	1st level.
- Also	crawl	all	domains	(.mk)	that	are	found	on crawled	websites.
- Save	all	crawled	pages
- Extract	MK	text	(MK	text	if	50+%	predefined	MK	words)
- Approximate	Duplicate	detection	(50+%	equal	4-grams)
- OUTPUT:	One	BIG	text	file
- 

#Documentation

Main aplication logic is in crawler.py here we have the crawling logic(note current version limits to 20k web pages:
```python
#Global variable. Contains all .mk domains
websiteURLs = []
#Global variable. Contains all URLs found using findUrlsFromDomain(url).
foundURLs = []
#Global variable. Contains all visited urls
visitedURLs = []
#already visited domains, do not visit again
alreadyVisited = []
#Global variable. Contains url and mk text
downloadedURLs = {}



def openWebsite(url):
    global visitedURLs

    website = urllib2.urlopen(url)
    website_html = website.read()
    website.close()

    return website_html

#find links in url from .mk domain
def findUrlsFromDomain(url):
    try:
        global websiteURLs
        global foundURLs

        #if already visited, do not open
        if url in visitedURLs or url in alreadyVisited: return
        if not url.startswith('http'): return

        website_html = openWebsite(url)
        #save website html
        mk_text = textUrlRegex.readText(website_html)
        downloadedURLs[url] = mk_text
        visitedURLs.append(url)

        if len(visitedURLs) % 10 == 0: print 'visited urls:', len(visitedURLs)

        domainSplit = url.split('/')
        #contains only the domain of url
        urlDomainName = domainSplit[0]+ '/' + domainSplit[1]+ '/' + domainSplit[2]

        #find all (<a href="*") strings in website_html
        urlMatchesText = re.findall(r'\<a ?.* ?href=[\"\'][^\"\']*[\"\']', website_html)

        #contains all website urls from urlDomainName
        websiteLinks=[]

        #finds all website urls from urlDomainName
        for urlMatchText in urlMatchesText:
            #find all hrefs
            urlMatches = re.findall(r'href=[\"\'][^\"\']*[\"\']', urlMatchText)
            for urlMatch in urlMatches:
                #get only contents of href
                link = urlMatch[6:-1]
                checkFileType = re.search(r'(?:.webm$|.mp4$|.doc$|.pdf$|.jpg$|.png$|.gif$|.image$|.pdf$|.jpeg$|.jfif$|.mpg$|.mpeg$|.ps$|.tar$|.txt$|.wav$|.zip$|.css$|.js$)', link)
                #don't open a link if it leads to a file with the above extensions
                if not checkFileType:
                    checkDomain = re.search(r'(?:http://|https://)', link)
                    #if link contains http, https or //, check if different domain
                    if (checkDomain):
                        checkDomainName = re.search(r'\.mk', link)
                        #if link contains .mk this link is from the same domain
                        if checkDomainName:
                            addNewWebsite(link)
                            if link not in foundURLs: foundURLs.append(link)
                            if re.search(urlDomainName, link): websiteLinks.append(link)
                    #it must be from the same domain
                    else:
                        #check if root path
                        checkPath=re.search(r'^\/', link)
                        #if link has # at the start, it's an anchor link from the same page
                        checkAnchor=re.search(r'^#', link)
                        if not checkAnchor and checkPath:
                            if not urlDomainName + link in foundURLs:
                                websiteLinks.append(urlDomainName + link)
                                foundURLs.append(urlDomainName + link)

        return websiteLinks

    except:
        pass

#if new, add this url to websiteURLs
def addNewWebsite(link):
    global websiteURLs

    link = link.split('/')
    url = link[0] + '/' + link[1] + '/' + link[2]

    if url not in websiteURLs:
        websiteURLs.append(url)

    return True


#recursive visit of sites in url's domain up to depth n
def visitSite(n, url):
    if n==0:
        return
    else:
        urls = findUrlsFromDomain(url)
        if urls:
            for url1 in urls:
                visitSite(n-1, url1)
        return

#write url and mk text to disk using cpickle and anydbm
def urlWriter():
    global websiteURLs
    global foundURLs
    global visitedURLs

    f = anydbm.open('cpickle_mk_text.anydbm', 'c')
    for url in downloadedURLs:
        text = downloadedURLs[url]
        f[url] = cPickle.dumps(text, 2)
    f.close()
    downloadedURLs.clear()

    f = open('foundDomains.txt','a')
    if len(websiteURLs) > 0:
        for url in websiteURLs: f.write(url + '\n')
    f.close()
    del websiteURLs[:]

    f = open('foundURLs.txt','w')
    if len(foundURLs) > 0:
        for url in foundURLs: f.write(url + '\n')
    f.close()
    del foundURLs[:]

    f = open('visitedURLs.txt','a')
    if len(visitedURLs) > 0:
        for url in visitedURLs:
            f.write(url + '\n')
            if url not in alreadyVisited: alreadyVisited.append(url)
    f.close()
    del visitedURLs[:]

#write url and mk text to txt file
def urlReader():
    f = anydbm.open('cpickle_mk_text.anydbm', 'r')
    f1 = open('rez.txt', 'w')

    for k in f.keys():
        f1.write(k.split('\n')[0] + '\t' + cPickle.loads(f[k]).replace('\n', '').replace('\r', '') + '\n')

    f.close()
    f1.close()

def main():
    global downloadedURLs
    global visitedURLs
    #url='http://www.time.mk/'
    depth = 3 #depth of recursive search

    start = time.time()

    for url in open('visitedURLs.txt'):
        alreadyVisited.append(url)

    i = 0
    for line in open('foundDomains.txt'):
        i += 1
        if i < 200021: continue

        visitSite(depth, line) #search mails and phone numbers in url

        if i % 1 == 0: print 'domains visited', i
        #every 100 downloaded sites, write to disk and clear ram
        if len(downloadedURLs) > 100:
            urlWriter()
        #stopping criteria
        if i == 210000:
            urlWriter()
            break

    urlWriter()
    end = time.time()


    #human readable mk text written in rez.txt
    urlReader()

    #print 'Domains:', len(websiteURLs)
    #print 'Found:  ', len(foundURLs)
    #print 'Visited:', len(visitedURLs)
    print 'Time:   ', (end - start) / 60, 'm'

if __name__ == '__main__':
    main()
```

result form crawler can be seen here: https://drive.google.com/file/d/0B6l1fZCJ7OnGVTBFX0tMV2U5Z2c/view?pref=2&pli=1 


mkText.py contains MkTextChecker with methods to check macedonian words from dictionary

```python

class MkTextChecker:

    #constructor with dictionaryName
    def __init__(self, dictionaryName):
        self.t = open(dictionaryName, 'r').read()

    # check text returns T if contains 50% or more macedonian words F otherwise
    def checkMkText(self,text):
        countT = 0
        countF = 0
        words = text.split()
        wordsLen = len(words)
        for word in words:
            if(self.checkMkWord(word)):
                countT+=1
            else:
                countF+=1
            if(countT >= wordsLen/2.0):
                return True
            elif(countF >= wordsLen/2.0):
                return False
        return False
    #if word is macedonian returns T, F otherwise
    def checkMkWord(self,word):
        if(self.t.find(word) != -1):
            return True
        return False
```


4gram.py is where MkTextChecker is called and where we do duplicate detection

```python

# -*- coding: utf-8 -*-


#initialise global variables
text = {}
fourgram = {}

checkerMk = MkTextChecker("wfl-mk.tbl")

i = 0

#read texts from file
for line in open("rez.txt"):
    i+=1
    split = line.split('\t')
    if(checkerMk.checkMkText(split[1])):
        text[split[0]] = split[1]
        print split[0]
    if i == 200:
        break;

#create fourgrams
for i in text.keys():
    fourgram[i] = set()
    words = text[i].split()
    for n in range(len(words) - 3):
        fourgram[i].add( ' '.join( words[n : n + 4] ) )



#duplicate detection
keys = fourgram.keys()
f1 = open('rezNoDuplicates.txt', 'w')

while len(keys) > 0:
    key = keys.pop()
    keysJ = list(keys)
    f1.write(key + '\t' + text[key])

    while len(keysJ) > 0:
        j = keysJ.pop()
        intersect = fourgram[key] & fourgram[j]
        #print "checking", text[j]
        #print "forgram ", fourgram[key], "fourgram", fourgram[j]
        #print "calculation", len(intersect) , len(fourgram[key]) / 2.0
        if len(intersect) >= len(fourgram[key])/2.0 and len(intersect) >= len(fourgram[j])/2.0:
            text.pop(j)
            keys.remove(j)
            fourgram.pop(j)

f1.close()

```


results can be seen here(note contains non mk text): https://onedrive.live.com/redir?resid=EE2C8D8A48D02330!1784&authkey=!AFfxuc4yA31kZLk&ithint=file%2ctxt

due to time constraints results with mk text with the first 200 pages can be seen here: https://onedrive.live.com/redir?resid=EE2C8D8A48D02330!1785&authkey=!AO1Axna9IWce2vo&ithint=file%2ctxt



