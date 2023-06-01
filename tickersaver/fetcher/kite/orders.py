import requests, os
from tickersaver.utils.log import logger_instance
from kiteconnect import KiteConnect
from http import HTTPStatus

logger = logger_instance


class Order(object):
    def __init__(self, config):
        self.config = config
        self.initiate_buffer = 0
        self.stoploss_buffer = 0
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'enctoken {}'.format(os.getenv("ZWSSTOKEN") or self.config.get("zwsstoken")),
            'Accept-Language': 'en-us',
            'Host': 'kite.zerodha.com',
            'Origin': 'https://kite.zerodha.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
            'Referer': 'https://kite.zerodha.com/positions',
            'X-Kite-Version': '3.0.4',
            'X-Kite-Userid': os.getenv("ZUSERNAME") or self.config.get("zusername")
        }

    def place_order(self, trading_symbol, transaction_type=KiteConnect.TRANSACTION_TYPE_BUY, quantity=0,
                    order_type=KiteConnect.ORDER_TYPE_MARKET, trigger_price=0,
                    exchange=KiteConnect.EXCHANGE_NSE, product=KiteConnect.PRODUCT_MIS):
        data = {
            'variety': 'regular',
            'exchange': exchange,
            'tradingsymbol': trading_symbol,
            'transaction_type': transaction_type,
            'order_type': order_type,
            'quantity': quantity,
            'price': '0',
            'product': product,
            'validity': 'DAY',
            'disclosed_quantity': '0',
            'trigger_price': trigger_price,
            'squareoff': '0',
            'stoploss': '0',
            'trailing_stoploss': '0',
            'user_id': os.getenv("ZUSERNAME") or self.config.get("zusername")
        }
        logger.info(
            "Firing {} Position  for {} for {} quantity ".format(
                transaction_type,
                trading_symbol,
                quantity))
        response = requests.post('https://kite.zerodha.com/oms/orders/regular', headers=self.headers, cookies={},
                                 data=data)
        logger.debug("Position attempted Status:{}, Response:{}".format(response.status_code, response.json()))
        return response

    def get_positions(self):
        logger.info("Getting position details")
        url = 'https://kite.zerodha.com/oms/portfolio/positions'
        response = requests.get(url, headers=self.headers)
        logger.debug("Position Details  Status:{}, Response:{}".format(response.status_code, response.json()))
        if response.status_code == HTTPStatus.OK:
            return response

    def truncate_file(self, filename):
        with open(filename, 'a') as fp:
            logger.info("Truncating the file - {} to 0 bytes".format(filename))
            fp.truncate(0)

    def write_positions_tofile(self, pos, filename, temp_write_seconds=-1):
        import csv, copy, time
        existing_position_list = []
        existing_position_list_file = []

        with open(filename, 'r') as fp:
            csvreader = csv.reader(fp)
            existing_position_list_file = list(csvreader)
            existing_position_list = copy.deepcopy(existing_position_list_file)
        for i in pos['data']['net']:
            tmp_list = [str(i['instrument_token']), i['tradingsymbol']]
            if tmp_list not in existing_position_list_file:
                existing_position_list_file.append(tmp_list)

        with open(filename, 'w') as fp:
            csvwriter = csv.writer(fp)
            csvwriter.writerows(existing_position_list_file)

        # this logic is to write instuments temporarily in the csv file uesd by ticker to fetch ltp
        if temp_write_seconds > 0:
            logger.info("Sleeping for {} seconds for subscribe to complete of all strikes".format(temp_write_seconds))
            time.sleep(temp_write_seconds)
            with open(filename, 'a') as fp1:
                logger.info("Truncating the file - {} to 0 bytes".format(filename))
                fp1.truncate(0)
            with open(filename, 'w') as fp2:
                csvwriter = csv.writer(fp2)
                csvwriter.writerows(existing_position_list)

    def get_orders(self):
        response = requests.get('https://kite.zerodha.com/oms/orders', headers=self.headers)
        logger.debug("Order Details  Status:{}, Response:{}".format(response.status_code, response.json()))
        if response.status_code == 200:
            return response

    def square_off_positions_level(self, open_buy_positions, open_sell_positions, level,
                                   exchange=KiteConnect.EXCHANGE_NFO):
        # squares of Sell first followed by Buy due to margin issue
        for pos in open_sell_positions:
            logger.info("Closing all open SELL positions as level of {} is hit".format(level))
            tradingsymbol = pos['tradingsymbol']
            transaction_type = KiteConnect.TRANSACTION_TYPE_BUY
            quantity = abs(pos['quantity'])
            product = pos['product']
            self.place_order(tradingsymbol, transaction_type=transaction_type, quantity=quantity,
                             exchange=exchange, product=product)

        for pos in open_buy_positions:
            logger.info("Closing all open BUY positions as level of {} is hit".format(level))
            tradingsymbol = pos['tradingsymbol']
            transaction_type = KiteConnect.TRANSACTION_TYPE_SELL
            quantity = abs(pos['quantity'])
            product = pos['product']
            self.place_order(tradingsymbol, transaction_type=transaction_type, quantity=quantity,
                             exchange=exchange, product=product)
