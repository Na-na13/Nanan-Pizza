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

@app.route("/login", methods=["POST"])
def login():
    username = request.form["uname"]
    password = request.form["psw"]
    print(username, password)
    # check if username exists
    sql = "SELECT * FROM users WHERE username=:username"
    query = db.session.execute(sql, {"username":username})
    user = query.fetchone()
    if not user:
        print("exit 1")
        return redirect("/")
    else:
        sql = "SELECT password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        passw = result.fetchone()
        print(passw[0])
        if passw[0] == password:
            session["username"] = username
            print("logged in succesfully")
            return redirect("/")
        else:
            print("exit 2")
            return redirect("/")


@app.route("/logged")
def logged():
    pass
