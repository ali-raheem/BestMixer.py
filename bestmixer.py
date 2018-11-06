#!/usr/bin/python3

"""This module handles the low level API cals to BestMixer.io
BestMixer Python3 API library
Copyright Ali Raheem 2018
GPLv3"""

import json
import base64
import requests

class BestMixer:
    """This class handles calls with a given api_key to BestMixer.io"""
    def __init__(self, api_key, tor=None, proxy='socks5://localhost:9150', use_proxy=False):
        self.api_key = api_key
        self.url = 'http://bestmixer7o57mba.onion' if tor else 'https://bestmixer.io'
        self.url += '/api/ext'
        self.proxies = None
        if tor or use_proxy:
            self.proxies = {'http': proxy}
        else:
            self.proxies = {}
    def request(self, action, data):
        """Generic take API path and data and make request"""
        data['api_key'] = self.api_key
        data = json.dumps(data)
        headers = {'Accept': 'application/json',
                   'Content-Type':'application/json'}
        res = requests.post(self.url + action, data=data, headers=headers, proxies=self.proxies)
        return json.loads(res.text)
    def get_order_info(self, oid):
        """Get information about a mix in process using the order_id"""
        data = {'order_id': oid}
        return self.request('/order/info', data)
    def get_code_info(self, oid):
        """Get information about your BM code discount using your bm_code"""
        data = {'bm_code':  oid}
        return self.request('/code/info', data)
    def get_fee_info(self):
        """Get minimum miner fee per output address"""
        return self.request('/fee/info', {})
    def order_create(self, coin, fee, output, bm_code=None):
        """Create an order coin with a fee and an output array"""
        data = {}
        data['coin'] = coin
# currently accepted ltc, btc, bch soon eth no validation incase
        data['fee'] = fee
# total percent must add up to 100
        total_percent = 0
        for out in output:
            total_percent += out['percent']
        if total_percent != 100:
            raise Exception('Outputs in Order must total 100%')

        data['output'] = output
        if bm_code:
            data['bm_code'] = bm_code
        return self.request('/order/create', data)
    @staticmethod
    def output(address, percent=100, delay=0):
        """Return an output dict for use with createOrder"""
        return {'address': address, 'percent': percent, 'delay': delay}

if __name__ == '__main__':
    BM = BestMixer('replace_with_API_key')
    # Example two address LTC mix with 30/70 split half hour and 2hr delays, 0.5612% fee
    order = BM.order_create('ltc', 0.5612,
    [BestMixer.output('Lxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 30, 30),
     BestMixer.output('Lxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 70, 120)])
    print(base64.b64decode(order['data']['letter_of_guarantee']).decode())
