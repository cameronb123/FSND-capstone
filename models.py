from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

# Replace postgres with postgresql to enable app to work with SQLALchemy > 1.4
database_path = os.environ['DATABASE_URL']

if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Movies
Have title and release date
'''
class Movie(db.Model):  
    __tablename__ = "Movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release = Column(Date)

    def __init__(self, title, release):
        self.title = title
        self.release = release

    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release': self.release}


'''
Actors
Have name, age and gender
'''
class Actor(db.Model):
    __tablename__ = "Actors"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String(1))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender}