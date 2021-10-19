#!/usr/bin/env python
import random
import requests
import json
from collections import deque

import matplotlib.pyplot as plt  # $ pip install matplotlib
import matplotlib.animation as animation

npoints = 30
x = deque([0], maxlen=npoints)
y = deque([0], maxlen=npoints)
fig, ax = plt.subplots()
[line] = ax.step(x, y)


def update(dy):
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
    data = requests.post(url=url, data=json.dumps(payload))
    print(data.json()['data']['data'][0]['amount'])
    x.append(data.json()['data']['data'][0]['amount'])  # update data
    y.append(y[-1] + dy)

    line.set_xdata(x)  # update plot data
    line.set_ydata(y)

    ax.relim()  # update axes limits
    ax.autoscale_view(True, True, True)
    return line, ax


def data_gen():
    while True:
        yield 1 if random.random() < 0.5 else -1


ani = animation.FuncAnimation(fig, update, data_gen)
plt.show()