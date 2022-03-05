from app import app
from flask import redirect, render_template, request, session

import order
import product
import user

@app.route("/")
def index():
    products = product.get_all()
    return render_template("index.html", pizzas=products[0], salads=products[1], drinks=products[2])

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not user.login(username, password):
            return redirect("/")
        return redirect("/logged")

@app.route("/logged")
def logged():
    products = product.get_all()
    return render_template("logged.html", pizzas=products[0], salads=products[1], drinks=products[2], extras=products[3])

@app.route("/logout")
def logout():
    user.logout()
    return redirect("/")

@app.route("/create", methods=["GET","POST"])
def create_new_user():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user.create_new(username, password):
            return redirect("/")
        else:
            pass
            # käyttäjätunnus on varattu!
    
@app.route("/search")
def search():
    key = request.args["query"]
    result = product.search(key)
    products = product.get_all()
    if not session.get("user_id"):
         return render_template("index.html", result=result, pizzas=products[0], salads=products[1], drinks=products[2])
    return render_template("logged.html", result=result, pizzas=products[0], salads=products[1], drinks=products[2])  

@app.route("/add_to_orderlist", methods=["POST"])
def add_to_orderlist():
    user.check_csrf()
    prod = request.form["product"]
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
