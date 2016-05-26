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
            cursor.execute("CREATE TABLE IF NOT EXISTS games(id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,title VARCHAR NOT NULL ,"
                           "url VARCHAR NOT NULL,description VARCHAR,user_tags VARCHAR,overall VARCHAR,statics VARCHAR,"
                           "release_date DATE,original_price VARCHAR,discount VARCHAR,min_os VARCHAR,min_processor VALUE,"
                           "min_memory VARCHAR,min_graphics VARCHAR,min_directx VARCHAR,min_storage VARCHAR,min_notes VARCHAR"
                           ",req_directx VARCHAR,req_storage VARCHAR,req_notes VARCHAR,req_os VARCHAR,req_processor VALUE,"
                           "req_memory VARCHAR,req_graphics VARCHAR)")
            connection_obj.commit()
    except Exception as e:
        print(e)


def add_game(title, url, **args):
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
        if title is None or url is None:
            return False
        with connection_obj:
            cursor = connection_obj.cursor()
            cols = ["description", "user_tags", "overall", "statics", "release_date", "original_price", "discount"]
            cols += ["min_os", "min_processor", "min_memory", "min_graphics", "min_directx", "min_storage", "min_notes"]
            cols += ["req_directx", "req_storage", "req_notes", "req_os", "req_processor", "req_memory", "req_graphics"]
            args_keys = tuple(args.keys())
            for col_name in cols:
                if col_name not in args_keys:
                    args.update({col_name: None})
            query_tuple = (title, url)
            for col_name in args_keys:
                query_tuple += (args[col_name])
            into_string = ""
            for key in args_keys:
                into_string += key
            cursor.execute(
                "INSERT INTO games("+ into_string + ") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", query_tuple)
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