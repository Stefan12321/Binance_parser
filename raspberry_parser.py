import requests
import sqlite3
import json
import time
import datetime


def get_data(serial):
    headers = {"content-type": "application/json",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
    url = 'https://www.binance.com/bapi/nft/v1/public/nft/market-mystery/mystery-list'
    payload = {
        "page": 1,
        "params": {
            "keyword": "",
            "nftType": "2",
            "orderBy": "amount_sort",
            "orderType": "1",
            "serialNo": [serial],
            "tradeType": "0",
        },
        "size": 16
    }

    # data = requests.get(url=url, headers=headers)
    data = requests.post(url=url, data=json.dumps(payload), headers=headers)
    for i in range(len(data.json()['data']['data'])):
        price = float(data.json()['data']['data'][i]['amount'])
        currency = data.json()['data']['data'][i]['currency']
        if currency == "BUSD":
            break
    print(price)
    return price


def add_data(price, list, db_name):
    try:
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()
        sqlite_insert_with_param = """INSERT INTO '{0}'
                                         ('price', 'time') 
                                         VALUES (?, ?);""".format(list)
        time_ = int(time.mktime(datetime.datetime.now().timetuple()))
        data_tuple = (price, time_)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")


if __name__ == '__main__':
    while True:
        price = get_data("143953674287424512")
        add_data(price, list="Metamon", db_name='data_binance.db')
        price = get_data("144710208067960832")
        add_data(price, list="DeHero", db_name='data_binance.db')
        time.sleep(5)