#!/usr/bin/env python3
from flask import Flask, abort, request

from passlib.hash import pbkdf2_sha256

from db import Db

app = Flask(__name__)

db = Db()

@app.route('/')
def hello():
    return "Lunchelp API"

@app.route('/user/add', methods=['POST']) #TODO: remove get
def user_put():
    if (request.form.get("email", "") == "" or
       request.form.get("name", "") == "" or
       request.form.get("password", "") == ""):
        abort(400)

    hashed_pw = pbkdf2_sha256.encrypt(request.form['password'],
                                        rounds=20000, salt_size=16)

    user = db.User(email=request.form['email'],
            name=request.form['name'],
            password=hashed_pw)# TODO: hash password
    try:
        db.session.add(user)
        db.session.commit()#TODO: necessary?
    except IntegrityError:
        db.session.rollback()
        abort(400) # non unique email

    if user is None:
        abort(400)

    return user.get_json()

@app.route('/user/get', methods=['POST']) #TODO: remove get
def user_get():
    if request.form.get("email", "") == "":
        abort(400)

    user = db.session.query(db.User).filter_by(email=request.form['email']).first()

    if user is None:
        abort(400)

    return user.get_json()

if __name__ == "__main__":
    app.run(debug=True) #TODO: remove after dev
