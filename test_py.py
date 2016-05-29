import cPickle
import anydbm

'''
db = anydbm.open('D:\\Aleksandar\\Desktop\\project-nlp\\mk_html.anydbm')
db1 = anydbm.open('D:\\Aleksandar\\Desktop\\project-nlp\\mk_html_new.anydbm', 'c')

v = cPickle.loads(db["0"])

i = 0
for url in v:
    db1[url] = cPickle.dumps(v[url], 2)
    i += 1

print i

db.close()
db1.close()
'''
f = anydbm.open('D:\\Aleksandar\\Desktop\\project-nlp\\mk_html_threading.anydbm')
print len(f)

'''
urls = []
i = 0
for line in open('D:\\Aleksandar\\Desktop\\project-nlp\\foundDomains.txt'):
    i += 1
    urls.append(line.strip())
    if i < 448: continue
    if line in urls: continue

for url in urls:
    f.write(url+"\n")
'''
f.close()
