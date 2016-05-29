import urllib2
import time
import anydbm
import cPickle
from bs4 import BeautifulSoup
import threading

# Global variable. Contains url and mk text
visitedURLs = []

# visited domains and urls
visited_domains = {}
# discovered domains, visit later
discovered_domains = []

urls = []
threadLock = threading.Lock()
num_threads = 100
db_name = "mk_html_threading.anydbm"


class MyThread(threading.Thread):
    def __init__(self, ThreadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = ThreadID
        self.name = name
        self.counter = counter

    def run(self):
        depth = 4
        threadLock.acquire()
        print "starting thread", self.threadID
        threadLock.release()
        for i in range(len(urls)/num_threads):
            index = i*num_threads + self.threadID
            #if index < 8000: continue

            url = urls[index]
            if url in visited_domains: continue
            visitSite(depth, url)

            threadLock.acquire()

            urlWriter(url)
            visited_domains[url] = 1
            print 'domain visited', index, url

            threadLock.release()

        threadLock.acquire()
        print "ending thread", self.threadID
        threadLock.release()


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


# find links in url from .mk domain
def findUrlsFromDomain(url):
    global visited_domains
    # global discovered_domains
    global visitedURLs

    links = []

    domainSplit = url.split('/')

    # contains only the domain of url
    domain = "/".join(domainSplit[:3])
    if domain not in visited_domains: visited_domains[domain] = {}
    if url in visited_domains[domain]: return

    visitedURLs.append(url)
    if len(visitedURLs) % 10 == 0: print 'visited urls:', len(visitedURLs)

    website_html = openWebsite(url)

    threadLock.acquire()
    visited_domains[domain][url] = website_html
    print url, len(links)
    threadLock.release()

    if not website_html: return

    soup = BeautifulSoup(website_html)
    for link in soup.findAll('a'):
        link = link.get('href')
        if not link: continue
        if "mailto:" in link: continue
        if not link.startswith('http'): link = domain + link
        link_domain = "/".join(link.split("/")[:3])

        if not link_domain.endswith(".mk"): continue
        # if not link_domain == domain and link_domain not in discovered_domains:
        # discovered_domains.append(link_domain)

        if link_domain == domain:
            links.append(link)

    threadLock.acquire()
    print url, len(links)
    threadLock.release()

    return links


# recursive visit of sites in url's domain up to depth n
def visitSite(n, url):
    if n == 0:
        return
    else:
        if not url.startswith('http'): return

        urls = findUrlsFromDomain(url)
        if urls:
            for url1 in urls:
                visitSite(n - 1, url1)
        return


# write url and mk text to disk using cpickle and anydbm
def urlWriter(url):
    f = anydbm.open(db_name, 'c')
    try:
        f[url] = cPickle.dumps(visited_domains[url], 2)
    except Exception as e:
        #error_f = open('error_log_new.txt', 'a')
        #error_f.write(url.strip() + ": " + str(e) + "\n")
        #error_f.close()
        pass
    f.close()

    # f = open('discovered_domains1.txt', 'a')
    # for domain in discovered_domains: f.write(domain.strip() + '\n')
    # f.close()


def main():
    global visited_domains
    global urls
    # global discovered_domains
    # url='http://motojove.com.mk'
    depth = 4  # depth of recursive search

    db = anydbm.open(db_name)
    i = 0
    for url in db.keys():
        i+=1
        if i%100 == 0: print i
        visited_domains[url] = 1
    db.close()

    # for domain in open("discovered_domains1.txt"):
    # discovered_domains.append(domain)

    start = time.time()

    urls = []
    for url in open("found_domains_new.txt"):
        urls.append(url.strip())

    threads = [MyThread(i, "Thread-" + str(i), 1) for i in range(num_threads)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = time.time()

    # human readable mk text written in rez.txt
    # urlReader()

    # print 'Domains:', len(websiteURLs)
    # print 'Found:  ', len(foundURLs)
    # print 'Visited:', len(visitedURLs)
    print 'Time:   ', (end - start) / 60, 'm'


if __name__ == '__main__':
    main()
    # findUrlsFromDomain("http://motojove.com.mk")
