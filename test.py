import time
import difflib
from bs4 import BeautifulSoup
from test_read_anydbm import *
from mkText import MkTextChecker
import multiprocessing
import re
from simhash import Simhash, SimhashIndex

checkerMk = MkTextChecker("wfl-mk.tbl")


def mk_text_diff(lines):

    if len(lines) >= 4:
        final_lines = []
        for line in lines:
            line = line[1:].strip()
            soup = BeautifulSoup(line, 'lxml')
            text = soup.getText().strip().encode("utf-8")
            if len(text) > 20 and checkerMk.checkMkText(text) and not text.endswith("..."):
                final_lines.append(text)
        if len(final_lines) >= 4:
            return final_lines
    else:
        return []


def site_content(domain, url):
    text1 = domains[domain][domain]
    text1_lines = text1.splitlines()

    text2 = domains[domain][url]
    text2_lines = text2.splitlines()

    d = difflib.Differ()
    diff = d.compare(text1_lines, text2_lines)
    lines = []
    content = []

    for line in diff:
        if line.startswith("+"):
            lines.append(line)
        else:
            rez = mk_text_diff(lines)
            if rez:
                content += rez
            lines = []

    for i, c in enumerate(content): print i, c

    return content


def test2():
    text1 = domains['http://www.sitel.com.mk']['http://www.sitel.com.mk/jelena-ja-ubil-razbojnik-od-zabel-so-koj-bila-vo-tajna-vrska']
    text1_lines = text1.splitlines()
    text2 = domains['http://www.sitel.com.mk']['http://www.sitel.com.mk']
    text2_lines = text2.splitlines()

    d = difflib.Differ()
    diff = d.compare(text1_lines, text2_lines)
    # print '\n'.join(diff)
    lines = []
    lines_minus = []

    for line in diff:
        if line.startswith("+"):
            lines.append(line)
        else:
            mk_text_diff(lines)
            lines = []


def test1():
    text1 = domains['http://www.sitel.com.mk']['http://www.sitel.com.mk/jelena-ja-ubil-razbojnik-od-zabel-so-koj-bila-vo-tajna-vrska']
    text1_lines = text1.splitlines()
    text2 = domains['http://www.sitel.com.mk']['http://www.sitel.com.mk']
    text2_lines = text2.splitlines()

    d = difflib.Differ()
    diff = d.compare(text1_lines, text2_lines)
    # print '\n'.join(diff)
    lines_plus = []
    lines_minus = []

    for i in diff:
        if i.startswith("+"):
            lines_plus.append(i)
            mk_text_diff(lines_minus)
            lines_minus = []
        elif i.startswith("-"):
            lines_minus.append(i)
            mk_text_diff(lines_plus)
            lines_plus = []


def count_sites():
    db = anydbm.open("mk_html_content_multitest.anydbm", "r")
    #print len(db)
    i = 0
    count = 0
    for k in db:
        if i % 10 == 0: print i
        i += 1
        site = cPickle.loads(db[k])
        count += len(site)
    print count
    db.close()


def multiproc_run(ns, start_num, finish_num, id):
    for i in range(start_num, finish_num):
        tmp = ns.dic
        tmp[i] = i * id
        ns.dic = tmp


def multiprocessing_test():
    mgr = multiprocessing.Manager()
    namespace = mgr.Namespace()
    namespace.dic = {"test": 1}
    event = mgr.Event()

    p = multiprocessing.Process(target=multiproc_run, args=(namespace, 1, 10, 1))
    c = multiprocessing.Process(target=multiproc_run, args=(namespace, 0, 10, 2))

    p.start()
    c.start()

    c.join()
    p.join()

    for i in namespace.dic:
        print i, namespace.dic[i]


def pool_process(data):
    return data*2


def pool_initializer():
    print "starting", multiprocessing.current_process().name


def pool_test():
    inputs = list(range(20))
    pool_size = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=pool_size, initializer=pool_initializer)

    pool_outputs = pool.map(pool_process, inputs)
    pool.close()
    pool.join()

    print pool_outputs


def write_txt():
    db = anydbm.open("mk_html_content_multitest.anydbm", "r")
    f = open("rez.txt", 'w')
    end = False
    i = 0
    j = 0
    k = 0
    for domain in db:
        site = cPickle.loads(db[domain])
        i+=1
        if i % 10 == 0: print i
        for url in site:
            #if len(site[url]) > 10:
            k += 1
            try:
                if len(site[url]) > 0:
                    f.write(url + '\t' + site[url].replace('\n', ' ').replace('\r', ' ') + '\n')
            except Exception as e:
                print e
                j += 1
                #print "text", site[url]
                end = True

    print j, k


    f.close()
    db.close()


def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def get_phrases(s):
    width = 3
    s = s.lower()
    s = s.split()
    start = 0
    end = start + width
    phrases = []
    while end <= len(s):
        for w in s[start:end]:
            phrases.append(w)
        start += 1
        end += 1
    return phrases


def simhash_test():
    data = {
        1: u'How are you? I Am fine. blar blar blar blar blar Thanks.',
        2: u'How are you i am fine. blar blar blar blar blar than',
        3: u'This is simhash test.',
    }
    for k, v in data.items(): print k, get_phrases(v)
    for k, v in data.items(): print k, Simhash(get_phrases(v)).value

    objs = [(str(k), Simhash(get_phrases(v))) for k, v in data.items()]
    index = SimhashIndex(objs, k=3)

    print index.bucket_size()

    s1 = Simhash(get_phrases(u'How are you i am fine. blar blar blar blar blar thank'))
    print index.get_near_dups(s1)

    index.add('4', s1)
    print index.get_near_dups(s1)


def main():
    start = time.time()
    #site_content('http://www.akademik.mk', 'http://www.akademik.mk/nekoi-sporni-prashana-vo-zakonot-za-zashtita-na-ukazhuvachite-intervju-so-sudijata-bojana-velkovska/')
    #site_content('http://www.sitel.com.mk', 'http://www.sitel.com.mk/jelena-ja-ubil-razbojnik-od-zabel-so-koj-bila-vo-tajna-vrska')
    #count_sites()
    #multiprocessing_test()
    #pool_test()
    #write_txt()
    simhash_test()
    print time.time()-start, "s"
    #print domains["http://www.akademik.mk"].keys()

if __name__ == "__main__":
    main()


