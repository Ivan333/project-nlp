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


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)


Session = sessionmaker()

engine = create_engine("sqlite:///tutorial.db", echo=False)

Base.metadata.create_all(engine)

Session.configure(bind=engine)

session = Session()
ed_user = User(name="ed", fullname = "ed jones", password = "edspassword")
session.add(ed_user)
session.commit()

temp = session.query(User).filter_by(name="ed").all()
print temp
