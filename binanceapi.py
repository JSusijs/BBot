import time
import logging
from binance.lib.utils import config_logging
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.error import ClientError

config_logging(logging, logging.DEBUG)

info = ""


def message_handler(_, message):
    global info
    info = message


um_futures_client = UMFutures(key='8GaWaBZ7vYQNDUDE7tcYMMsjF7FwxyNgMC9OtZXDsdMnkQcPSoCF0AeyWwq4vPEz', secret='6ZWRExVLogY5xORd4sCXLtddFKdOUqlDbm2bv3BiFvPBVjEjgp9Pei5I3htsY3TP')
my_client = UMFuturesWebsocketClient(on_message=message_handler, is_combined=True)
my_client.agg_trade(symbol="GALAUSDT", id=1)
#logging.info(um_futures_client.account(recvWindow=6000))

time.sleep(1)

for i in range(0, 9):
    time.sleep(1)
    print(info)

time.sleep(1)

my_client.agg_trade(symbol="GALAUSDT", id=1, action=UMFuturesWebsocketClient.ACTION_UNSUBSCRIBE)
time.sleep(1)

listen_key = um_futures_client.new_listen_key()['listenKey']
print(listen_key)

try:
    response = um_futures_client.get_account_trades(symbol="GALAUSDT", recvWindow=6000)
    print(response)
except ClientError as error:
    logging.error(
        "Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        )
    )

time.sleep(1)
logging.info(um_futures_client.close_listen_key(listen_key))
my_client.stop()
