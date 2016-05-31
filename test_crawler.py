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
    website_html = ""
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        if response.info().getheader('Content-Type').split(";")[0] == "text/html":
            website = urllib2.urlopen(url, timeout=1)
            website_html = website.read()

            website.close()
    except Exception as e:
        print "openWebsite %s error: %s" % (url, e) 

    return website_html


#find links in url from .mk domain
def findUrlsFromDomain(url):
    global visited_domains
    #global discovered_domains
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
    if not website_html: return
        
    soup = BeautifulSoup(website_html)
    for link in soup.findAll('a'):
        link = link.get('href')
        if not link: continue
        if "mailto:" in link: continue
        if not link.startswith('http'): link = domain + link
        link_domain = "/".join(link.split("/")[:3])

        if not link_domain.endswith(".mk"): continue
        #if not link_domain == domain and link_domain not in discovered_domains:
            #discovered_domains.append(link_domain)

        if link_domain == domain:
            links.append(link)

    print url, len(links)
    return links


#recursive visit of sites in url's domain up to depth n
def visitSite(n, url):
    if n==0:
        return
    else:
        if not url.startswith('http'): return

        urls = findUrlsFromDomain(url)
        if urls:
            for url1 in urls:
                visitSite(n-1, url1)
        return


#write url and mk text to disk using cpickle and anydbm
def urlWriter(url):
    f = anydbm.open('mk_html_new.anydbm', 'c')
    try:
        f[url] = cPickle.dumps(visited_domains[url], 2)
    except Exception as e:
        error_f = open('error_log.txt', 'a')
        error_f.write(url.strip() + ": " + str(e) + "\n")
        error_f.close()
    f.close()

    #f = open('discovered_domains1.txt', 'a')
    #for domain in discovered_domains: f.write(domain.strip() + '\n')
    #f.close()


#write url and mk text to txt file
def urlReader():
    f1 = open('rez.txt', 'w')

    for domain in visited_domains:
        for url in visited_domains[domain]:
            f1.write( url + "\n" + visited_domains[domain][url] + "\n\n" )

    f1.close()


def main():
    global visited_domains
    #global discovered_domains
    depth = 4 #depth of recursive search
    
    db = anydbm.open("mk_html_new.anydbm")
    for url in db:
        visited_domains[url] = 1
    db.close()

    #for domain in open("discovered_domains1.txt"):
        #discovered_domains.append(domain)
    
    start = time.time()

    i = 0
    for url in open('found_domains_new.txt'):
        i += 1
        url = url.strip()

        if url in visited_domains: continue
        visitSite(depth, url)
        urlWriter(url)

        visited_domains[url] = 1
    
        if i % 1 == 0: print 'domains visited', i
        #stopping criteria
        #if i == 1500:
            #break

    end = time.time()


    #human readable mk text written in rez.txt
    #urlReader()

    #print 'Domains:', len(websiteURLs)
    #print 'Found:  ', len(foundURLs)
    #print 'Visited:', len(visitedURLs)
    print 'Time:   ', (end - start) / 60, 'm'

if __name__ == '__main__':
    main()
    #findUrlsFromDomain("http://motojove.com.mk")
