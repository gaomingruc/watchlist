from flask import Flask, url_for
app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to My Watchlist!"


@app.route("/user/<name>")
def user_page(name):
    return "hello, %s" % name


@app.route("/test")
def test_url_for():
    content = url_for("user_page", name="ming")
    return content
