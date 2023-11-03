from flask import Flask, render_template, request, redirect, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super secret key'

def get_db_connection():
    conn = sqlite3.connect("TDL.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        return "aslkfhd"
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        # supppos the user_id is 1
        cursor.execute(
                "SELECT * FROM todolist WHERE user_id = ? ;", 
                (1,)
        )
        data = cursor.fetchall()
        #print(data[0][0])
        cursor.close()
        conn.close()

        return render_template("index.html", title = "Homepage", todolist=data)

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
        #print(result[0])
        cursor.close()
        conn.close()   

        if result:
            if check_password_hash(result[2],password):
                user_id = result[0]
                flash("Logged in successfully!", category="success")
                return redirect("/",)
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("username does not exists", category="error")


    return render_template("login.html", title="Login page")



if __name__ == "__main__":
    
    app.run(debug=True)