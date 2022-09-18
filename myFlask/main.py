from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") #decorator
def home():
    return render_template("home.html")

@app.route("/<name>") #decorator
def user(name):
    # return f"<h1>Hello, {name}</h1>"
    return render_template("home.html", myName=name)

@app.route("/info")
def info():
    return render_template("info.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

app.run()