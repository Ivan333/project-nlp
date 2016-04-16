import textUrlRegex
import cpickleUrlReader
import urllib2
import re
import time
import anydbm
import cPickle
from bs4 import BeautifulSoup

#Global variable. Contains url and mk text
visitedURLs = []

#visited domains and urls
visited_domains = {}
#discovered domains, visit later
discovered_domains = []

def openWebsite(url):
    global visitedURLs

    website = urllib2.urlopen(url, timeout=5)
    website_html = website.read()
    
    website.close()
    
    return website_html

#find links in url from .mk domain
def findUrlsFromDomain(url):
    try:
        global visited_domains
        global discovered_domains
        global visitedURLs
        
        links = []

        domainSplit = url.split('/')
        #contains only the domain of url
        domain = "/".join(domainSplit[:3])
        if domain not in visited_domains: visited_domains[domain] = {}
        if url in visited_domains[domain]: return
            
        visitedURLs.append(url)
        if len(visitedURLs) % 10 == 0: print 'visited urls:', len(visitedURLs)
        
        website_html = openWebsite(url)        
        visited_domains[domain][url] = website_html
        
        soup = BeautifulSoup(website_html)
        for link in soup.findAll('a'):
            link = link.get('href')
            if "mailto:" in link: continue
            if not link.startswith('http'): link = domain + link               
            link_domain = "/".join(link.split("/")[:3])
            
            if not link_domain.endswith(".mk"): continue     
            if not link_domain == domain and link_domain not in discovered_domains: 
                discovered_domains.append(link_domain)
            
            if link_domain == domain:
                links.append(link)
        
        print url, len(links)
        return links

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
        if not url.startswith('http'): return
        if url in visited_domains: return
        
        urls = findUrlsFromDomain(url)
        if urls:
            for url1 in urls:
                visitSite(n-1, url1)
        return

#write url and mk text to disk using cpickle and anydbm
def urlWriter():

    f = anydbm.open('mk_html.anydbm', 'c')
    f["0"] = cPickle.dumps(visited_domains, 2)
    f.close()

    f = open('doscovered_domains.txt','w')
    for domain in discovered_domains: f.write(domain + '\n')
    f.close()

#write url and mk text to txt file
def urlReader():
    f1 = open('rez.txt', 'w')

    for domain in visited_domains:
        for url in visited_domains[domain]:
            f1.write( url +"\n" + visited_domains[domain][url] +"\n\n" )

    f1.close()

def main():
    global visited_domains
    global discovered_domains
    url='http://sitel.com.mk/'
    depth = 4 #depth of recursive search
    
    #db = anydbm.open("mk_html.anydbm",)
    #visited_domains = cPickle.loads(db["0"])  
    #db.close()
    
    #for domain in open("discovered_domains.txt"):
        #discovered_domains.append(domain)
    
    start = time.time()

    i = 0
    #for line in open('foundDomains.txt'):
    #i += 1
    #if i < 200021: continue

    visitSite(depth, url) #search mails and phone numbers in url

    #if i % 1 == 0: print 'domains visited', i
    #stopping criteria
    #if i == 210000:
        #break

    urlWriter()
    end = time.time()


    #human readable mk text written in rez.txt
    urlReader()

    #print 'Domains:', len(websiteURLs)
    #print 'Found:  ', len(foundURLs)
    #print 'Visited:', len(visitedURLs)
    print 'Time:   ', (end - start) / 60, 'm'

if __name__ == '__main__':    
    #main()
    findUrlsFromDomain("http://sitel.com.mk/tv-programa?qt-tv_programa=1#qt-tv_programa")
