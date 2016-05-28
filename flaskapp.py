# -*- coding: utf-8 -*-
__author__ = 'sargdsra'

from flask import Flask, render_template, session, request
from database import check_user, add_user

app = Flask(__name__)
app.secret_key = 'amir'


@app.route("/")
def f_home():
    if session.get("user"):
        user = session["user"]
        return render_template("main.html", Username=user)
    return render_template("main.html")


@app.route("/login", methods=['POST'])
def f_login():
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        check = request.form.getlist('check')
        if check_user(user, passw):
            if check:
                session['user'] = user
            return render_template("main.html", Username=user)
    return render_template("main.html")


@app.route("/signup", methods=['POST'])
def f_sign_up():
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        repassw = request.form['re_password']
        email = request.form['email']
        if passw == repassw:
            if add_user(user, passw, email):
                session['user'] = user
                return render_template("main.html", Username=user)
    return render_template("main.html")

if __name__ == '__main__':
    app.run(debug=True, port=4958)
