from app import app
from flask import render_template, request, redirect
import users, messages

@app.route("/")
def index():
    topics = messages.get_all()
    replies = messages.get_sum()
    return render_template("index.html", topics = topics, replies = replies)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = False
    if request.method == "GET":
        return render_template("login.html", error = error)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            error = True
            return render_template("login.html", error = error)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    error = False
    if request.method == "GET":
        return render_template("signin.html", error = error)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.signin(username, password) == True:
            return redirect("/")
        else:
            error = True
            return render_template("signin.html", error = error)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/new", methods=["GET", "POST"])
def new():
    error = False
    if request.method == "GET":
        return render_template("new.html", error = error)
    
    if request.method == "POST":
        topic = request.form["topic"]
        content = request.form["content"]
        if messages.new(topic, content) == True:
            return redirect("/")
        else:
            error = True
            return render_template("new.html", error = error)


@app.route("/message/<int:id>", methods=["GET", "POST"])
def message(id):
    content = messages.get_message(id)
    if request.method == "GET":
        replies = messages.get_replies(id)
        return render_template("message.html", id = id, content = content, replies = replies)
    if request.method == "POST":
        reply = request.form["reply"]
        messages.reply(reply, id)
        return redirect("/message/" + str(id))

@app.route("/questions")
def questions():
    return render_template("questions.html")
