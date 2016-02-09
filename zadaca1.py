__author__ = 'Ivan'
#encoding: utf-8

import re
from crawler import Crawler, CrawlerCache
import urllib
import sys

"""
Ivan:

The code testid on finki.ukim.mk
crawler can be found on: https://gist.github.com/debrice/a34563fb078d9d2d15e8

"""
def get_mail_matcher():
    #this: ([\w\.-\\,]+)(\s*[Aa][Tt]\s*|@)([\w\.-]+\s*[Dd][Oo][Tt]\s*[\w\.-]*|[\w\.-]+) can find mails as ivan at  finki dot com
    # or ivan,petre,stanko@something.something...
    mail_match = re.compile(r'([>]?)([\w\.-\\,]+@[\w-]+\.[\w\.-]+)([<]?)|([\w\.-\\,]+\s*[Aa][Tt]\s*[Dd][Oo][Tt]\s*[\w\.-])')
    return mail_match

def get_phone_matcher():
    ## better solution is to use regex library, but this gets the job done
    numberSixTimes = r'[\s/\.\\\-]*\d'
    numberSixTimes*=5
    numberSixTimes = r'[\s/\\\-]{1,4}\d' + numberSixTimes

    numberSevenTimes = r'[\s/\.\\\-]*\d'
    numberSevenTimes*=6
    numberSevenTimes = r'[\s/\\\-]{1,4}\d' + numberSevenTimes

    numberSixTimes2 = r'[\s/\.\\\-]*\d'
    numberSixTimes2*=6

    #r'(\+389)?[\s/\.\\]*(02'+numberSevenTimes+'|0\d\d'+numberSixTimes+')'(\+389)?[\s/\.\\]*
    phone_match = re.compile(r'\+389?[\s/\.\\\-]*0?2'+numberSevenTimes+'|0?\d\d'+numberSixTimes)
    return phone_match

def match_string(string, mail_matcher,phone_matcher):
    if not string:
        return -1
    matched_mails = mail_matcher.findall(string)
    if matched_mails:
        for mail_match in matched_mails:
            print mail_match[1]+mail_match[3] + ' email'

    matched_phones = phone_matcher.findall(string)
    if matched_phones:
        for phone_match in matched_phones:
            print phone_match + ' phone'

def wget2(url):
    try:
        ufile = urllib.urlopen(url)
        if ufile.info().gettype() == 'text/html':
          return ufile.read()
    except IOError:
        print 'problem reading url:', url


def main():
    args = sys.argv[1:]

    if not args:
        print 'usage: domain [domain ...]'
        sys.exit(1)

    for domain in args:

        crawler = Crawler(CrawlerCache('crawler.db'), depth=3)
        print 'Checking urls in database for ' + domain + ' ...'
        crawler.crawl(domain, no_cache=re.compile('^/$').match)

        urls = crawler.content[crawler.domain].keys()


        mail_matcher = get_mail_matcher()
        phone_matcher = get_phone_matcher()

        for url in urls:
            text = crawler.curl(url)
            #print 'For url: ' + content_url+url + ' we found the folowing phones and emails:'
            match_string(text,mail_matcher,phone_matcher)


    return

if __name__ == '__main__':
    main()