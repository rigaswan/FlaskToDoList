from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1> hello world</h1>"

if __init__ == "__main__":
    app.run(debug=True) 