from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1> hello world</h1>"

@app.route("/dbtest")
def detest():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("select * from user")
    data = cursor.fetchall()
    return render_template("db.html",data=data)