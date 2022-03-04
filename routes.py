from app import app
from db import db
#from datetime import datetime
#from flask import Flask
from flask import redirect, render_template, request, session
#from flask_sqlalchemy import SQLAlchemy
#from os import getenv
#from werkzeug.security import check_password_hash, generate_password_hash

import user
import order

#app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.secret_key = getenv("SECRET_KEY")
#db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = db.session.execute("SELECT name, price, ingredients FROM products WHERE category ='pizza'")
    pizzas = sql.fetchall()
    sql = db.session.execute("SELECT name, price, ingredients FROM products WHERE category ='salad'")
    salads = sql.fetchall()
    sql = db.session.execute("SELECT name, price, ingredients FROM products WHERE category ='drink'")
    drinks = sql.fetchall()
    return render_template("index.html", pizzas=pizzas, salads=salads, drinks=drinks)

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    password = request.form["password"]
    if user.login(username, password):
        return redirect("/logged")
    else:
        pass
        print("käyttäjätunnus tai salasana ei täsmää -> luo uusi käyttäjä?")
    return redirect("/")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return redirect("/")
        return redirect("/logged")
#    return render_template("login.html")

@app.route("/logged")
def logged():
    sql = db.session.execute("SELECT prod_id AS id, name, price, ingredients FROM products WHERE category ='pizza' ORDER BY prod_id")
    pizzas = sql.fetchall()
    sql = db.session.execute("SELECT prod_id AS id, name, price, ingredients FROM products WHERE category ='salad' ORDER BY prod_id")
    salads = sql.fetchall()
    sql = db.session.execute("SELECT prod_id AS id, name, price, ingredients FROM products WHERE category ='drink' ORDER BY prod_id")
    drinks = sql.fetchall()
    sql = db.session.execute("SELECT extra_id AS id, name, price FROM extras ORDER BY name, price")
    extras = sql.fetchall()
    return render_template("logged.html", pizzas=pizzas, salads=salads, drinks=drinks, extras=extras)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create_new_user():
    username = request.form["username"]
    password = request.form["password"]
    if user.create_new(username, password):
        return redirect("/")
    else:
        pass
        # käyttäjätunnus on varattu!

@app.route("/logout")
def logout():
    user.logout()
    return redirect("/")

@app.route("/add_to_orderlist", methods=["POST"])
def add_to_orderlist():
    user.check_csrf()
    prod = request.form["product"]
    print("tuote:",prod)
    size = request.form["size"]
    extras = request.form.getlist("extra")
    if order.add_product(prod, size, extras):
        return logged()
        # Tuote lisätty tilaukseen onnistuneesti
    else:
        pass
        # Tuotteen lisäämisessä tilaukseen ilmeni virhe, yritä uudestaan!

@app.route("/view_orderlist")
def view_orderlist():
    orderlist = order.view_all()
    orders = orderlist[0]
    total_price = orderlist[1]
    return render_template("orderlist.html", orders=orders, price=total_price)

@app.route("/submit_order")
def submit_order():
    pass
    #user = session["username"]
    #order_sql = db.session.execute("SELECT prod, size, extras FROM orderlist")
    #final_order = [(row[0],row[1],row[2]) for row in order_sql.fetchall()]
    #print(final_order)
    #ordertime = datetime.now()
    #try:
    #    submit_sql = "INSERT INTO orders (username, order_list, order_time) VALUES(:username, :order_list, :ordertime)"
    #    db.session.execute(submit_sql,{"username":user, "order_list":final_order, "ordertime":ordertime})
    #    db.session.commit()
    #    print("order submitted") # inform user!
    #    # empty orderlist
    #    db.session.execute("DELETE FROM orderlist")
    #    db.session.commit()
    #    return redirect("/logged")
    #except Exception:
    #    print("error occured while submitting the order") # inform user!
    #    return redirect("/logged")

@app.route("/remove_item", methods=["POST"])
def remove_item():
    user.check_csrf()
    order_id = request.form["order_id"]
    order.remove_product(order_id)
    return view_orderlist()
