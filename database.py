# -*- coding: utf-8 -*-
import MySQLdb as m                                            # All over the program MySQLdb called m
from _config import _DBNAME, _DBHOST, _DBPASS, _DBUSER


class MySql:
    """
    | Never creates an instance from this class.For getting connection object just call the connection static
    | method.
    """
    connection_obj = None

    @staticmethod
    def connection():
        instance = MySql()
        MySql.connection_obj = instance._connection
        return MySql.connection_obj

    def __init__(self):
        try:
            self._connection = m.Connection(_DBHOST, _DBUSER, _DBPASS, _DBNAME, use_unicode=True)
            self._connection.set_character_set('utf8')
            self._connection.ping(True)
        except m.Error as e:
            print e


def create_game_table():
    """
    | This void function creates game table if it not exists!
    :return:
    """
    try:
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS games(id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,"
                           "title VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci,"
                           "url VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci,"
                           "overall VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci,"
                           "description TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci,"
                           "user_tags VARCHAR(255),static VARCHAR(255),purchase_price FLOAT ,"
                           "release_date DATE,discount FLOAT,min_os VARCHAR(255),"
                           "min_processor VARCHAR(255),"
                           "min_memory VARCHAR(255),min_graphics VARCHAR(255),min_directx VARCHAR(255),"
                           "min_storage VARCHAR(255),min_notes VARCHAR(255),details VARCHAR(255)"
                           ",rec_directx VARCHAR(255),rec_storage VARCHAR(255),rec_notes VARCHAR(255),"
                           "rec_os VARCHAR(255),rec_processor VARCHAR(255),after_discount INT,"
                           "rec_memory VARCHAR(255),rec_graphics VARCHAR(255), original_price FLOAT,reviews INT)")
            connection_obj.commit()
    except Exception as e:
        print(e)


def create_users_table():
    """
    | This void function creates game table if it not exists!
    :return:
    """
    try:
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS users(id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,"
                           "user_name VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci,"
                           "password VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci,"
                           "email VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci)")
            connection_obj.commit()
    except Exception as e:
        print(e)


def create_summary_table():
    try:
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS summary(id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,"
                           "title VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci,url VARCHAR(255),"
                           "release_date DATE,discount FLOAT,price FLOAT,final_price FLOAT,image VARCHAR(255),"
                           "game_id INT, FOREIGN KEY(game_id) REFERENCES games(id))")
            connection_obj.commit()
    except Exception as e:
        print(e)


def create_gpu_table():
    try:
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS gpu(id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,"
                           "title VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci)")
            connection_obj.commit()
    except Exception as e:
        print(e)


def create_cpu_table():
    try:
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cpu(id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,"
                           "title VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci)")
            connection_obj.commit()
    except Exception as e:
        print(e)


def check_game_exists(url):
    """
    | This function gets url and if a game with same url exists return that's id number in a tuple.
    :param url:
    :return: tuple|int
    """
    try:
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("SELECT id FROM games WHERE url = %s", (url,))
            return cursor.fetchone()
    except Exception as e:
        print(e)
        return -1


