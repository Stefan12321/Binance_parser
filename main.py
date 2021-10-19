import time
from datetime import datetime
import sqlite3
from PyQt5 import Qt, QtCore, QtWidgets
from utils import TimeAxisItem, timestamp
import pyqtgraph as pg
import numpy as np
import requests
import json
import threading
import paramiko


class Window(Qt.QWidget):

    def __init__(self):
        super().__init__()

        layout = Qt.QVBoxLayout(self)

        self.view = view = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')}, )
        pen = pg.mkPen(color=(255, 0, 0))
        pen2 = pg.mkPen(color=(0, 255, 0))
        self.view.setLabel('left', "<span style=\"color:red;font-size:20px\">Price (BUSD)</span>")
        self.view.setLabel('bottom', "<span style=\"color:red;font-size:20px\">Time</span>")
        self.view.showGrid(x=True, y=True)
        self.view.setBackground('w')
        self.view.plot(name="Metamon", pen=pen, symbol='o', symbolSize=8,
                              symbolBrush=('b'))
        self.view.plot(name="DeHero", pen=pen2, symbol='o', symbolSize=8,
                       symbolBrush=('b'))
        self.view.addLegend()
        self.curve = view.plot(name="Metamon",  pen=pen, symbol='o', symbolSize=3, symbolBrush=('b'))
        self.curve2 = view.plot(name="DeHero",  pen=pen2, symbol='o', symbolSize=3, symbolBrush=('b'))


        # self.btn = Qt.QPushButton("Random plot")
        # self.btn.clicked.connect(self.start_thread)
        self.week = QtWidgets.QRadioButton()
        self.week.setObjectName("QRadioButton_week")
        self.week.setText("Week")
        self.week.setChecked(True)
        self.day = QtWidgets.QRadioButton()
        self.day.setObjectName("QRadioButton_day")
        self.day.setText("Day")
        self.hour = QtWidgets.QRadioButton()
        self.hour.setObjectName("QRadioButton_hour")
        self.hour.setText("Hour")

        layout.addWidget(Qt.QLabel("Some text"))
        layout.addWidget(self.view)
        layout.addWidget(self.week)
        layout.addWidget(self.day)
        layout.addWidget(self.hour)
        # layout.addWidget(self.btn)
        ip = '192.168.0.101'
        user = 'pi'
        pwd = 'raspberry'
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.ssh_client.load_system_host_keys()
        self.ssh_client.connect(ip, 22, user, pwd)
        self.sftp_client = self.ssh_client.open_sftp()

        self.start_thread()

    def random_plot(self):

        arraya = []
        arrayb = []
        db = self.get_data_from_db('data.db', list='price_data')
        for data in db:
            arraya.append(data[0])
            arrayb.append(data[1])
        time.sleep(5)
        while True:
            if self.week.isChecked():
                null_time = int(time.mktime(datetime(year=datetime.now().year,
                                                     month=datetime.now().month,
                                                     day=datetime.now().day,
                                                     hour=0,
                                                     minute=0,
                                                     second=0).timetuple()))
            elif self.day.isChecked():
                null_time = int(time.mktime(datetime(year=datetime.now().year,
                                                     month=datetime.now().month,
                                                     day=datetime.now().day,
                                                     hour=0,
                                                     minute=0,
                                                     second=0).timetuple()))
            elif self.hour.isChecked():
                null_time = int(time.mktime(datetime(year=datetime.now().year,
                                                     month=datetime.now().month,
                                                     day=datetime.now().day,
                                                     hour=datetime.now().hour - 1,
                                                     minute=datetime.now().minute,
                                                     second=datetime.now().second).timetuple()))
            self.get_data_from_sftp()
            # price = self.get_data()

            # self.add_data(price)
            # price_array.append(price)
            # time_array.append(timestamp())
            price_array = []
            time_array = []
            array3 = []
            array4 = []
            db = self.get_data_from_db('data_binance.db', list='Metamon')
            for data in db:
                price_array.append(data[0])
                time_array.append(data[1])

            for i in range(5):
                try:
                    index_ = time_array.index(null_time)
                    break
                except ValueError:
                    null_time += 1
                    pass
            self.curve.setData(time_array[index_:], price_array[index_:])
            db = self.get_data_from_db('data_binance.db', list='DeHero')
            for data in db:
                array3.append(data[0])
                array4.append(data[1])
            for i in range(5):
                try:
                    index_ = time_array.index(null_time)
                    break
                except ValueError:
                    null_time += 1
                    pass

            self.curve2.setData(array4[index_:], array3[index_:])
            # self.view.addItem()
            time.sleep(5)

    def start_thread(self):
        t = threading.Thread(target=self.random_plot)
        t.start()

    def get_data_from_db(self, db_name, list):
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

    def get_data_from_sftp(self):
        self.sftp_client.get("/home/pi/binance/data_binance.db",
                        "C:\\Users\\Stefan\\PycharmProjects\\binance_parser\\data_binance.db")

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
                "serialNo": ["143953674287424512"],
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
            time_ = int(time.mktime(datetime.now().timetuple()))
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