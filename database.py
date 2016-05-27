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
        if MySql.connection_obj is None:
            instance = MySql()
            MySql.connection_obj = instance._connection
        return MySql.connection_obj

    def __init__(self):
        try:
            self._connection = m.Connection(_DBHOST, _DBUSER, _DBPASS, _DBNAME, use_unicode=True)
            self._connection.set_character_set('utf8')
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
                           "description VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci,"
                           "user_tags VARCHAR(255),statics VARCHAR(255),purchase_price FLOAT ,"
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
    # try:
    if kwargs['title'] == "code1":
        return False
    connection_obj = MySql.connection()
    with connection_obj:
        cursor = connection_obj.cursor()
        cols = ["title", "url", "overall", "description", "user_tags", "statics", "purchase_price", "release_date"]
        cols += ["discount", "min_os", "min_processor", "min_memory", "min_graphics", "min_directx", "min_storage"]
        cols += ["min_notes", "details", "rec_directx", "rec_storage", "rec_notes", "rec_os", "rec_processor"]
        cols += ["after_discount", "rec_memory", "rec_graphics", "original_price", "reviews"]
        kwargs_keys = tuple(kwargs.keys())
        for col_name in cols:
            if col_name not in kwargs_keys:
                kwargs.update({col_name: ""})
        query_tuple = tuple()
        for col_name in cols:
            if col_name not in kwargs_keys:
                query_tuple += ("",)
                continue
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
        for key in cols:
            into_string += key + ","
        into_string = into_string[:len(into_string) - 1]
        into_string = into_string.replace("statistics", "statics")
        cursor.execute(
            "INSERT INTO games(" + into_string + ") VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)", query_tuple)
        connection_obj.commit()
        return True
    # except Exception as e:
    #     print(e)
    #     print kwargs
    #     print "_____________________"
    #     return -1


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
            return cursor.fetchone()
    except Exception as e:
        print(e)
        return -1


def add_user(username, email, password):
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
            if not check_user_with_email(email) and not check_user_with_username(username):
                return False
            cursor.execute("INSERT INTO users(user_name,password,email) VALUES(%s,%s,%s) IF user_name != %s AND"
                           " email != %s", (username, password, email, username, email))
            connection_obj.commit()
            return True
    except Exception as e:
        print(e)
        return -1


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
            return cursor.fetchone()
    except Exception as e:
        print(e)
        return -1


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
            return cursor.fetchone()
    except Exception as e:
        print(e)
        return -1

create_game_table()
create_users_table()