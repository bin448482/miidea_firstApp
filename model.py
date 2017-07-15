# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declarative_base
import datetime

#initial database
engine = create_engine('mysql+mysqlconnector://dev:miidea299553@127.0.0.1:3306/miidea_encryption_keys_db')
Base = declarative_base()

#deal with datatime type to json serializer
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

#add class for json serialization
class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class EncryptionKeys(Base, Serializer):
    __tablename__ = 'tbl_encryption_keys'
    id =  Column('id', Integer, primary_key=True)
    key = Column('key', String(20))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    def serialize(self):
        d = Serializer.serialize(self)
        return d

class Account(Base):
    __tablename__ = 'tbl_account'
    id = Column('id', Integer, primary_key=True)
    phone_or_email = Column('phone_or_email', String(50))
    tbl_encryption_keys_id = Column('tbl_encryption_keys_id', Integer)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

class Token(Base):
    __tablename__ = 'tbl_Token'
    id = Column('id', Integer, primary_key=True)
    token = Column('token', String(50))
    tbl_encryption_keys_id = Column('tbl_encryption_keys_id', Integer)

def initailDatabase():
    Base.metadata.create_all(engine)

def addEncryptionKey(key):
    Session = sessionmaker(bind=engine)
    session = Session()
    item = EncryptionKeys(key=key)
    session.add(item)
    session.commit()
    return item

def udpateEncryptionKey(id, key):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(EncryptionKeys).filter(EncryptionKeys.id == id).update({"key" : key})
    session.commit()
    item = session.query(EncryptionKeys).filter(EncryptionKeys.id == id).first()
    if item is not None:
        return item
    else:
        return None

def getEncryptionKey(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    item = session.query(EncryptionKeys).filter(EncryptionKeys.id == id).first()
    if item is not None:
        return item
    else:
        return None

def getAccount(phone_or_email):
    Session = sessionmaker(bind=engine)
    session = Session()
    item = session.query(Account).filter(Account.phone_or_email ==
        phone_or_email).order_by(desc(Account.created_date)).first()
    if item is not None:
        return item
    else:
        return None

def createAccount(phone_or_email, tbl_encryption_keys_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    item = Account(phone_or_email=phone_or_email, tbl_encryption_keys_id=tbl_encryption_keys_id)
    session.add(item)
    session.commit()
    return item

def createToken(token, tbl_encryption_keys_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    item = session.query(Token).filter(
        Token.token == token, Token.tbl_encryption_keys_id == tbl_encryption_keys_id).first()
    if item is None:
        item = Token(token = token, tbl_encryption_keys_id = tbl_encryption_keys_id)
        session.add(item)
        session.commit()

if __name__ == '__main__':
    initailDatabase()


