from db import db
from flask import session

def add_product(product, size, extras):
    price = get_price(product, size, extras)
    try:
        sql = "INSERT INTO orderlist (user_id, product_id, size, extras, price, visible) VALUES (:id, :product, :size, :extras, :price, :visible)"
        db.session.execute(sql,{"id":session["user_id"], "product":product, "size":size, "extras":extras, "price":price, "visible":True})
        db.session.commit()
        return True
    except Exception:
        return False
   
def remove_product(product):
    try:
        sql = "DELETE FROM orderlist WHERE order_id=:order_id AND user_id=:user_id"
        db.session.execute(sql,{"order_id":product, "user_id":session["user_id"]})
        db.session.commit()
        return True
    except Exception:
        return False
        
def get_price(product_id, size, extras):
    sql = "SELECT SUM(price) FROM (SELECT price FROM products WHERE prod_id=:product_id UNION ALL SELECT price FROM sizes WHERE size_id=:size) AS total"
    query = db.session.execute(sql, {"product_id":product_id, "size":size})
    price = query.fetchone()[0]
    for extra in extras:
        xtr_sql = "SELECT price FROM extras WHERE name=:name"
        xtr_query = db.session.execute(xtr_sql,{"name":extra})
        result = xtr_query.fetchone()
        if result:
            price += result[0]
    return price
    
def view_all():
    user_id = session["user_id"]
    order_query = db.session.execute("SELECT O.order_id AS id, O.product_id AS pid, P.name, S.size_name AS size, O.extras, O.price FROM products P LEFT JOIN orderlist O ON prod_id=O.product_id LEFT JOIN sizes S ON O.size=S.size_id WHERE user_id=user_id AND visible=True;")
    order = order_query.fetchall()
    price_query = db.session.execute("SELECT SUM(price) FROM orderlist WHERE user_id=user_id AND visible=True")
    total_price = price_query.fetchone()[0]
    return order, total_price

def submit_order():
    pass
    