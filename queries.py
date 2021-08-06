from flask import session, request
from db import db
import os
import users

def new_question(topic, choices):
    sql = "INSERT INTO questions (topic) VALUES (:topic)"
    db.session.execute(sql, {"topic":topic})
    db.session.commit()
    sql = "SELECT id FROM questions ORDER BY id DESC LIMIT 1"
    result = db.session.execute(sql)
    question_id = result.fetchone()[0]
    for choice in choices:
        sql = "INSERT INTO choices (question_id, choice) VALUES (:question_id, :choice)"
        db.session.execute(sql, {"question_id":question_id, "choice":choice})
        db.session.commit()

def get_queries():
    sql = "SELECT id, topic FROM questions ORDER BY id"
    result = db.session.execute(sql)
    return result

def get_question(id):
    sql = "SELECT topic FROM questions WHERE id =:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    return result

def get_choices(question_id):
    sql = "SELECT id, choice FROM choices WHERE question_id =:question_id"
    result = db.session.execute(sql, {"question_id":question_id}).fetchall()
    return result

def answer(choice_id):
    user_id = users.user_id()
    sql = "INSERT INTO answers (choice_id, user_id) VALUES (:choice_id, :user_id)"
    db.session.execute(sql, {"choice_id":choice_id, "user_id":str(user_id)})
    db.session.commit()

def get_answers(question_id):
    sql = "SELECT C.choice, count(A.choice_id) FROM answers A, choices C WHERE A.choice_id = C.id AND C.question_id =:question_id GROUP BY C.id, C.choice"
    result = db.session.execute(sql, {"question_id":question_id}).fetchall()
    return result
        
