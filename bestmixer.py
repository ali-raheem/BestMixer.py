#!/usr/bin/python3

# BestMixer Python3 API library
# GPLv3
# Copyright Ali Raheem 2018

import json
import requests
import base64

class BestMixer:
    def __init__(self, api_key, tor = None, proxy = 'socks5://localhost:9150', use_proxy = False):
        self.api_key = api_key
        self.url = 'http://bestmixer7o57mba.onion' if tor else 'https://bestmixer.io'
        self.url += '/api/ext'
        self.proxies = None
        if tor or use_proxy:
            self.proxies = {'http': proxy}
        else:
            self.proxies = {}
    def request(self, action, data):
        data['api_key'] = self.api_key
        data = json.dumps(data)
        headers = {'Accept': 'application/json',
                   'Content-Type':'application/json'}
        r = requests.post(self.url + action, data = data, headers = headers, proxies = self.proxies)
        return json.loads(r.text)
    def getOrderInfo(self, id):
        data = {'order_id': id}
        return self.request('/order/info', data)
    def getCodeInfo(self, id):
        data = {'bm_code':  id}
        return self.request('/code/info', data)
    def getFeeInfo(self):
        return self.request('/fee/info', {})
    def orderCreate(self, coin, fee, output, bm_code = None):
        data = {}
        data['coin'] = coin
# currently accepted ltc, btc, bch soon eth no validation incase
        data['fee'] = fee
# total percent must add up to 100
        total_percent = 0
        for out in output:
            total_percent += out['percent']
        if(total_percent != 100):
            raise Exception('Outputs in Order must total 100%')

        data['output'] = output
        if(bm_code):
            data['bm_code'] = bm_code
        return self.request('/order/create', data)
    @staticmethod
    def output(address, percent = 100, delay = 0):
        return {'address': address, 'percent': percent, 'delay': delay}

if __name__ == '__main__':
    bm = BestMixer('replace_with_API_key')
    # Example two address LTC mix with 30/70 split half hour and 2hr delays, 0.5612% fee
    order = bm.orderCreate('ltc', 0.5612,
    [
        BestMixer.output('Lxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 30, 30),
        BestMixer.output('Lxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 70, 120)
    ]
    )
    print(base64.b64decode(order['data']['letter_of_guarantee']).decode())
