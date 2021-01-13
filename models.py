from sqlalchemy import Column, Integer, String, Text, create_engine, DateTime, ForeignKey

from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class AddUpdateDelete():
    def add(self, resource):
        session.add(resource)
        return session.commit()

    def update(self):
        return session.commit()

    def delete(self, resource):
        session.delete(resource)
        return session.commit()


class User(Base, AddUpdateDelete):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(String, nullable=False)
    answer = Column(Integer)
    poll = Column(Integer)
    opinion = Column(Text)
    participation = Column(Text)

    def __init__(self, name, age, phone_number, answer, poll, opinion, participation):
        self.name = name
        self.age = age
        self.phone_number = phone_number
        self.answer = answer
        self.poll = poll
        self.opinion = opinion
        self.participation = participation
    
