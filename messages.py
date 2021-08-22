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
        sql = "INSERT INTO messages (topic, user_id, visible) VALUES (:topic, :user_id, :visible)"
        db.session.execute(sql, {"topic":topic, "user_id":user_id, "visible":visible})
        db.session.commit()
        sql = "SELECT id FROM messages ORDER BY id DESC LIMIT 1"
        result = db.session.execute(sql)
        message_id = result.fetchone()[0]
        reply(content, message_id)
        return True

def get_all():
    sql = "SELECT DISTINCT ON (M.id)M.id, M.topic, R.content, M.user_id FROM messages M, replies R WHERE visible = TRUE AND M.id = R.message_id ORDER BY M.id DESC, R.id"
    messages = db.session.execute(sql)
    return messages

def get_message(message_id):
    sql = "SELECT id, topic, user_id FROM messages WHERE id = :message_id AND visible = TRUE"
    result = db.session.execute(sql, {"message_id":message_id}).fetchone()
    return result

def reply(content, message_id):
    user_id =users.user_id()
    if content != "" and content.count(" ") != len(content):
        sql = "INSERT INTO replies (content, message_id, user_id) VALUES (:content, :message_id, :user_id)"
        db.session.execute(sql, {"content":content, "message_id":message_id, "user_id":user_id})
        db.session.commit()

def get_replies(message_id):
    sql = "SELECT content, user_id FROM replies WHERE message_id =:message_id"
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

def private_message(user2_id, content):
    user1_id = users.user_id()
    sql = "INSERT INTO chats (user1_id, user2_id, content) VALUES (:user1_id, :user2_id, :content)"
    db.session.execute(sql, {"user1_id":user1_id, "user2_id":user2_id, "content":content})
    db.session.commit()

def get_private_chat(user2_id):
    user1_id = users.user_id()
    sql = "SELECT content, user1_id FROM chats WHERE user1_id =:user1_id AND user2_id=:user2_id OR user1_id=:user2_id AND user2_id =:user1_id"
    result = db.session.execute(sql, {"user1_id":user1_id, "user2_id":user2_id}).fetchall()
    return result

def get_contacts():
    user_id = users.user_id()
    sql = "SELECT DISTINCT U.username, U.id FROM users U, chats C WHERE U.id = C.user1_id AND C.user2_id =:user_id OR U.id=C.user2_id AND C.user1_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return result

def get_search(word):
    sql = "SELECT M.id, M.topic, R.content, M.user_id FROM messages M, replies R WHERE M.id = R.message_id AND R.content LIKE :word AND M.visible=TRUE GROUP BY R.content, M.id, M.topic"
    result = db.session.execute(sql, {"word":"%"+word+"%"})
    return result


