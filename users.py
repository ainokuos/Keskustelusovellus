from flask import request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import os


def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user[0]
            return True
        else:
            return False


def signin(username, password):
    if len(password) == 0:
        return False
    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user:
        return False
    else:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        login(username, password)
        return True

def logout():
    del session["username"]
    del session["user_id"]

def user_id():
    return session["user_id"]

