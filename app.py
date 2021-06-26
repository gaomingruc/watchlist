import os
import click
from flask import Flask, url_for, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + \
    os.path.join(app.root_path, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev"
db = SQLAlchemy(app)


class User(db.Model):
    """数据库中定义user表"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    """数据库中定义movie表"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(20))


@app.cli.command()
@click.option("--drop", is_flag=True, help="删除数据库候再新建数据库")
def initdb(drop):
    """使用flask initdb --drop 初始化数据库"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("初始化数据库")


@app.cli.command()
def forge():
    """使用flask forge生成虚拟数据"""
    db.create_all()

    name = "高明"
    movies = [
        {"title": "送你一朵小红花", "year": "2020"},
        {"title": "姜子牙", "year": "2020"},
        {"title": "蝙蝠侠：黑暗骑士 The Dark Knight", "year": "2008"},
        {"title": "潜伏", "year": "2009"},
        {"title": "红星照耀中国", "year": "2019"},
        {"title": "徒手攀岩 Free Solo", "year": "2018"},
        {"title": "哪吒之魔童降世", "year": "2019"},
        {"title": "乒乓 ピンポン THE ANIMATION", "year": "2014"},
        {"title": "穹顶之下", "year": "2015"},
        {"title": "大腕", "year": "2001"},
    ]

    user = User(name=name)
    db.session.add(user)
    for movie in movies:
        movie_to_db = Movie(title=movie["title"], year=movie["year"])
        db.session.add(movie_to_db)
    db.session.commit()
    click.echo("虚拟数据已生成")


@app.route("/", methods=["GET", "POST"])
def index():
    """
    主页视图函数
    GET方法渲染电影记录结果
    POST方法处理新增电影记录表单数据
    """
    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year")
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash("您输入了错误的电影记录")
            return redirect(url_for("index"))
        movie_to_db = Movie(title=title, year=year)
        db.session.add(movie_to_db)
        db.session.commit()
        flash("新电影已添加")
        return redirect(url_for("index"))

    movies = Movie.query.all()
    return render_template("index.html", movies=movies)


@app.route("/movie/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year")
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash("您输入了错误的电影记录")
            return redirect(url_for("edit", movie_id=movie.id))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash("电影已修改")
        return redirect(url_for("index"))
    return render_template("edit.html", movie=movie)


@app.route("/movie/delete/<int:movie_id>", methods=["POST"])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("%s已删除" % movie.title)
    return redirect(url_for("index"))


@ app.errorhandler(404)
def page_not_found(e):
    """404错误处理函数"""
    return render_template("404.html"), 404


@ app.errorhandler(405)
def page_not_found(e):
    """405错误处理函数"""
    return render_template("405.html"), 404


@ app.context_processor
def inject_user():
    """将user注入模版上下文，使得渲染模版时不用再传入user变量"""
    user = User.query.first()
    return dict(user=user)
