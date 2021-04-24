from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")
booted = True

@app.route("/")
def login():
    global booted
    if booted == True:
        booted = False
        session["username"] = None
        session["isadmin"] = False
        
    if session["username"] == None:
        return render_template("login.html")
    return redirect("/frontpage")
    
@app.route("/catalogue")
def catalogue():
    if session["isadmin"] == False:
        return render_template("accesserror.html")
    result = db.session.execute("SELECT COUNT(*) FROM cards")
    count = result.fetchone()[0]
    result = db.session.execute("SELECT * FROM cards")
    kortit = result.fetchall()
    
    caards = []
    
    for kortti in kortit:
        caard = []
        caard.append(str(kortti[0]))
        caard.append(kortti[1])
        caard.append(kortti[2])
        caard.append(kortti[3])
        caard.append(str(kortti[4]))
        caards.append(caard)
    
    kortit = caards
        
    return render_template("catalogue.html", count=count, kortit=kortit)
    
@app.route("/add")
def add():
    if session["isadmin"] == False:
        return render_template("accesserror.html")
    return render_template("add.html")
    
@app.route("/send", methods=["POST"])
def send():
    if session["isadmin"] == False:
        return render_template("accesserror.html")
    name = request.form["name"]
    descr = request.form["descr"]
    elem = request.form["elementti"]
    rari = request.form["harvinaisuus"]
    
    sql = "INSERT INTO cards (nimi, elementti, kuvaus, harvinaisuus) VALUES (:name, :elem, :descr, :rari)"
    db.session.execute(sql, {"name":name, "elem":elem, "descr":descr, "rari":rari})
    db.session.commit()
    return redirect("/catalogue")
    
@app.route("/userlogin", methods=["POST"])
def userlogin():

    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT password FROM users WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    
    if user == None:
        return redirect("/error")
    
    hash_value = user[0]
    if check_password_hash(hash_value,password):
        session["username"] = username
        session["isadmin"] = False
        if username == "admin":
            session["isadmin"] = True
    else:
        return redirect("/error")
    return redirect("/frontpage")
    
@app.route("/signin")
def signin():
    if session["username"] != None:
        return redirect("/")
    return render_template("/signin.html")
    
@app.route("/frontpage")
def frontpage():
    if session["username"] == None:
        return redirect("/")
    username = session["username"]
    if session["isadmin"] == True:
        return render_template("/adminlogin.html")
    return render_template("/frontpage.html", username=username)
    
@app.route("/createaccount", methods=["POST"])
def createaccount():
    username = request.form["username"]
    p = request.form["password"]
    cp = request.form["confpassword"]
    
    password = generate_password_hash(p)
    
    if p != cp:
        return redirect("/error")
    
    sql = "INSERT INTO users (username, password, actions, coins, isadmin) VALUES (:username, :password, 0, 0, TRUE)"
    db.session.execute(sql, {"username":username,"password":password})
    db.session.commit()
    return redirect("/")
    
@app.route("/error")
def error():
    return render_template("/error.html")
    
@app.route("/logout")
def logout():
    session["username"] = None
    session["isadmin"] = False
    return redirect("/")
