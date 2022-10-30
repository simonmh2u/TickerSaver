import requests
from tickersaver.utils.log import logger_instance

logger = logger_instance


class Order(object):
    def __init__(self, config):
        self.config = config
        self.initiate_buffer = 0
        self.stoploss_buffer = 0
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'enctoken {}'.format(self.config.get("wsstoken")),
            'Accept-Language': 'en-us',
            'Host': 'kite.zerodha.com',
            'Origin': 'https://kite.zerodha.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
            'Referer': 'https://kite.zerodha.com/positions',
            'X-Kite-Version': '3.0.4',
            'X-Kite-Userid': self.config.get("username"),
        }

    def get_positions(self):
        logger.info("Getting position details")
        url = 'https://kite.zerodha.com/oms/portfolio/positions'
        response = requests.get(url, headers=self.headers)
        logger.debug("Position Details  Status:{}, Response:{}".format(response.status_code, response.json()))
        if response.status_code == 200:
            return response

    def write_positions_tofile(self, pos, filename):
        import csv
        existing_position_list = []
        existing_position_list_file = []

        with open(filename, 'r') as fp:
            csvreader = csv.reader(fp)
            existing_position_list_file = list(csvreader)
        for i in pos['data']['net']:
            tmp_list = [str(i['instrument_token']), i['tradingsymbol']]
            if tmp_list not in existing_position_list_file:
                existing_position_list_file.append(tmp_list)

        with open(filename, 'w') as fp:
            csvwriter = csv.writer(fp)
            csvwriter.writerows(existing_position_list_file)
