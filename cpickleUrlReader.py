import cPickle
import anydbm


def urlReader(fileName):
    websiteURLs = {}
    for line in open(filename):
        websiteURLs[line] = ' '

    f = anydbm.open('cpickle.anydmb', 'n')
    for url in websiteURLs:
        f[url] = websiteURLs[url]
