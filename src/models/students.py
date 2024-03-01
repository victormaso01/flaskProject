from src.config import db
from sqlalchemy import Column, Integer, String

class Student(db.Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    spec = Column(String(50))
    age = Column(Integer)

    def __init__(self, name, spec, age):
        self.name = name
        self.spec = spec
        self.age = age

    def __str__(self):
        return f'name : {self.name}, spec : {self.spec}, age : {self.age}'