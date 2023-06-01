from kiteconnect import KiteTicker
from tickersaver.utils.log import logger_instance
from urllib.parse import quote_plus
from tickersaver.cache.sqllite_cache import Sqllite
from tickersaver.fetcher.kite.orders import Order
import os, csv, datetime, json, argparse

logger = logger_instance


class KT(KiteTicker):

    def init_db(self, config):
        sql = Sqllite()
        sql.init_ltp_db(config.get("dbpath"))
        self.sql = sql

    def _create_connection(self, url, **kwargs):
        wsstoken = os.getenv("zwsstoken") or self.config.get("wsstoken")
        wsstoken = quote_plus(wsstoken)
        username = os.getenv("ZUSERNAME") or self.config.get("username")
        url = 'wss://ws.zerodha.com/?api_key=kitefront&user_id={}&enctoken={}&uid=1&user-agent=kite3-web&version=2.9.1'.format(
            username, wsstoken)
        super(KT, self)._create_connection(url, **kwargs)


def on_ticks(ws, ticks):
    config = ws.config
    filename = config.get("tickerfile_path")

    # exit on 15:24
    dt = datetime.datetime.now()
    # if dt.time() >= datetime.time(15, 24, 0):
    #     logger.info("Exiting as Indian MIS market hours have closed")
    #     ws.close(code=4000, reason="market_close_time")

    # If ticker file has changed then refresh the instrument list from the ticker file
    dynamic_config_mod_time = os.stat(filename).st_mtime
    if hasattr(ws, 'file_mod_time') and dynamic_config_mod_time > ws.file_mod_time:
        logger.info("File Changed - resubscribing")
        with open(filename, 'r') as fp:
            csvreader = csv.reader(fp)
            existing_position_list_file = list(csvreader)
            newsublist = [int(x[0]) for x in existing_position_list_file]
        logger.info("File Changed Unsubscribing {}".format(ws.instrument_list))
        ws.unsubscribe(ws.instrument_list)
        sub_list = ws.always_on_instrument_list + newsublist
        logger.info("File Changed Subscribing {}".format(sub_list))
        ws.subscribe(sub_list)
        ws.instrument_list = sub_list
        ws.file_mod_time = dynamic_config_mod_time

    # touch the below file to refresh the sub list dynamically
    if os.path.exists(config.get("instrument_touch_path")) and config.get("subscribe_current_positions"):
        pos = ws.order.get_positions().json()
        ws.order.write_positions_tofile(pos, filename)
        os.remove(config.get("instrument_touch_path"))
    logger.debug("Sample Data: {}".format(ticks))
    logger.info("Tick received")

    for i in ticks:
        key = str(i['instrument_token'])
        ws.sql.set_ltp(key, i['last_price'])


def on_close(ws, code, reason):
    logger.info("Close received with the code, reason - {}, {}".format(code, reason))
    if code == 4000:
        logger.info("Exiting as market hours have ended, in on_close - {}".format(code))
        ws.stop()


def on_connect(ws, response):  # noqa
    config = ws.config
    filename = config.get("tickerfile_path")

    if not os.path.exists(filename):
        with open(filename, 'w') as fp:
            logger.info("Creating empty file - {}".format(filename))
    # Callback on successful connect.
    if config.get("subscribe_current_positions"):
        pos = ws.order.get_positions().json()
        ws.order.write_positions_tofile(pos, filename)
    dynamic_config_mod_time = os.stat(filename).st_mtime
    with open(filename, 'r') as fp:
        csvreader = csv.reader(fp)
        existing_position_list_file = list(csvreader)
        newsublist = [int(x[0]) for x in existing_position_list_file]
    ws.file_mod_time = dynamic_config_mod_time
    sub_list = ws.always_on_instrument_list + newsublist
    ws.instrument_list = sub_list
    logger.info("Subscribe list : {}".format(sub_list))
    ws.subscribe(sub_list)
    ws.set_mode(ws.MODE_LTP, sub_list)


def start_stream(config):
    order = Order(config)
    kws = KT("", "")
    kws.init_db(config)
    kws.config = config
    # Assign the callbacks.
    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close
    kws.instrument_list = []
    kws.always_on_instrument_list = config.get("default_instruments")
    kws.order = order
    kws.connect()


def main():
    parser = argparse.ArgumentParser(description='Zerodha Ticker Saver')
    parser.add_argument('-c', '--config', help='Configuration file path', required=True)
    args = parser.parse_args()
    config_filepath = args.config
    with open(config_filepath) as fp:
        config = fp.read()
        config = json.loads(config)
    username = os.getenv("ZUSERNAME")
    wsstoken = os.getenv("ZWSSTOKEN")

    # If not set in env variable then check if value is set in the config file
    if not username:
        username = config.get("zusername", "")
    if not wsstoken:
        wsstoken = config.get("zwsstoken", "")

    if not username or not wsstoken:
        logger.error("Auth information not set in environment variable or config, exiting!!")
        exit(5)

    config["username"] = username
    config["wsstoken"] = wsstoken
    start_stream(config)


if __name__ == '__main__':
    main()
