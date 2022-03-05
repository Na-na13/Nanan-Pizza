from db import db
from flask import session

def get_all():
    sql = db.session.execute("SELECT prod_id AS id, name, price, ingredients FROM products WHERE category ='pizza' ORDER BY prod_id")
    pizzas = sql.fetchall()
    sql = db.session.execute("SELECT prod_id AS id, name, price, ingredients FROM products WHERE category ='salad' ORDER BY prod_id")
    salads = sql.fetchall()
    sql = db.session.execute("SELECT prod_id AS id, name, price, ingredients FROM products WHERE category ='drink' ORDER BY prod_id")
    drinks = sql.fetchall()
    sql = db.session.execute("SELECT extra_id AS id, name, price FROM extras ORDER BY name, price")
    extras = sql.fetchall()
    return pizzas, salads, drinks, extras
    
def search(query):
    sql = ("SELECT DISTINCT p.prod_id, name, ingredients, price FROM products p JOIN (SELECT prod_id, unnest(ingredients) AS inc FROM products) AS i ON i.inc ILIKE :query AND i.prod_id=p.prod_id ORDER BY prod_id;")
    query = db.session.execute(sql, {"query":"%"+query+"%"})
    result = query.fetchall()
    return result