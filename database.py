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
            self._connection = m.Connection(_DBHOST, _DBUSER, _DBPASS, _DBNAME)
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
                           "description VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci,"
                           "user_tags VARCHAR(255),overall VARCHAR(255),statics VARCHAR(255),"
                           "release_date DATE,original_price VARCHAR(255),discount VARCHAR(255),min_os VARCHAR(255),min_processor VARCHAR(255),"
                           "min_memory VARCHAR(255),min_graphics VARCHAR(255),min_directx VARCHAR(255),min_storage VARCHAR(255),min_notes VARCHAR(255)"
                           ",req_directx VARCHAR(255),req_storage VARCHAR(255),req_notes VARCHAR(255),req_os VARCHAR(255),req_processor VARCHAR(255),"
                           "req_memory VARCHAR(255),req_graphics VARCHAR(255))")
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
    try:
        connection_obj = MySql.connection()
        with connection_obj:
            cursor = connection_obj.cursor()
            cols = ["title", "url", "description", "user_tags", "overall", "statics", "release_date", "original_price", "discount"]
            cols += ["min_os", "min_processor", "min_memory", "min_graphics", "min_directx", "min_storage", "min_notes"]
            cols += ["rec_directx", "rec_storage", "rec_notes", "rec_os", "rec_processor", "rec_memory", "rec_graphics"]
            kwargs_keys = tuple(kwargs.keys())
            for col_name in cols:
                if col_name not in kwargs_keys:
                    kwargs.update({col_name: None})
            query_tuple = tuple()
            for col_name in kwargs_keys:
                query_tuple += (kwargs[col_name])
            into_string = ""
            for key in kwargs_keys:
                into_string += key
            cursor.execute(
                "INSERT INTO games(" + into_string + ") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", query_tuple)
            connection_obj.commit()
            return True
    except Exception as e:
        print(e)
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

create_game_table()