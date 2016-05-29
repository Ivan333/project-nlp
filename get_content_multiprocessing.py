import multiprocessing
import anydbm
import difflib
from bs4 import BeautifulSoup
from mkText import MkTextChecker
import cPickle

checkerMk = MkTextChecker("wfl-mk.tbl")


def mk_text_diff(lines):

    try:
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
    except Exception as e:
        print "mk_text_diff error: %s" % str(e)


def site_content(domain, domain_name, url):
    text1 = domain[domain_name]
    text1_lines = text1.splitlines()

    text2 = domain[url]
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

    #for i, c in enumerate(content): print i, c

    return "\n".join(content)


def pool_process(data):
    domain = data
    num_urls = 0
    content = {}
    for domain_name in data:
        if domain_name not in content:
            content[domain_name] = {}
        domain = data[domain_name]
        for url in domain:
            num_urls += 1
            if num_urls % 10 == 0: print "%s urls compared: %s" % (domain_name, str(num_urls))
            content[domain_name][url] = site_content(domain, domain_name, url)

    return content


def pool_initializer():
    print "starting", multiprocessing.current_process().name


def pool_test(content):
    inputs = content
    pool_size = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=pool_size, initializer=pool_initializer)

    pool_outputs = pool.map(pool_process, inputs)
    pool.close()
    pool.join()

    return pool_outputs


def main():
    db = anydbm.open("mk_html_new.anydbm", "r")
    db_content = anydbm.open("mk_html_content_multitest.anydbm", "c")

    domains = []
    i = 1
    for domain_name in db:
        print i, "domain", domain_name
        i += 1
        domain_name = domain_name.strip()
        dont_visit = ["http://www.alfalab.mk", "http://zulu.com.mk"]
        if domain_name in dont_visit or domain_name in db_content:
            print "vekje postoi: ", domain_name
            continue
        if domain_name not in domains:
            domains.append({domain_name: cPickle.loads(db[domain_name])})

        if i % 100 == 0:
            content = pool_test(domains)
            for domain in content:
                for name in domain:
                    db_content[name] = cPickle.dumps(domain[name], 2)
            db_content.close()
            db_content = anydbm.open("mk_html_content_multitest.anydbm", "c")
            domains = []

    db_content.close()
    db.close()

if __name__ == "__main__":
    main()

