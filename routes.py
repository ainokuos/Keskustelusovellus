from app import app
from flask import render_template, request, redirect
import users, messages, queries


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = False
    if request.method == "GET":
        return render_template("login.html", error=error)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            error = True
            return render_template("login.html", error=error)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    error = False
    if request.method == "GET":
        return render_template("signin.html", error=error)
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.signin(username, password) == True:
            return redirect("/")
        else:
            error = True
            return render_template("signin.html", error=error)


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/topics", methods=["GET", "POST"])
def topics():
    if request.method == "GET":
        topics = messages.get_all()
        replies = messages.get_sum()
        return render_template("topics.html", topics=topics, replies=replies)
    if request.method == "POST":
        search = request.form["search"]
        topics = messages.get_search(search)
        replies = messages.get_sum()
        return render_template("topics.html", topics=topics, replies=replies)
        

@app.route("/new", methods=["GET", "POST"])
def new():
    error = False
    if request.method == "GET":
        return render_template("new.html", error=error)
    
    if request.method == "POST":
        topic = request.form["topic"]
        content = request.form["content"]
        if messages.new(topic, content) == True:
            return redirect("/topics")
        else:
            error = True
            return render_template("new.html", error=error)


@app.route("/message/<int:id>", methods=["GET", "POST"])
def message(id):
    content = messages.get_message(id)
    username = users.get_username(content[2])
    if request.method == "GET":
        replies = messages.get_replies(id)
        return render_template("message.html", id=id, content=content, replies=replies, username=username)
    if request.method == "POST":
        reply = request.form["reply"]
        messages.reply(reply, id)
        return redirect("/message/" + str(id))


@app.route("/questions")
def questions():
    polls = queries.get_queries()
    return render_template("questions.html", polls=polls)


@app.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "GET":
        return render_template("ask.html")
    if request.method == "POST":
        topic = request.form["topic"]
        choices = request.form.getlist("choice")
        queries.new_question(topic, choices)
        return redirect("/questions")


@app.route("/question/<int:id>", methods=["GET", "POST"])
def question(id):
    if request.method == "GET":
        answered = queries.answered(id)
        question = queries.get_question(id)
        choices = queries.get_choices(id)
        answers = queries.get_answers(id)
        sum = queries.get_sum(id)
        return render_template("question.html", id=id, question=question, choices=choices, answers=answers, answered=answered, sum=sum)
    
    if request.method == "POST":
        choice = request.form["choice"]
        queries.answer(choice)
        return redirect("/question/"+ str(id))


@app.route("/delete/<int:id>")
def delete(id):
    messages.delete(id)
    return redirect("/topics")


@app.route("/delete_question/<int:id>")
def delete_question(id):
    queries.delete(id)
    return redirect("/questions")

@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    if request.method =="GET":
        contacts = messages.get_contacts()
        return render_template("contacts.html", contacts=contacts)
    if request.method == "POST":
        search = request.form["search"]
        contacts = users.get_search(search)
        return render_template("contacts.html", contacts=contacts)

@app.route("/chat/<int:id>", methods=["GET", "POST"])
def chat(id):
    if request.method == "GET":
        chats = messages.get_private_chat(id)
        return render_template("chat.html", id=id, chats=chats)
    
    if request.method == "POST":
        content = request.form["content"]
        messages.private_message(id, content)
        return redirect("/chat/" + str(id))

