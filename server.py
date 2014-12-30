#!/usr/bin/env python3
import json

from collections import OrderedDict

from flask import Flask, abort, request

from passlib.hash import pbkdf2_sha256

from sqlalchemy import create_engine
from sqlalchemy import Sequence
from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from sqlalchemy.exc import IntegrityError



#engine = create_engine("sqlite:///:memory:", echo=True)
engine = create_engine("sqlite:///test.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email = Column(String(254), unique=True)
    name = Column(String(773)) # Wolfe+585, Sr.
    password = Column(String)

    def get_json(self):
        d = OrderedDict()
        d['id'] = self.id
        d['email'] = self.email
        d['name'] = self.name
        d['password'] = self.password

        return json.dumps(d)

    def __repr__(self):
        return "User" + str(self.get_json())

Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/user/add', methods=['POST']) #TODO: remove get
def user_put():
    if (request.form.get("email", "") == "" or
       request.form.get("name", "") == "" or
       request.form.get("password", "") == ""):
        abort(400)

    hashed_pw = pbkdf2_sha256.encrypt(request.form['password'],
                                        rounds=20000, salt_size=16)

    user = User(email=request.form['email'],
            name=request.form['name'],
            password=hashed_pw)# TODO: hash password
    try:
        session.add(user)
        session.commit()#TODO: necessary?
    except IntegrityError:
        session.rollback()
        abort(400) # non unique email


    return user.get_json()

@app.route('/user/get', methods=['POST']) #TODO: remove get
def user_get():
    if request.form.get("email", "") == "":
        abort(400)

    user = session.query(User).filter_by(email=request.form['email']).first()
    return user.get_json()

if __name__ == "__main__":
    app.run(debug=True) #TODO: remove after dev
