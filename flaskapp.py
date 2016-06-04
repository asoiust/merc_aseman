# -*- coding: utf-8 -*-
__author__ = 'sargdsra'

from flask import Flask, render_template, session, request, json, redirect, url_for
from database import check_user, add_user, search, get_summary, get_post, create_s, get_res
from req import check
from app import go_in_link_ver4

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
    return render_template("main.html", items=get_4())


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
    return render_template("main.html", items=get_4())


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
    return render_template("main.html", items=get_4())


@app.route('/search', methods=['GET'])
def f_search():
    if session.get("user"):
        search_dict = dict()
        search_dict["min_storage"] = request.args.get("min_storage", "", type=str)
        search_dict["max_storage"] = request.args.get("max_storage", "", type=str)
        search_dict["min_memory"] = request.args.get("min_memory", "", type=str)
        search_dict["rec_memory"] = request.args.get("max_memory", "", type=str)
        search_dict["min_os"] = request.args.get("min_os", "", type=str)
        search_dict["rec_os"] = request.args.get("rec_os", "", type=str)
        search_dict["min_graphics"] = request.args.get("min_graphics", "", type=str)
        search_dict["rec_graphics"] = request.args.get("rec_graphics", "", type=str)
        search_dict["min_processor"] = request.args.get("min_processor", "", type=str)
        search_dict["rec_processor"] = request.args.get("rec_processor", "", type=str)
        search_dict["min_price"] = request.args.get("min_price", "", type=str)
        search_dict["max_price"] = request.args.get("max_price", "", type=str)
        search_dict["min_directX"] = request.args.get("min_directX", "", type=str)
        search_dict["rec_directX"] = request.args.get("rec_directX", "", type=str)
        search_dict["min_discount"] = request.args.get("min_discount", "", type=str)
        search_dict["max_discount"] = request.args.get("max_discount", "", type=str)
        search_dict["min_reviews"] = request.args.get("min_reviews", "", type=str)
        search_dict["max_reviews"] = request.args.get("max_reviews", "", type=str)
        search_dict["min_statics"] = request.args.get("min_statics", "", type=str)
        search_dict["max_statics"] = request.args.get("max_statics", "", type=str)
        search_dict["min_overall"] = request.args.get("min_overall", "", type=str)
        search_dict["max_overall"] = request.args.get("max_overall", "", type=str)
        search_dict["genre"] = request.args.get("genre", "", type=str)
        search_dict["word"] = request.args.get("word", "", type=str)
        search_dict["min_release_date"] = request.args.get("min_release_date", "", type=str)
        search_dict["max_release_date"] = request.args.get("max_release_date", "", type=str)
        print "123"
        search_result = search(search_dict, "0")
        print search_result
        if search_result:
            stup = list(search_result)
            slis = [list(i) for i in stup]
            for item in slis:
                item[2] = str(item[2])
                item[3] = str(item[3])
                if "Publisher" in item[3]:
                    d = item[3].index("Publisher")
                    item[3] = item[3][:d]
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
                item[3] = str(item[3])
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
            stup[8] = str(stup[8])
            stup[17] = str(stup[17])
            if "Publisher" in stup[17]:
                d = stup[17].index("Publisher")
                stup[17] = stup[17][:d]
            return json.dumps(stup)
        return "0"
    return redirect(url_for("f_home"))


