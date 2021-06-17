from flask import Flask, url_for, render_template
app = Flask(__name__)


name = "高明"
movies = [
    {"title": "流浪地球", "rate_score": "5"},
    {"title": "test movie", "rate_score": "4"}
]


@app.route("/")
def index():
    return render_template("index.html", name=name, movies=movies)
