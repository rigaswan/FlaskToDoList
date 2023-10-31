from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

db = sqlite3.connect("test.db")
cursor = db.cursor()
cursor.execute(" create table user (id varchar(20) primary key autoincrement, name varchar(20)" )
cursor.execute('insert into user (name) values (\"wck\")')
db.commit()
cursor.close()
db.close()

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

if __name__ == "__main__":
    app.run(debug=True)