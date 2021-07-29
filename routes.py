from app import app
from flask import render_template, request, redirect
import users

@app.route("/")
def index():
    return render_template("index.html")

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
