from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["uname"]
    password = request.form["psw"]
    # check if username exists
    sql = "SELECT * FROM users WHERE username=:username"
    query = db.session.execute(sql, {"username":username})
    user = query.fetchone()
    if not user:
        print("not existing user")
        return redirect("/")
    else:
	# check if password is correct
        sql = "SELECT password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        passw = result.fetchone()
        if passw[0] == password:
            session["username"] = username
            print("logged in succesfully")
            return redirect("/logged")
        else:
            print("password did not match")
            return redirect("/")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logged")
def logged():
    return render_template("logged.html")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create_new_user():
    # check if username is available
    username = request.form["uname"]
    password = request.form["psw"]
    sql = "SELECT * FROM users WHERE username=:username"
    query = db.session.execute(sql,{"username":username})
    user = query.fetchone()
    if not user:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql,{"username":username, "password":password})
        db.session.commit()
        print("new user created")
        return redirect("/")
    else:
        print("username is taken")
        return render_template("new.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
