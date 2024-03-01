import os

class Config:
    DATABASE_URI = os.environ.get('DATABASE_URI', 'mysql+mysqlconnector://root@localhost:3306/school')