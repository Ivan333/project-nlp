#Extract all MK phone numbers & emails from a given domain, to depth 3
#Change URL in def main to choose domain
#Change depth in def main to choose depth

import sys
import urllib2
import re

websiteURLs = [] #Global variable. Contains all URLs found using findUrlsFromDomain(url).

def findUrlsFromDomain(url): #find links on this page from url's domain
    try:
        global websiteURLs
        website = urllib2.urlopen(url)
        website_html = website.read()
        domainSplit = url.split('/')
        urlDomainName = domainSplit[0]+'/'+domainSplit[1]+'/'+domainSplit[2]#contains only the domain of url

        #find all (<a href="*") strings in website_html
        urlMatchesText = re.findall(r'\<a ?.* ?href=[\"\'][^\"\']*[\"\']',website_html)

        #contains all website urls from urlDomainName
        websiteLinks=[]

        #finds all website urls from urlDomainName
        for urlMatchText in urlMatchesText:
            urlMatches = re.findall(r'href=[\"\'][^\"\']*[\"\']',urlMatchText)#find all hrefs
            for urlMatch in urlMatches:
                link=urlMatch[6:-1]#get only contents of href
                checkFileType = re.search(r'(?:.webm$|.mp4$|.doc$|.pdf$|.jpg$|.png$|.gif$|.image$|.pdf$|.jpeg$|.jfif$|.mpg$|.mpeg$|.ps$|.tar$|.txt$|.wav$|.zip$|.css$|.js$)',link)
                if not checkFileType: #don't open a link if it leads to a file with the above extensions
                    checkDomain = re.search(r'(?:http://|https://|http://www.|https://www.|//www.|//)',link)
                    if (checkDomain): #if link contains http, https or //, check if different domain
                        if not link in websiteURLs: #add link only if its not in global variable websiteURLs
                            websiteLinks.append(link)
                            websiteURLs.append(link)
                        else: #it must be from the same domain
                            checkPath=re.search(r'^\/',link) #check if root path
                            checkAnchor=re.search(r'^#',link) #if link has # at the start, it's an anchor link from the same page
                            if not checkAnchor and checkPath:
                                if not urlDomainName+link in websiteURLs: #add link only if its not in global variable websiteURLs
                                    websiteLinks.append(urlDomainName+link)
                                    websiteURLs.append(urlDomainName+link)

        website.close()

        return websiteLinks

    except:
        pass


def visitSite(n, url): #recursively find all emails and phones from links in url's domain up to depth n
    if n==0:
        return
    else:
        urls = findUrlsFromDomain(url)
        for url1 in urls:
            visitSite(n-1,url1)
        return

def main():
    url='http://time.mk'
    depth=1 #depth of recursive search

    visitSite(depth,url) #search mails and phone numbers in url
    for url in websiteURLs:
        print url

if __name__ == '__main__':
    main()