def add_game(kwargs):
    """
    | This function adds a new game in to the database;
    | if game add correctly, returns True, If title or url is None, returns False and if any problem occurs
    | returns
    :param title:
    :param url:
    :param args:
    :return: bool|int
    """
    try:
        if type(kwargs) == list:
            return
        if kwargs['title'] == "0":
            return False
        if kwargs["discount"] == "0":
            kwargs["after_discount"] = "0"
        cols = ["title", "url", "overall", "description", "user_tags", "static", "purchase_price",
                "release_date"]
        cols += ["discount", "min_os", "min_processor", "min_memory", "min_graphics", "min_directx",
                 "min_storage"]
        cols += ["min_notes", "details", "rec_directx", "rec_storage", "rec_notes", "rec_os", "rec_processor"]
        cols += ["after_discount", "rec_memory", "rec_graphics", "original_price", "reviews"]
        if kwargs['purchase_price'] == "Free To Play" or kwargs['purchase_price'] == "Free":
            kwargs['purchase_price'] = "0"
        for col_name in cols:
            if col_name not in kwargs.keys():
                kwargs.update({col_name: " "})
        query_tuple = tuple()
        for col_name in cols:
            if type(kwargs[col_name]) == list and len(kwargs[col_name]) == 1:
                if kwargs[col_name][0] is None:
                    query_tuple += ("",)
                    continue
                try:
                    query_tuple += (kwargs[col_name][0].encode('utf-8'),)
                except UnicodeDecodeError:
                    query_tuple += (kwargs[col_name][0].decode('unicode_escape').encode('ascii', 'ignore'),)
            elif type(kwargs[col_name]) == list:
                pr_result = ""
                for tag in kwargs[col_name]:
                    pr_result += tag.encode('utf-8') + "|"
                query_tuple += (pr_result,)
            elif type(kwargs[col_name]) == unicode:
                query_tuple += (kwargs[col_name].encode('utf-8'),)
            else:
                query_tuple += (kwargs[col_name],)
        into_string = ""
        url = kwargs["url"]
        if check_game_exists(url):
            cols.remove("url")
            for key in cols:
                into_string += key + " = %s,"
            into_string = into_string[:len(into_string) - 1]
            into_string = into_string.replace("statistics", "static")
            query_tuple = tuple([str(x) for x in query_tuple if x != url])
            del kwargs["url"]
            connection_obj = MySql.connection()
            with connection_obj:
                cursor = connection_obj.cursor()
                if type(query_tuple[0]) == tuple:
                    query_tuple = query_tuple[0]
                print kwargs
                print query_tuple
                print into_string
                print url
                cursor.execute("UPDATE games SET " + into_string + " WHERE url = %s", query_tuple + (url,))
                connection_obj.commit()
        else:
            for key in cols:
                into_string += key + ","
            into_string = into_string[:len(into_string) - 1]
            into_string = into_string.replace("statistics", "static")
            connection_obj = MySql.connection()
            with connection_obj:
                cursor = connection_obj.cursor()
                cursor.execute(
                    "INSERT INTO games(" + into_string + ") VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)",
                    query_tuple)
                connection_obj.commit()
                return True
    except Exception as e:
        print(e)
        print kwargs
        print url
        print "_____________________"
        return -1


def get_all_game():
    try:
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("SELECT * FROM games")
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)
        return -1


