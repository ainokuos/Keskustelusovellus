import os
from flask import session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session["username"] = username
        session["user_id"] = user[0]
        session["csrf_token"] = os.urandom(16).hex()
        return True
    return False


def signin(username, password):
    if len(password) == 0 or len(username) == 0:
        return False
    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user:
        return False
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    login(username, password)
    return True

def logout():
    del session["username"]
    del session["user_id"]
    del session["csrf_token"]

def user_id():
    return session["user_id"]

def get_username(user_id):
    sql = "SELECT username FROM users WHERE id =:user_id"
    result = db.session.execute(sql, {"user_id":user_id}).fetchone()
    return result

def get_search(word):
    sql = "SELECT username, id FROM users WHERE username LIKE :word"
    result = db.session.execute(sql, {"word":"%"+word+"%"}).fetchall()
    return result

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def require_user():
    if not session.get("user_id"):
        abort(403)