@app.route("/statistics", methods=['POST'])
def f_stat():
    if session.get("user"):
        if request.method == 'POST':
            if request.form['requestType'] == "overall":
                very_positive = get_res("SELECT COUNT(overall) FROM games WHERE overall='Very Positive';")
                positive = get_res("SELECT COUNT(overall) FROM games WHERE overall='Positive';")
                overwhelmingly_positive = get_res(
                    "SELECT COUNT(overall) FROM games WHERE overall='Overwhelmingly Positive';")
                mostly_positive = get_res("SELECT COUNT(overall) FROM games WHERE overall='Mostly Positive';")
                res = [very_positive[0][0], positive[0][0], overwhelmingly_positive[0][0], mostly_positive[0][0]]
                return json.dumps(res)
            if request.form['requestType'] == "topstatics":
                inf = get_res("SELECT title,static,purchase_price,after_discount FROM games ORDER BY static DESC LIMIT 10;")
                inf = list(inf)
                res = [list(i) for i in inf]
                print res
                return json.dumps(res)
            if request.form['requestType'] == "aveofall":
                ave_of_no_discount = float(get_res("SELECT AVG(price) FROM summary WHERE discount = 0")[0][0])
                ave_of_have_discount = float(
                    get_res("SELECT AVG(final_price) FROM summary WHERE discount<>'0';")[0][0])
                # if error occurs change <> into !=
                ave = "{0:.2f}".format((ave_of_no_discount + ave_of_have_discount) / 2)
                return json.dumps((ave,))
            if request.form['requestType'] == "newgames":
                inf = get_res("SELECT * FROM games ORDER BY release_date DESC LIMIT 10;")
                inf = list(inf)
                res = [list(i) for i in inf]
                for item in res:
                    item[8] = str(item[8])
                    item[17] = str(item[17])
                    if "Publisher" in item[17]:
                        d = item[17].index("Publisher")
                        item[17] = item[17][:d]
                return json.dumps(res)
            if request.form['requestType'] == "topreviews":
                inf = get_res("SELECT * FROM games ORDER BY reviews DESC LIMIT 10;")
                inf = list(inf)
                res = [list(i) for i in inf]
                for item in res:
                    item[8] = str(item[8])
                    item[17] = str(item[17])
                    if "Publisher" in item[17]:
                        d = item[17].index("Publisher")
                        item[17] = item[17][:d]
                return json.dumps(res)
            if request.form['requestType'] == "count_of_all_games":
                inf = get_res("SELECT COUNT(overall) FROM games;")
                inf = inf[0][0]
                res = inf
                return json.dumps((res,))
            if request.form['requestType'] == "avg_static":
                inf = get_res("SELECT AVG(static) FROM games;")
                inf = float(inf[0][0])
                res = "{0:.2f}".format(inf)
                return json.dumps((res,))
            if request.form['requestType'] == "count_of_all_free_games":
                inf = get_res("SELECT COUNT(user_tags) FROM games WHERE user_tags LIKE '%Free to Play%';")
                res = int(inf[0][0])
                return json.dumps((res,))
            if request.form['requestType'] == "user_tags":
                inf = get_res("SELECT user_tags FROM games")
                res = check(inf, "tg")
                return json.dumps(res)
            if request.form['requestType'] == "genre":
                inf = get_res("SELECT details FROM games")
                res = check(inf, "ge")
                return json.dumps(res)
            if request.form['requestType'] == "averageDiscount":
                result = get_res("SELECT AVG(final_price) FROM summary WHERE discount > 0")
                return json.dumps(result[0])
    return redirect(url_for("f_home"))


@app.route("/p_search", methods=['POST'])
def f_go_search():
    if request.method == 'POST' and session.get("user"):
        return render_template("ad-search.html")
    return render_template("main.html", items=get_4())


@app.route("/p_inf")
def f_go_info():
    if session.get("user"):
        return render_template("info.html")
    return render_template("main.html", items=get_4())


@app.route("/logout")
def f_logout():
    if session.get("user"):
        session.clear()
    return render_template("main.html", items=get_4())


@app.route('/lab', methods=['GET'])
def f_lab():
    return render_template("main.html", items=get_4())


@app.route('/game/<int:game_id>')
def f_g_p_game(game_id):
    if session.get("user"):
        inf = str(get_res("SELECT url FROM games WHERE id=" + str(game_id) + ";")[0][0])
        go_in_link_ver4(inf)
        inf = list(get_res("SELECT id, title, description, min_processor, min_memory, min_graphics, min_storage, rec_storage, rec_processor, rec_memory, rec_graphics FROM games WHERE id=" + str(
            game_id) + ";")[0])
        res = str(get_res("SELECT image FROM summary WHERE game_id=" + str(game_id) + ";")[0][0])
        inf.append(res)
        return render_template("game.html", item=inf, Username=session["user"])
    return render_template("main.html", items=get_4())


def get_4():
    inf = get_res("SELECT id, description FROM games ORDER BY static DESC LIMIT 4;")
    inf = list(inf)
    res = [list(i) for i in inf]
    for item in res:
        st = "SELECT image FROM summary WHERE game_id=" + str(item[0]) + ";"
        inf = get_res(st)
        item.append(str(inf[0][0]))
    return res


if __name__ == '__main__':
    app.run(debug=True, port=4958)
