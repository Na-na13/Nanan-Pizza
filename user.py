from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

import secrets

def login(username, password):
    sql = "SELECT password, user_id FROM users WHERE username=:username"
    query = db.session.execute(sql, {"username":username})
    result = query.fetchone()
    if not result:
        return False
    if not check_password_hash(result[0], password):
        return False
    session["user_id"] = result[1]
    session["user_name"] = username
    session["csrf_token"] = secrets.token_hex(16)
    return True
    
def logout():
    del session["user_id"]
    del session["user_name"]
    
def create_new(username, password):
    # check if username is available
    try:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"        
        db.session.execute(sql,{"username":username, "password":hash_value})
        db.session.commit()
        print("new user created")
        return login(username, password)
    except Exception as e:
        print(e)
        print("username is taken") # show error message to user!
        return False
    
def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)