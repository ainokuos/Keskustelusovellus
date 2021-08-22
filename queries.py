from db import db
import os
import users

def new_question(topic, choices):
    user_id = users.user_id()
    visible = "TRUE"
    sql = "INSERT INTO questions (topic, user_id, visible) VALUES (:topic, :user_id, :visible)"
    db.session.execute(sql, {"topic":topic, "user_id":user_id, "visible":visible})
    db.session.commit()
    sql = "SELECT id FROM questions ORDER BY id DESC LIMIT 1"
    result = db.session.execute(sql)
    question_id = result.fetchone()[0]
    for choice in choices:
        if choice != "":
            sql = "INSERT INTO choices (question_id, choice) VALUES (:question_id, :choice)"
            db.session.execute(sql, {"question_id":question_id, "choice":choice})
            db.session.commit()

def get_queries():
    sql = "SELECT id, topic, user_id FROM questions WHERE visible=TRUE ORDER BY id DESC"
    result = db.session.execute(sql)
    return result

def get_question(id):
    sql = "SELECT topic, user_id FROM questions WHERE id =:id"
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
    sql = "SELECT C.choice, count(A.choice_id) FROM choices C, answers A WHERE A.choice_id = C.id AND C.question_id =:question_id GROUP BY C.id, C.choice, C.question_id"
    result = db.session.execute(sql, {"question_id":question_id}).fetchall()
    return result

def delete(id):
    sql = "UPDATE questions SET visible=FALSE WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
        
def answered(question_id):
    sql ="SELECT A.user_id FROM answers A, questions Q, choices C  WHERE Q.id = C.question_id AND C.id = A.choice_id AND Q.id =:question_id"
    results = db.session.execute(sql, {"question_id":question_id}).fetchall()
    for result in results:
        if result[0] == users.user_id():
            return True
    return False

def get_sum(question_id):
    sql ="SELECT COUNT(A.id) FROM answers A, choices C WHERE A.choice_id=C.id AND C.question_id=:question_id;"
    result = db.session.execute(sql, {"question_id":question_id}).fetchone()
    return result[0]