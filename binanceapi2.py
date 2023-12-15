import time
import logging
from scipy.stats import pearsonr
from binance.lib.utils import config_logging
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.error import ClientError


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

    for i in range(0, candleamount):
        oi.insert(i, float(oi_return[i]['sumOpenInterestValue']))
        price.insert(i, float(price_return[i][4]))

    c = pearsonr(price, oi)

    return oi, price, c


print(oi_analysis('UNIUSDT', '1h', 30, 5, 5))
