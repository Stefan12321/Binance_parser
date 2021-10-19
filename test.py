import datetime
import sqlite3
import time


def create_table(price, time_):
    try:
        sqliteConnection = sqlite3.connect('data_binance.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_create_table_query = '''CREATE TABLE Metamon (
                                               price REAL,
                                               time timestamp);'''

        cursor = sqliteConnection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_create_table_query = '''CREATE TABLE DeHero (
                                                       price REAL,
                                                       time timestamp);'''
        cursor.execute(sqlite_create_table_query)
        # sqlite_insert_with_param = """INSERT INTO 'price_data'
        #                          ('price', 'time')
        #                          VALUES (?, ?);"""
        # data_tuple = (price, time_)
        # cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")


def get_data():
    try:
        sqliteConnection = sqlite3.connect('test.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM price_data;")
        all_results = cursor.fetchall()
        return all_results
        # print(all_results)
        # print(type(all_results[0][1]))
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")


def add_data(price):
    try:
        sqliteConnection = sqlite3.connect('test.db')
        cursor = sqliteConnection.cursor()
        sqlite_insert_with_param = """INSERT INTO 'price_data'
                                         ('price', 'time') 
                                         VALUES (?, ?);"""
        time_ = datetime.datetime.now()
        data_tuple = (price, time_)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")


def addDeveloper(id, name, joiningDate):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_create_table_query = '''CREATE TABLE new_developers (
                                       id INTEGER PRIMARY KEY,
                                       name TEXT NOT NULL,
                                       joiningDate timestamp);'''

        cursor = sqliteConnection.cursor()
        cursor.execute(sqlite_create_table_query)

        # insert developer detail
        sqlite_insert_with_param = """INSERT INTO 'new_developers'
                          ('id', 'name', 'joiningDate') 
                          VALUES (?, ?, ?);"""

        data_tuple = (id, name, joiningDate)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Developer added successfully \n")

        # get developer detail
        sqlite_select_query = """SELECT name, joiningDate from new_developers where id = ?"""
        cursor.execute(sqlite_select_query, (1,))
        records = cursor.fetchall()

        for row in records:
            developer = row[0]
            joining_Date = row[1]
            print(developer, " joined on", joiningDate)
            print("joining date type is", type(joining_Date))

        cursor.close()

    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

# addDeveloper(2, 'Vil', datetime.datetime.now())


if __name__ == '__main__':
    create_table(31, int(time.mktime(datetime.datetime.now().timetuple())))
    # add_data(79.9)
    # get_data()
    # print(int(time.mktime(datetime.datetime.now().timetuple())))