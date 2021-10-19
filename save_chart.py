# import matplotlib.pyplot as plt
# import numpy as np
#
# # Data for plotting
# t = np.arange(0.0, 2.0, 0.01)
# s = 1 + np.sin(2 * np.pi * t)
#
# fig, ax = plt.subplots()
# ax.plot(t, s)
#
# ax.set(xlabel='time (s)', ylabel='voltage (mV)',
#        title='About as simple as it gets, folks')
# ax.grid()
#
# fig.savefig("test.png")
# plt.show()

import matplotlib.pyplot as plt
import sqlite3
import time
from datetime import datetime
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)


def get_data_from_db(db_name, list):
    try:
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM {0};".format(list))
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


def save_chart(period):
    if period == 'all':
        index_ = 0
    elif period == 'day':
        null_time = int(time.mktime(datetime(year=datetime.now().year,
                                             month=datetime.now().month,
                                             day=datetime.now().day,
                                             hour=0,
                                             minute=0,
                                             second=0).timetuple()))
    elif period == 'hour':
        null_time = int(time.mktime(datetime(year=datetime.now().year,
                                             month=datetime.now().month,
                                             day=datetime.now().day,
                                             hour=datetime.now().hour - 1,
                                             minute=datetime.now().minute,
                                             second=datetime.now().second).timetuple()))
    db = get_data_from_db('data_binance.db', list='Metamon')
    formatter = DateFormatter('%H:%M:%S')
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("A test graph")
    price_list = []
    time_list = []
    for data in db:
        price_list.append(data[0])
        time_list.append(datetime.fromtimestamp(data[1]))
    counter = 0
    while counter < 6 and period != 'all':
        try:
            index_ = time_list.index(datetime.fromtimestamp(null_time))
            break
        except ValueError:
            null_time += 1
            counter += 1
            print(counter)
            pass
    fig, ax = plt.subplots(figsize=(20, 15))
    ax.plot(time_list[index_:], price_list[index_:])

    ax.xaxis.set_major_formatter(formatter)
    ax.grid()
    plt.savefig("test.png")
    # plt.show()

if __name__ == '__main__':
    save_chart('day')

