'''
source: http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html

easy_install SQLAlchemy
download http://aka.ms/vcpython27
read http://stackoverflow.com/questions/5504404/python-unable-to-easy-install-windows-7-x64
download http://www.lfd.uci.edu/~gohlke/pythonlibs/#pysqlite
read https://pip.pypa.io/en/latest/user_guide/#installing-from-wheels
pip install pysqlite-2.8.2-cp27-cp27m-win_amd64.whl
'''

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import anydbm
import cPickle


engine = create_engine("sqlite:///mk_html_sqlite.db", echo=False)
Base = declarative_base()


class Website(Base):
    __tablename__ = "website"

    id = Column(Integer, primary_key=True)
    domain = Column(String)
    url = Column(String)
    html = Column(TEXT)

    def __repr__(self):
        return "<User(id='%s', domain='%s', url='%s')>" % (str(self.id), self.domain, self.url)


Session = sessionmaker()
#create a table (website) in the database
#Base.metadata.create_all(engine)
Session.configure(bind=engine)
session = Session()

db = anydbm.open("mk_html_new.anydbm", 'r')
#'''
i = 0
for domain_name in db:
    if i % 10 == 0: print i
    i += 1
    domain = cPickle.loads(db[domain_name])
    '''
    for url in domain:
        site = Website(domain=domain_name, url=url, html=cPickle.dumps(domain[url]))
        if not session.query(Website).filter_by(url=url).first():
            session.add(site)
    session.commit()
    '''

db.close()
#'''
#ed_user = User(name="ed", fullname = "ed jones", password = "edspassword")
#session.add(ed_user)
#session.commit()

temp = session.query(Website).filter_by(domain="http://contrek.mk").all()
print "test", temp
