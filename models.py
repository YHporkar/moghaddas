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
    answer1 = Column(Integer)
    answer2 = Column(Integer)
    answer3 = Column(Integer)
    answer4 = Column(Integer)
    answer5 = Column(Integer)
    opinion = Column(Text)
    participation = Column(Text)

    def __init__(self, name, age, phone_number, answer1, answer2, answer3, answer4, answer5, opinion, participation):
        self.name = name
        self.age = age
        self.phone_number = phone_number
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.answer4 = answer4
        self.answer5 = answer5
        self.opinion = opinion
        self.participation = participation
    
