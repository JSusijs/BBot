import time
import logging
import scipy
from scipy.stats import pearsonr
import numpy as np
from binance.lib.utils import config_logging
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.error import ClientError


def correlation(price, oi, intercept):
    price_int = []
    oi_int = []
    for i in range(0, abs(intercept)):
        price_int.append(price[i])
        oi_int.append(oi[i])
    c = pearsonr(price_int,oi_int)
    return c


def data0(price, oi, price_open):
    price1 = []
    price_open1 = []
    oi1 = []
    price2 = price
    price2.reverse()
    price_open2 = price_open
    price_open2.reverse()
    oi2 = oi
    oi2.reverse()
    for i in range(0, len(price)):
        price1.append(price2[i])
        price_open1.append(price_open2[i])
        oi1.append(oi2[i])
    return price1, oi1, price_open1


def intercept_candle(price_close, price_open, ma):
    for i in range(0, len(price_close)-len(ma)):
        if price_close[i] > ma[i] > price_open[i]:
            index = i
            if index >= 2:
                return index
        elif price_close[i] < ma[i] < price_open[i]:
            index = -i
            if index <= -2:
                return index


def ma_close(price, candlelookback, candlenum):
    ma = []
    for i in range(0, candlenum-candlelookback):
        price_lookback = []
        for j in range(i, i+candlelookback):
            price_lookback.append(price[j])
        ma.append(np.mean(price_lookback))
    return ma


def lastprice(symbol):
    my_client = UMFutures()
    mark_price = my_client.mark_price(symbol)
    return mark_price['markPrice']


def price_range_relative(lowerlimit, upperlimit, last_price):
    mid_price = (lowerlimit + upperlimit) / 2
    c = (float(last_price)-mid_price)/(upperlimit-mid_price)
    return c


def oi_analysis(symbol, timeframe, candleamount, lowerlimit, upperlimit, candlelookback):
    my_client = UMFutures()
    oi_return = my_client.open_interest_hist(symbol, timeframe, **{"limit": candleamount})
    price_return = my_client.mark_price_klines(symbol, timeframe, **{"limit": candleamount+1})
    oi = []
    price = []
    price_open = []

    for i in range(0, candleamount):
        oi.insert(i, float(oi_return[i]['sumOpenInterestValue']))
        price.insert(i, float(price_return[i][4]))
        price_open.insert(i, float(price_return[i][1]))

    data = data0(price, oi, price_open)
    price_close_reverse = data[0]
    oi_close_reverse_adj = data[1]
    price_open_reverse = data[2]
    ma_data = ma_close(price_close_reverse, candlelookback, candleamount)
    intercept = intercept_candle(price_close_reverse, price_open_reverse, ma_data)
    coef = correlation(price_close_reverse, oi_close_reverse_adj, intercept)
    prr = price_range_relative(lowerlimit, upperlimit, lastprice(symbol))

    return intercept, coef, prr


print(oi_analysis('SUIUSDT', '15m', 150, 0.77, 0.92, 50))
