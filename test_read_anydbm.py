import anydbm
import cPickle
'''
db = anydbm.open("mk_html.anydbm")

f = open("test_visited_domains.txt", "w")

urls = cPickle.loads(db["0"])
i = 0
for k in urls:
    f.write(k+"\n")
    i+=len(k)

print len(urls)
print i

f.close()

urls = cPickle.loads(db["0"])

print "http://www.sitel.com.mk", len(urls["http://www.sitel.com.mk"])
print "http://www.kanal5.com.mk", len(urls["http://www.kanal5.com.mk"])
print "http://www.akademik.mk", len(urls["http://www.akademik.mk"])
print "http://24vesti.mk", len(urls["http://24vesti.mk"])

db1 = anydbm.open("test_db.anydbm", "c")

db1["http://www.sitel.com.mk"] = cPickle.dumps(urls["http://www.sitel.com.mk"])
db1["http://www.kanal5.com.mk"] = cPickle.dumps(urls["http://www.kanal5.com.mk"])
db1["http://www.akademik.mk"] = cPickle.dumps(urls["http://www.akademik.mk"])
db1["http://24vesti.mk"] = cPickle.dumps(urls["http://24vesti.mk"])

db1.close()

db.close()
'''

db = anydbm.open("test_db.anydbm")

domains = {}
for k in db:
    domains[k] = cPickle.loads(db[k])

db.close()
