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
def user_post():
    if (request.form.get("email", "") == "" or
       request.form.get("name", "") == "" or
       request.form.get("password", "") == ""):
        return json.dumps({'status': 400, 'message': 'Invalid input'})

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
        return json.dumps({'status': 400, 'message': 'Duplicate user'})#TODO: accurate?

    if user is None:
        return json.dumps({'status': 500, 'message': "Could not insert resturant"})

    return user.get_json()

@app.route('/user/get', methods=['POST']) #TODO: remove get
def user_get():
    if request.form.get("email", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    user = db.session.query(db.User).filter_by(email=request.form['email']).first()

    if user is None:
        return json.dumps({'status': 500, 'message': "Could not find user"})

    return user.get_json()

@app.route('/resturant/add', methods=['POST'])
def resturant_post():
    if (request.form.get("name", "") == "" or
        request.form.get("address", "") == ""):
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    resturant = db.Resturant(name=request.form['name'], address=request.form['address'])

    try:
        db.session.add(resturant)
        db.session.commit()#TODO: necessary?
    except IntegrityError:
        db.session.rollback()
        return json.dumps({'status': 400, 'message': 'Duplicate resturant'})#TODO: accurate?

    if resturant is None:
        return json.dumps({'status': 500, 'message': "Could not insert resturant"})

    return resturant.get_json()

@app.route('/resturant/get', methods=['POST'])
def resturant_get():
    if request.form.get("name", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    resturant = db.session.query(db.Resturant).filter_by(name=request.form['name']).first()

    if user is None:
        return json.dumps({'status': 500, 'message': "Could not find resturant"})

    return resturant.get_json()

@app.route('/group/add', methods=['POST'])
def group_post():
    if (request.form.get("name", "") == ""):
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    group = db.Group(name=request.form['name'])

    try:
        db.session.add(group)
        db.session.commit()#TODO: necessary?
    except IntegrityError:
        db.session.rollback()
        return json.dumps({'status': 400, 'message': 'Duplicate group'})#TODO: accurate?

    if resturant is None:
        return json.dumps({'status': 500, 'message': "Could not insert group"})

    return resturant.get_json()

@app.route('/group/get', methods=['POST'])
def group_get():
    if request.form.get("id", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    group = db.session.query(db.Group).filter_by(name=request.form['name']).first()

    if user is None:
        return json.dumps({'status': 500, 'message': "Could not find group"})

    return group.get_json()

@app.route('/event/add', methods=['POST'])
def event_post():
    if (request.form.get("name", "") == "" or
        request.form.get("desc", "") == "" or
        request.form.get("resturant_id", "") == "" or
        request.form.get("group_id", "") == "" or
        request.form.get("time", "") == ""):#TODO: int validation?
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    event = db.Event(name=request.form['name'],
                    desc=request.form['desc'],
                    resturant_id=int(request.form['resturant_id']),
                    group_id=int(request.form['group_id']),
                    time=int(request.form['time']))

    try:
        db.session.add(event)
        db.session.commit()#TODO: necessary?
    except IntegrityError:
        db.session.rollback()
        return json.dumps({'status': 400, 'message': 'Duplicate event'})#TODO: accurate?

    if event is None:
        return json.dumps({'status': 500, 'message': "Could not insert event"})

    return event.get_json()

@app.route('/event/get', methods=['POST'])
def event_get():
    if request.form.get("id", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    event = db.session.query(db.Group).filter_by(id=request.form['id']).first()

    if event is None:
        return json.dumps({'status': 500, 'message': "Could not find event"})

    return group.get_json()

if __name__ == "__main__":
    app.run(debug=True) #TODO: remove after dev
