from db import db
import os
import users

def new_question(topic, choices):
    sql = "INSERT INTO questions (topic) VALUES (:topic)"
    question = db.session.execute(sql, {"topic":topic})
    question_id = question.fetchone()[0]
    for choice in choices:
        if choice != "":
            sql = "INSERT INTO choices (question_id, choice) VALUES (:question_id, :choice)"
            db.session.execute(sql, {"question_id":question_id, "choice":choice})
    db.session.commit()

def get_questions():
    sql = "SELECT id, topic FROM questions"
    result = db.session.execute(sql)
    questions = result.fetchall()
    return questions