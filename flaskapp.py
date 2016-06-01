# -*- coding: utf-8 -*-
__author__ = 'sargdsra'

from flask import Flask, render_template, session, request, json, redirect, url_for
from database import check_user, add_user, search, get_summary, get_post, create_s, get_res

app = Flask(__name__)
app.secret_key = '\xa2\x1a\xb2B\x7f\x06\x95q\x00&\xe2\x0e\x89C\xbe\x84\xbb\xbf\xb1\x917\x96T\xbb'


@app.before_first_request
def init_db():
    create_s()


@app.route("/")
def f_home():
    if session.get("user"):
        user = session["user"]
        return render_template("ad-search.html", Username=user)
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
            return render_template("ad-search.html", Username=user)
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
                return render_template("ad-search.html", Username=user)
    return render_template("main.html")


@app.route('/search')
def f_search():
    if session.get("user"):
        search_dict = {}
        """static_possible_search_args = ["word", "overall", "genre"]
		possible_search_args = ["min_storage", "max_storage", "min_price", "max_price"]
		possible_search_args += ["min_discount", "max_discount", "min_statics", "max_statics", "min_release_date"]
		possible_search_args += ["max_release_date", "min_os", "max_os", "min_processor", "max_processor"]
		possible_search_args += ["min_memory", "max_memory", "min_graphics", "max_graphics", "min_directX"]
		possible_search_args += ["max_directX", "min_reviews", "max_reviews"]"""
        # search_dict["min_os"] = request.args.get("os", "", type=str)
        search_dict["min_os"] = ""
        search_dict["min_graphics"] = ""
        search_dict["min_processor"] = ""
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
        search_dict["min_reviews"] = "1100"
        search_dict["max_reviews"] = ""
        print "123"
        if search(search_dict):
            stup = list(search(search_dict))
            slis = [list(i) for i in stup]
            for item in slis:
                item[2] = str(item[2])
            return json.dumps(slis)
        return "0"
    return redirect(url_for("f_home"))


@app.route('/summary')
def f_summary():
    if session.get("user"):
        page_number = request.args.get("page_number", "0", type=str)
        print "123"
        if get_summary(page_number):
            stup = list(get_summary(page_number))
            slis = [list(i) for i in stup]
            for item in slis:
                item[2] = str(item[2])
            return json.dumps(slis)
        return "0"
    return redirect(url_for("f_home"))


@app.route('/game')
def f_game():
    if session.get("user"):
        inf = request.args.get("inf", "", type=str)
        print "123"
        if get_post(inf):
            stup = list(get_post(inf))
            stup[2] = str(stup[2])
            return json.dumps(stup)
        return "0"
    return redirect(url_for("f_home"))


@app.route("/statistics", methods=['POST'])
def f_stat():
    if session.get("user"):
        if request.method == 'POST':
            json_request = request.get_json(silent=True)
            # if json_request['requestType'] == "overall":
            if request.form['requestType'] == "overall":
                very_positive = get_res("SELECT COUNT(overall) FROM games WHERE overall='Very Positive';")
                positive = get_res("SELECT COUNT(overall) FROM games WHERE overall='Positive';")
                overwhelmingly_positive = get_res("SELECT COUNT(overall) FROM games WHERE overall='Overwhelmingly Positive';")
                mostly_positive = get_res("SELECT COUNT(overall) FROM games WHERE overall='Mostly Positive';")
                res = [very_positive[0][0], positive[0][0], overwhelmingly_positive[0][0], mostly_positive[0][0]]
                return json.dumps(res)
            if json_request['requestType'] == "topstatics":
                inf = get_res("SELECT * FROM games ORDER BY statics DESC LIMIT 10;")
                inf = list(inf)
                res = [list(i) for i in inf]
                for item in res:
                    item[8] = str(item[8])
                return json.dumps(res)
            if json_request['requestType'] == "aveofall":
                ave_of_no_discount = float(get_res("SELECT AVG(purchase_price) FROM games WHERE discount='0';")[0][0])
                ave_of_have_discount = float(get_res("SELECT AVG(original_price) FROM games WHERE discount<>'0';")[0][0])
                # if error occurs change <> into !=
                ave = "{0:.2f}".format((ave_of_no_discount + ave_of_have_discount) / 2)
                return json.dumps(ave)
            if json_request['requestType'] == "newgames":
                inf = get_res("SELECT * FROM games ORDER BY release_date DESC LIMIT 10;")
                inf = list(inf)
                res = [list(i) for i in inf]
                for item in res:
                    item[8] = str(item[8])
                return json.dumps(res)
            if json_request['requestType'] == "topreviews":
                inf = get_res("SELECT * FROM games ORDER BY reviews DESC LIMIT 10;")
                inf = list(inf)
                res = [list(i) for i in inf]
                for item in res:
                    item[8] = str(item[8])
                return json.dumps(res)
    return redirect(url_for("f_home"))


@app.route("/p_search", methods=['POST'])
def f_go_search():
    if request.method == 'POST' and session.get("user"):
        return render_template("ad-search.html")
    return render_template("main.html")


@app.route("/p_inf")
def f_go_info():
    if session.get("user"):
        return render_template("info.html")
    return render_template("main.html")


if __name__ == '__main__':
    app.run(debug=True, port=4958)
