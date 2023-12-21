import time
import logging
import scipy
from scipy.stats import pearsonr
import numpy as np
from binance.lib.utils import config_logging
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.error import ClientError


def correlation(intercept, price, oi, candleamount):
    price1 = []
    oi1 = []
    for i in range(0, intercept):
        price1.append(price[i])
        oi1.append(oi[candleamount-i-1])
        print(price[i])
        print(oi[candleamount-i-1])
    correl = pearsonr(price1, oi1)
    return correl


def intercept_candle(price, candlelookback, candlenum, candleamount, price_open):
    price1 = price
    price1.reverse()
    price2 = price_open
    price2.reverse()
    for i in range(0, candleamount-candlenum):
        ma = ma_close(price, candlenum-i, candlenum)
        print(ma)
        if price2[i] < ma < price1[i] or price2[i] > ma > price1[i]:
            index = i
            return index, price2[index], price1[index], ma


def ma_close(price, candlelookback, candlenum):
    price1 = []
    price2 = price
    price2.reverse()
    if candlenum <= 100-candlelookback:
        for i in range(candlelookback, candlelookback+candlenum):
            price1.append(price2[i])
        ma = np.mean(price1)
        price2.reverse()
        return ma


def lastprice(symbol):
    my_client = UMFutures()
    mark_price = my_client.mark_price(symbol)
    return mark_price['markPrice']


def oi_analysis(symbol, timeframe, candleamount, lowerlimit, upperlimit):
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

    c = pearsonr(price, oi)
    ma = ma_close(price,0,50)
    intercept = intercept_candle(price, 0, 50, 100, price_open)
    c_last_trend = correlation(intercept[0]+2, price, oi, 100)

    return oi, price, c, ma, intercept, c_last_trend


print(oi_analysis('UNIUSDT', '5m', 100, 5, 5))
