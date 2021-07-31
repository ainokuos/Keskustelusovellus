from flask import request, session
from db import db
import os
import users

def new(topic, content):
    user_id = users.user_id()
    sql = "INSERT INTO messages (topic, content, user_id) VALUES (:topic, :content, :user_id)"
    db.session.execute(sql, {"topic":topic, "content":content, "user_id":user_id})
    db.session.commit()

def get_all():
    sql = "SELECT id, topic, content FROM messages ORDER BY topic"
    messages = db.session.execute(sql)
    return messages

def get_message(message_id):
    sql = "SELECT topic, content FROM messages WHERE id = :message_id"
    result = db.session.execute(sql, {"message_id":message_id}).fetchone()
    return result
