from flask import Flask, render_template, request, redirect, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_session import Session
from datetime import timedelta, datetime, timezone
import pytz
import requests, json


app = Flask(__name__)
app.secret_key = 'super secret key'
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


def get_db_connection():
    conn = sqlite3.connect("TDL.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        
        newtext = request.form.get("thingtodo")
        #username = request.form.get("username")
        print(newtext)
        if len(newtext) < 1:
            flash("Please enter your thing-to-do.", category="error") 
            return redirect("/")
        # insert into data base
        else:
            conn = get_db_connection()
            cursor = conn.cursor() 
            # detail_hktime=datetime.now(timezone.utc)+timedelta(hours=8)
            # hktime=datetime.strftime(detail_hktime, '%Y-%m-%d %H:%M')

            hktz = pytz.timezone("Asia/Hong_Kong")
            detail_hktime=datetime.now(hktz)
            hktime = detail_hktime.strftime("%Y-%m-%d %H:%M")

            cursor.execute(
                    "INSERT INTO todolist (data,dt, user_id) values(?,?,?); ", 
                    (newtext,hktime,session["user_id"])
            )
            conn.commit()
            cursor.close()
            conn.close()
            return redirect("/")
    else:
        if session.get("logged_in"):
            conn = get_db_connection()
            cursor = conn.cursor() 
            cursor.execute(
                    "SELECT * FROM users WHERE name = ? ;", 
                    (session["name"],)
            )
            result = cursor.fetchone()
            session["user_id"] = result[0]
            #print (session["user_id"])
            # result[0]: user_id | result[1]: username | result[2]: password_hashed

            cursor.execute(
                    "SELECT * FROM todolist WHERE user_id = ? ;", 
                    (session["user_id"] ,)
            )
            data = cursor.fetchall()
            #print(data[0][0])
            cursor.close()
            conn.close()

            return render_template("index.html", title = "Homepage", todolist=data)
        return redirect("/login")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
                    "SELECT * FROM users WHERE name = ? ;", 
                    (username,)
        )
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(result) != 0:
            flash("username NOT avaiable.", category="error")
        elif len(username) < 2:
            flash("Your username is too short!", category="error")
        elif password != password2:
            flash("Password don\'t match!", category="error")
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            hash_p = generate_password_hash(password)
            cursor.execute(
                        'INSERT INTO users (name,password) values(?,?);',
                        (username, hash_p)
                    )
            conn.commit()
            cursor.close()
            conn.close()

            session["logged_in"] = True
            session["name"] = username
            flash("Account created!", category="success")
            return redirect("/")
    return render_template("register.html", title = "Register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
                    "SELECT * FROM users WHERE name = ? ;", 
                    (username,)
        )
        result = cursor.fetchone()
        # result[0]: user_id | result[1]: username | result[2]: password_hashed
        cursor.close()
        conn.close()   

        if result:
            if check_password_hash(result[2],password):
                user_id = result[0]
                session["logged_in"] = True
                session["name"] = result[1]
                session["user_id"] = result[0]
                flash("Logged in successfully!", category="success")
                return redirect("/",)
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("username does not exists", category="error")


    return render_template("login.html", title="Login page")


@app.route("/logout")
def logout():
    session["logged_in"] = False
    session.pop("name", None)
    session.pop("user_id",None)
    flash("You\'re logged out.", category="success")
    return redirect("/")

@app.route("/delete/<int:thingid>", methods=["GET", "POST"])
def delete(thingid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
                "DELETE FROM todolist WHERE id = ? ;", 
                (thingid,)
    )
    conn.commit()
    cursor.close()
    conn.close()   
    return redirect("/")

@app.route("/etaO")
def etaO():
    url = "https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line=ISL&sta=HKU"
    urljson = requests.get(url)
    etadata = json.loads(urljson.text)
    
    return render_template("eta.html", title = "Next Train Arrival Time", etadata=etadata["data"]["ISL-HKU"], time=etadata["data"]["ISL-HKU"]["curr_time"])

@app.route("/eta/<string:station>")
def eta(station):
    
    if station == "WHA":
        line = "KTL"
    else:
        line = "ISL"

    url = f"https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line={line}&sta={station}"
    urljson = requests.get(url)
    etadata = json.loads(urljson.text)
    
    return render_template("eta.html", title = "Next Train Arrival Time", 
                           etadata=etadata["data"][line+"-"+station],
                           station = station,
                           time=etadata["data"][line+"-"+station]["curr_time"]
                        )


if __name__ == "__main__":
    
    app.run(debug=True)
