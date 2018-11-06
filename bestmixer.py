#!/usr/bin/python3

# BestMixer Python3 API library
# GPLv3
# Copyright Ali Raheem 2018

import json
import requests

class BestMixer:
    def __init__(self, api_key, tor = None, tor_port = 9150):
        self.api_key = api_key
        self.url = 'http://bestmixer7o57mba.onion' if tor else 'https://bestmixer.io'
        self.url += '/api/ext'
        #9150 is port for TBB, tor uses 9050
        self.proxies = {'http': 'socks5://localhost:'+str(tor_port)} if tor else {}
    def request(self, action, data):
        data['api_key'] = self.api_key
        data = json.dumps(data)
        headers = {'Accept': 'application/json',
                   'Content-Type':'application/json'}
        r = requests.post(self.url + action, data = data, headers = headers, proxies = self.proxies)
        return r.text
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
        data['output'] = output
        if(bm_code):
            data['bm_code'] = bm_code
        return self.request('/order/create', data)

if __name__ == '__main__':
    bm = BestMixer("replace_with_api_key")
    # Example two address LTC mix with 30/70 split 100mins and 400 min delays, 0.5612% fee
    print(bm.orderCreate('ltc', 0.5612,
    [
        {'address': 'Lxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
         'percent': 30,
         'delay': 55
        },
        {'address': 'Lxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
         'percent': 70,
         'delay': 120
        }
    ]
    ))