def add_summary(input_list):
    connection_onj = MySql.connection()
    for input_dict in input_list:
        limit = len(input_dict['title'])
        with connection_onj:
            for counter in range(limit):
                title = input_dict['title'][counter].encode('utf-8')
                url = input_dict['url'][counter].encode('utf-8')
                discount = input_dict['discount'][counter].encode('utf-8')
                if discount:
                    discount = discount.replace("-", "").replace("%", "")           # Remove useless characters from discount
                price_tuple = input_dict['price'][counter]
                if len(price_tuple) == 1:
                    price = price_tuple[0].encode('utf-8').replace("$", "")
                    final_price = "0"
                else:
                    # price = price_tuple[0].encode('utf-8')
                    price = price_tuple[1].encode('utf-8').replace("$", "")
                    final_price = price_tuple[1].encode('utf-8')
                image = input_dict["pics"][0].encode("utf-8")
                release = input_dict['rdate'][counter]
                months_name = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                date_list = release.encode("utf-8").split(" ")
                release_date = date_list[2] + "-" + str(months_name.index(date_list[1].replace(',', "")) + 1) + "-" + date_list[0]
                # Send to the database

                cursor = connection_onj.cursor()
                cursor.execute("SELECT id FROM games WHERE url = %s", (url,))
                try:
                    game_id = cursor.fetchone()[0]
                except IndexError:
                    return
                cursor.execute("INSERT INTO summary(title,url,release_date,discount,price,final_price,image,game_id) "
                               "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                               (title, url, release_date, discount, price, final_price, image, str(game_id)))
                connection_onj.commit()


def check_user(username, password):
    """
    | This function gets username and password and returns user id of the user with same username and password in a
    | tuple. If username or password is empty returns False;
    :param username:
    :param password:
    :return: tuple|int|bool
    """
    try:
        if not username or not password:
            return False
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("SELECT id FROM users WHERE user_name = %s AND password = %s", (username, password))
            res = cursor.fetchone()
            if res == None:
                return False
            else:
                return res
    except Exception as e:
        print(e)
        return 0


def add_user(username, password, email):
    """
    | This void function add new user to users table if username and email didn't use before.
    :param username:
    :param email:
    :param password:
    :return: void
    """
    try:
        if not username or not password or not email:
            return False
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            # if not check_user_with_email(email) and not check_user_with_username(username):
            #     return False
            cursor.execute("INSERT INTO users(user_name,password,email) VALUES(%s,%s,%s)", (username, password, email))
            connection_obj.commit()
            return True
    except Exception as e:
        print(e)
        return 0


def check_user_with_email(email):
    """
    | This function returns user id with specific email address in a tuple.If email is empty returns False.
    | If any error occurs, returns -1
    :param email:
    :return: bool|int|tuple
    """
    try:
        if not email:
            return False
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            res = cursor.fetchone()
            if res == None:
                return False
            else:
                return res
    except Exception as e:
        print(e)
        return 0


def check_user_with_username(username):
    """
    | This function returns user id with specific username in a tuple.If username is empty returns False.
    | If any error occurs, returns -1
    :param email:
    :return: bool|int|tuple
    """
    try:
        if not username:
            return False
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("SELECT id FROM users WHERE user_name = %s", (username,))
            res = cursor.fetchone()
            if res == None:
                return False
            else:
                return res
    except Exception as e:
        print(e)
        return 0


def search(input_dict):
    """
    | This function gets a dictionary and returns result as a tuple.
    :param input_dict:dict
    :return:tuple|int
    """
    try:
        for encoder in input_dict:
            input_dict[encoder] = input_dict[encoder].encode("utf-8")
        static_possible_search_args = ["word", "overall", "genre"]
        possible_search_args = ["min_storage", "max_storage", "min_price", "max_price"]
        possible_search_args += ["min_discount", "max_discount", "min_statics", "max_statics", "min_release_date"]
        # possible_search_args += ["max_release_date", "min_os", "rec_os", "min_processor", "rec_processor"]
        possible_search_args += ["max_release_date", "min_os", "min_processor"]
        # possible_search_args += ["min_memory", "rec_memory", "min_graphics", "rec_graphics", "min_directX"]
        possible_search_args += ["min_memory", "min_graphics", "min_directX"]
        # possible_search_args += ["rec_directX", "min_reviews", "max_reviews"]
        possible_search_args += ["min_reviews", "max_reviews"]
        search_string = ""
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            for arg in possible_search_args:
                if input_dict[arg]:
                    if arg == "min_price":
                        search_string += "purchase_price <= " + input_dict[arg] + " OR after_discount <= " + \
                         input_dict[arg] + "IF after_discount > 0 OR "
                    elif arg == "max_price":
                        search_string += "purchase_price >= " + input_dict[arg] + " OR after_discount >= " + \
                                         input_dict[arg] + "IF after_discount > 0 OR "
                    elif arg == "min_discount":
                        search_string += "discount >= " + input_dict[arg] + " AND "
                    elif arg == "max_discount":
                        search_string += "discount <= " + input_dict[arg] + " AND "
                    elif arg == "min_statics":
                        search_string += "static >= " + input_dict[arg] + " AND "
                    elif arg == "max_statics":
                        search_string += "static <= " + input_dict[arg] + " AND "
                    elif arg == "min_release_date":
                        search_string += "release_date >= " + input_dict[arg] + " AND "
                    elif arg == "max_release_date":
                        search_string += "release_date <= " + input_dict[arg] + " AND "
                    elif arg == "min_reviews":
                        search_string += "reviews >= " + input_dict[arg] + " AND "
                    elif arg == "max_reviews":
                        search_string += "reviews <= " + input_dict[arg] + " AND "
                    elif arg.split("_")[0] == "min":
                        search_string += arg + " <= " + input_dict[arg] + " AND "
                    elif arg.split("_")[0] == "rec":
                        search_string += arg + " >= " + input_dict[arg] + " AND "
                    else:
                        search_string += arg + " = " + input_dict[arg] + " AND "
            if search_string.split(" ")[-2] == "AND":
                search_string = search_string[:len(search_string) - 5]
            if (input_dict["word"] or input_dict["overall"]) and (input_dict["word"] or input_dict["genre"]) and \
                    (input_dict["overall"] or input_dict["genre"]):
                for arg in static_possible_search_args:
                    if arg:
                        like_string = "LIKE %s', (unicode(u'%' " + input_dict[arg] + "u'%')"
                        search_string += "title " + like_string + " OR "
                        search_string += "description " + like_string + " OR "
                        search_string += "user_tags " + like_string + " OR "
                        search_string += "details " + like_string + " OR "
            if search_string.split(" ")[-2] == "Or":
                search_string = search_string[:len(search_string) - 5]
        # cursor.execute("SELECT games.title,games.url,games.release_date,games.details,games.description,games.id,"
        # "summary.image FROM games WHERE " + search_string + "INNER JOIN summary ON summary.id = games.summary_id")
        cursor.execute("SELECT games.title,games.url,games.release_date,games.details,games.description,games.id FROM"
                       " games WHERE " + search_string)
        result = cursor.fetchall()
        print result
        return result

    except Exception as e:
        print e
        return 0


def get_post(identifier):
    """
    | This function get an argument that is game id, game title or game url and returns game info in a tuple.
    | If identifier is empty or None returns False and if any exception thrown returns -1
    :param identifier: str
    :return: bool|tuple|int
    """
    try:
        if not identifier:
            return False
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("SELECT * FROM games WHERE id = %s OR title = %s OR url = %s",
                           (identifier, identifier, identifier))
            return cursor.fetchone()
    except Exception as e:
        print e
        return 0


def send_query(query, Tuple=None):
    try:
        connection_obj = MySql.connection()
        cursor = connection_obj.cursor()
        if Tuple is None:
            cursor.execute(query)
        else:
            cursor.execute(query, Tuple)
        if query.split(' ')[0] in ['SELECT', 'COUNT']:
            return cursor.fetchall()
        connection_obj.commit()
    except m.Error as e:
        print e
        return False


def get_res(query, Tuple=None):
    res = send_query(query, Tuple)
    if res:
        return res
    return tuple()


def get_summary(page_number):
    """
    | This function gets page number and returns 10 games with page_number offset in a tuple of tuples.
    | If any exception thrown returns -1
    :param page_number:str
    :return: tuple|int
    """
    try:
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("SELECT * FROM summary ORDER BY id DESC LIMIT 10 OFFSET " + page_number)
            return cursor.fetchall()
    except Exception as e:
        print e
        return 0


def add_cpu(title_list):
    """
    | This function adds cpu title to the table if not exists
    :param title_list:list
    :return:bool|int
    """
    try:
        if type(title_list) == list:
            for title in title_list:
                connection_obj = MySql.connection()
                with connection_obj:
                    cursor = connection_obj.cursor()
                    cursor.execute("INSERT INTO cpu(title) VALUES(%s)" + title)
                    connection_obj.commit()
            return True
    except Exception as e:
        print e
        return 0


def add_gpu(title_list):
    """
    | This function adds cpu title to the table if not exists
    :param title_list: list
    :return: bool
    """
    try:
        if type(title_list) == list:
            for title in title_list:
                connection_obj = MySql.connection()
                with connection_obj:
                    cursor = connection_obj.cursor()
                    cursor.execute("INSERT INTO gpu(title) VALUES(%s)" + title)
                    connection_obj.commit()
            return True
    except Exception as e:
        print e
        return 0


def get_cpu(title):
    """
    | This function returns all cpus with title included title param as a tuple of tuples
    :param title: str
    :return: tuple
    """
    try:
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("SELECT * FROM cpu WHERE title LIKE CONVERT(%s USING utf8) ",
                           (unicode(u'%' + title + u'%'),))
            return cursor.fetchall()
    except Exception as e:
        print e
        return 0


def get_gpu(title):
    """
    | This function returns all gpus with title included title param as a tuple of tuples
    :param title: str
    :return: tuple
    """
    try:
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cursor.execute("SELECT * FROM gpu WHERE title LIKE CONVERT(%s USING utf8) ",
                           (unicode(u'%' + title + u'%'),))
            return cursor.fetchall()
    except Exception as e:
        print e
        return 0


def create_s():
    create_game_table()
    create_summary_table()
    create_users_table()
    create_cpu_table()
    create_gpu_table()


