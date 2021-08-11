from flask import request, session
from db import db
import os
import users

def new(topic, content):
    if len(content) == 0:
        return False
    else:
        user_id = users.user_id()
        visible = "TRUE"
        sql = "INSERT INTO messages (topic, content, user_id, visible) VALUES (:topic, :content, :user_id, :visible)"
        db.session.execute(sql, {"topic":topic, "content":content, "user_id":user_id, "visible":visible})
        db.session.commit()
        return True

def get_all():
    sql = "SELECT id, topic, content FROM messages WHERE visible = TRUE ORDER BY id"
    messages = db.session.execute(sql)
    return messages

def get_message(message_id):
    sql = "SELECT id, topic, content, user_id FROM messages WHERE id = :message_id AND visible = TRUE"
    result = db.session.execute(sql, {"message_id":message_id}).fetchone()
    return result

def reply(content, message_id):
    user_id =users.user_id()
    if content != "" and content.count(" ") != len(content):
        sql = "INSERT INTO replies (content, message_id, user_id) VALUES (:content, :message_id, :user_id)"
        db.session.execute(sql, {"content":content, "message_id":message_id, "user_id":user_id})
        db.session.commit()

def get_replies(message_id):
    sql = "SELECT content FROM replies WHERE message_id =:message_id"
    result = db.session.execute(sql, {"message_id":message_id}).fetchall()
    return result

def get_sum():
    sql = "SELECT COUNT(replies.message_id) FROM messages LEFT JOIN replies ON messages.id = replies.message_id GROUP BY messages.id ORDER BY messages.id"
    sum = db.session.execute(sql).fetchall()
    return sum

def delete(id):
    sql = "UPDATE messages SET visible=FALSE WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

