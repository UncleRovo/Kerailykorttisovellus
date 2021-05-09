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
    
@app.route("/listmycards")
def listmycards():
    if session["username"] == None or session["isadmin"] == True:
        return render_template("error.html")
    ownerid = session["userID"]
    sql = "SELECT cards.nimi, cards.elementti, cards.kuvaus, cards.harvinaisuus, circulation.amount FROM cards, circulation WHERE circulation.ownerid = :ownerid AND cards.id = circulation.cardid"
    result = db.session.execute(sql, {"ownerid":ownerid})
    
    userCards = result.fetchall()
    temp = []
    
    for card in userCards:
        cardtoadd = []
        cardtoadd.append(card[0])
        cardtoadd.append(card[1])
        cardtoadd.append(card[2])
        if card[3] == 1:
            cardtoadd.append("Kulta")
        elif card[3] == 2:
            cardtoadd.append("Hopea")
        else:   
            cardtoadd.append("Pronssi")
        cardtoadd.append(str(card[4]))
        temp.append(cardtoadd)
    
    userCards = temp
        
    return render_template("listmycards.html", kortit=userCards)
    
@app.route("/messages")
def messages():
    if session["username"] == None or session["isadmin"] == True:
        return render_template("error.html")
    recip = session["userID"]
    sql = "SELECT * FROM messages"
    result = db.session.execute(sql)
    
    msgs = result.fetchall()
    temp = []
    
    for message in msgs:
        if message[3] == recip or message[3] == -1:
            tempmsg = []
            tempmsg.append(message[0])
            tempmsg.append(message[2])
            temp.append(tempmsg)
    
    msgs = temp
        
    return render_template("messages.html", viestit=msgs)
    
@app.route("/add")
def add():
    if session["isadmin"] == False:
        return render_template("accesserror.html")
    return render_template("add.html")
    
@app.route("/insertcode")
def insertcode():
    if session["isadmin"] == True or session["username"] == None:
        return redirect("/frontpage")
    return render_template("insertcode.html")
    
@app.route("/getcoins", methods=["POST"])
def getcoins():
    if session["isadmin"] == True or session["username"] == None:
        return redirect("/frontpage")
    code = request.form["code"]
    
    sql = "SELECT coinamount FROM coincodes WHERE code = :code"
    result = db.session.execute(sql, {"code":code})
    
    kolikot = result.fetchall()[0]

    if kolikot == None or kolikot[0] == 0:
        return redirect("/error")
        
    coins = kolikot[0] + session["coins"]
    session["coins"] = coins
    
    
    sql = "UPDATE users SET coins = :coins WHERE id = :userid"
    db.session.execute(sql, {"coins":coins, "userid":session["userID"]})
    db.session.commit()
    
    sql = "DELETE FROM coincodes WHERE code = :code"
    result = db.session.execute(sql, {"code":code})
    db.session.commit()
    
    return redirect("/frontpage")
    
@app.route("/addcoincode")
def addcoincode():
    if session["isadmin"] == False:
        return render_template("accesserror.html")
    return render_template("addcoincode.html")
    
@app.route("/addcode", methods=["POST"])
def addcode():
    if session["isadmin"] == False:
        return render_template("accesserror.html")
    code = request.form["code"]
    coinamount = request.form["coinamount"]
    
    sql = "INSERT INTO coincodes (code, coinamount) VALUES (:code, :coinamount)"
    
    db.session.execute(sql, {"code":code, "coinamount":coinamount})
    db.session.commit()
    
    
    if request.form["ilmoitus"] == "0":
        print("täällä ollaan")
        sql = "INSERT INTO messages (message, sender, sendername, recip) VALUES ('Uusi kolikkokoodi julkaistu! Käytä koodi "+code+" ennenkuin muut ehtivät!', :sender, :sendername, -1)"
        sender = session["userID"]
        sendername = session["username"]
        db.session.execute(sql, {"sender":sender, "sendername":sendername})
        db.session.commit()
    
    return redirect("/frontpage")
    
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
    card = request.form["name"]
    sql = "DELETE FROM cards WHERE id=:id"
    db.session.execute(sql, {"id":card})
    db.session.commit()
    
    sql ="DELETE FROM circulation WHERE cardid = :cardid"
    db.session.execute(sql, {"cardid":card})
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
