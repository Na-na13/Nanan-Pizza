from datetime import datetime
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
    sql = db.session.execute("SELECT name, price, ingredients FROM pizza")
    pizzas = sql.fetchall()
    return render_template("index.html", pizzas=pizzas)

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["uname"]
    password = request.form["psw"]
    sql = "SELECT password FROM users WHERE username=:username"
    query = db.session.execute(sql, {"username":username})
    result = query.fetchone()
    # check if username exists
    if not result:
        print("not existing user") # show error message to user!
        return redirect("/")
    # check if password matches
    elif result[0] == password:
        session["username"] = username
        print("logged in succesfully")
        return redirect("/logged")
    else:
        print("password did not match") # show error message to user!
        return redirect("/")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logged")
def logged():
    sql = db.session.execute("SELECT name, price, ingredients FROM pizza")
    pizzas = sql.fetchall()
    sql = db.session.execute("SELECT name, price FROM extras")
    extras = sql.fetchall()
    return render_template("logged.html", pizzas=pizzas, extras=extras)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create_new_user():
    # check if username is available
    username = request.form["uname"]
    password = request.form["psw"]
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql,{"username":username, "password":password})
        db.session.commit()
        print("new user created")
        return redirect("/")
    except Exception:
        print("username is taken") # show error message to user!
        return render_template("new.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/add_to_orderlist", methods=["POST"])
def add_to_orderlist():
    prod = request.form["product"]
    size = request.form["size"]
    extras = request.form.getlist("extra")
    try:
        sql = "INSERT INTO orderlist (prod, size, extras) VALUES (:prod, :size, :extras)"
        db.session.execute(sql,{"prod":prod, "size":size, "extras":extras})
        db.session.commit()
        print("item added to orderlist") # inform user!
        return logged()
    except Exception:
        print("error, try again!") # inform user!
        return logged()

@app.route("/view_orderlist")
def view_orderlist():
    sql = db.session.execute("SELECT prod, size, extras FROM orderlist")
    orders = sql.fetchall()
    price = 0
    for prod in orders:
        prod_sql = "SELECT price FROM pizza WHERE name=:name"
        result = db.session.execute(prod_sql,{"name":prod[0]})
        price += result.fetchone()[0]
        for extra in prod[2]:
            xtr_sql = "SELECT price FROM extras WHERE name=:name"
            xtr_result = db.session.execute(xtr_sql,{"name":extra})
            price += xtr_result.fetchone()[0]
        if prod[1] == 2:
            price += 6.5
        if prod[1] == 3:
            proce += 4.5
    return render_template("orderlist.html", orders=orders, price=price)

@app.route("/submit_order")
def submit_order():
    user = session["username"]
    order_sql = db.session.execute("SELECT prod, size, extras FROM orderlist")
    final_order = [(row[0],row[1],row[2]) for row in order_sql.fetchall()]
    print(final_order)
    ordertime = datetime.now()
    try:
        submit_sql = "INSERT INTO orders (username, order_list, order_time) VALUES(:username, :order_list, :ordertime)"
        db.session.execute(submit_sql,{"username":user, "order_list":final_order, "ordertime":ordertime})
        db.session.commit()
        print("order submitted") # inform user!
        # empty orderlist
        db.session.execute("DELETE FROM orderlist")
        db.session.commit()
        return redirect("/logged")
    except Exception:
        print("error occured while submitting the order") # inform user!
        return redirect("/logged")
