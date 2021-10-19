import time
import datetime
import sqlite3
from PyQt5 import Qt, QtCore
from utils import TimeAxisItem, timestamp
import pyqtgraph as pg
import numpy as np
import requests
import json
import threading


class Window(Qt.QWidget):

    def __init__(self):
        super().__init__()

        layout = Qt.QVBoxLayout(self)

        self.view = view = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')}, )
        pen = pg.mkPen(color=(255, 0, 0))
        self.view.setLabel('left', "<span style=\"color:red;font-size:20px\">Price (BUSD)</span>")
        self.view.setLabel('bottom', "<span style=\"color:red;font-size:20px\">Time</span>")
        self.view.showGrid(x=True, y=True)
        self.view.setBackground('w')
        self.curve = view.plot(name="Line",  pen=pen, symbol='o', symbolSize=8, symbolBrush=('b'))


        self.btn = Qt.QPushButton("Random plot")
        self.btn.clicked.connect(self.start_thread)

        layout.addWidget(Qt.QLabel("DeHero"))
        layout.addWidget(self.view)
        layout.addWidget(self.btn)
        self.start_thread()

    def random_plot(self):
        # price = self.get_data()
        # self.add_data(price)
        # array = [price]
        # array2 = [timestamp()]
        array = []
        array2 = []
        db = self.get_data_from_db()
        for data in db:
            array.append(data[0])
            array2.append(data[1])
        time.sleep(5)
        while True:
            price = self.get_data()

            self.add_data(price)
            array.append(price)
            array2.append(timestamp())
            self.curve.setData(array2, array)
            # self.view.addItem()
            time.sleep(5)

    def start_thread(self):
        t = threading.Thread(target=self.random_plot)
        t.start()

    def get_data_from_db(self):
        try:
            sqliteConnection = sqlite3.connect('data_de.db')
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

    def get_data(self):
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
                "serialNo": ["144710208067960832"],
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

    def add_data(self, price):
        try:
            sqliteConnection = sqlite3.connect('data.db')
            cursor = sqliteConnection.cursor()
            sqlite_insert_with_param = """INSERT INTO 'price_data'
                                             ('price', 'time') 
                                             VALUES (?, ?);"""
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


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = Window()
    w.show()
    app.exec()