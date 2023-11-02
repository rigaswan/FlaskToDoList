from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        return "aslkfhd"
    return render_template("index.html", title = "Homepage")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if len(username) < 2:
            flash("Your username is too short!", category="error")
        elif password != password2:
            flash("Password don\'t match!", category="error")
        else:
            flash("Account created!", category="success")
            return redirect("/")
    return render_template("register.html", title = "Register")

@app.route("/login")
def login():

    return render_template("login.html", title="Login page")



if __name__ == "__main__":
    
    app.run(debug=True)