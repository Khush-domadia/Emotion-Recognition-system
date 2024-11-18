from flask import render_template
from base import app


@app.route('/')
def login():
    return render_template("admin/login.html")


@app.route('/home')
def index():
    return render_template("admin/index.html")
