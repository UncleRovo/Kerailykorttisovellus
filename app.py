from flask import Flask
import random
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def login():
    return render_template("login.html")
    
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
        if kortti[4] == 1:
            caard.append("Kulta")
        elif kortti[4] == 2:
            caard.append("Hopea")
        else:
            caard.append("Pronssi")
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
    
@app.route("/remove")
def remove():
    if session["isadmin"] == False:
        return render_template("accesserror.html")
    result = db.session.execute("SELECT * FROM cards")
    kortit = result.fetchall()
    return render_template("remove.html", kortit=kortit)
    
@app.route("/delete", methods=["POST"])
def delete():
    if session["isadmin"] == False:
        return render_template("accesserror.html")
    cardID = request.form["name"]
    sql = "DELETE FROM cards WHERE id=:id"
    db.session.execute(sql, {"id":cardID})
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
        
    sql = "SELECT coins FROM users WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    coins = result.fetchone()
    session["coins"] = coins[0]
    
    sql = "SELECT id FROM users WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    userID = result.fetchone()
    session["userID"] = userID[0]
    
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
    coins = session["coins"]
    userID = session["userID"]
    if session["isadmin"] == True:
        return render_template("/adminlogin.html")
    return render_template("/frontpage.html", username=username, coins=coins, userID=userID)
    
@app.route("/buycard")
def buycard():
    if session["username"] == None or session["username"] == "admin":
        return redirect("/")
    return render_template("/buycard.html", username=session["username"])
    
@app.route("/randomizecard")
def randomizecard():
    if session["username"] == None or session["username"] == "admin":
        return redirect("/")
        
    session["coins"] = session["coins"] - 1
    
    if session["coins"] < 0:
        session["coins"] = 0;
        return redirect("/error")
    newCoins = session["coins"]
    ownerID = session["userID"]
    
    sql = "UPDATE users SET coins = :newCoins WHERE id = :ownerID"
    db.session.execute(sql, {"newCoins":newCoins, "ownerID":ownerID})
    db.session.commit()
    
    result = db.session.execute("SELECT * FROM cards")
    kortit = result.fetchall()
    index = random.randint(0, len(kortit) - 1)
    kortti = kortit[index]
    
    cardID = kortti[0]
    
    
    sql = "SELECT * FROM circulation WHERE cardID = :cardID AND ownerID = :ownerID"
    result = db.session.execute(sql, {"cardID":cardID, "ownerID":ownerID})
    olemassaolevat = result.fetchall()
    
    if len(olemassaolevat) == 0:
        print("ei kortteja, voidaan lisätä")
        sql = "INSERT INTO circulation VALUES (:ownerID, :cardID, 1)"
    else:
        print("käyttäjällä on jo tämä kortti")
        sql = "UPDATE circulation SET amount = (SELECT amount FROM circulation WHERE ownerID = :ownerID AND cardID = :cardID) + 1 WHERE ownerID = :ownerID AND cardID = :cardID"
    
    
    db.session.execute(sql, {"ownerID":ownerID, "cardID":cardID})
    db.session.commit()
    
    harv = "Pronssi"
    if kortti[4] == 2:
        harv = "Hopea"
    elif kortti[4] == 1:
        harv = "Kulta"
    
    return render_template("/getcard.html", kortti=kortti[1], harv=harv)
    
@app.route("/createaccount", methods=["POST"])
def createaccount():
    username = request.form["username"]
    p = request.form["password"]
    cp = request.form["confpassword"]
    
    password = generate_password_hash(p)
    
    if p != cp:
        return redirect("/error")
    
    sql = "INSERT INTO users (username, password, actions, coins, isadmin) VALUES (:username, :password, 0, 5, FALSE)"
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
    session["coins"] = 0
    session["userID"] = -1
    return redirect("/")
