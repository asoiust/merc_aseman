# -*- coding: utf-8 -*-
__author__ = 'sargdsra'

from flask import Flask, render_template, session, request, jsonify
from database import check_user, add_user, search

app = Flask(__name__)
app.secret_key = 'amir'


@app.route("/")
def f_home():
    if session.get("user"):
        user = session["user"]
        session.clear()
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


@app.route('/search')
def f_search():
    search_dict = {}
    """static_possible_search_args = ["word", "overall", "genre"]
        possible_search_args = ["min_storage", "max_storage", "min_price", "max_price"]
        possible_search_args += ["min_discount", "max_discount", "min_statics", "max_statics", "min_release_date"]
        possible_search_args += ["max_release_date", "min_os", "max_os", "min_processor", "max_processor"]
        possible_search_args += ["min_memory", "max_memory", "min_graphics", "max_graphics", "min_directX"]
        possible_search_args += ["max_directX", "min_reviews", "max_reviews"]"""
    search_dict["min_os"] = request.args.get("os", "", type=str)
    search_dict["min_graphics"] = request.args.get("graphic_card", "", type=str)
    search_dict["min_processor"] = request.args.get("proccessor", "", type=str)
    search_dict["min_directX"] = ""
    search_dict["word"] = ""
    search_dict["overall"] = ""
    search_dict["genre"] = ""
    search_dict["min_storage"] = ""
    search_dict["max_storage"] = ""
    search_dict["min_price"] = ""
    search_dict["max_price"] = ""
    search_dict["min_discount"] = ""
    search_dict["max_discount"] = ""
    search_dict["min_statics"] = ""
    search_dict["max_statics"] = ""
    search_dict["min_release_date"] = ""
    search_dict["max_release_date"] = ""
    search_dict["max_os"] = ""
    search_dict["max_processor"] = ""
    search_dict["min_memory"] = ""
    search_dict["max_memory"] = ""
    search_dict["max_graphics"] = ""
    search_dict["max_directX"] = ""
    search_dict["min_reviews"] = ""
    search_dict["max_reviews"] = ""
    print "123"
    return jsonify(search(search_dict))


@app.route("/p_search", methods=['POST'])
def f_go_search():
    if request.method == 'POST':
        return render_template("ad-search.html")


if __name__ == '__main__':
    app.run(debug=True, port=4958)
