#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
#	Name    : twitterAPI
#	Author  : Ting
#   Version : 1
#   Purpose : Finds tweets of certain topics and loads their stats to a 
#               GoogleSheet 
#
###############################################################################

# Import from Standard Packages
import logging
import traceback
import json, hmac, hashlib, time, requests, base64
from argparse import ArgumentParser

# Import from 3rd Party Packages
from requests.auth import AuthBase


class CoinbaseExchangeAuth(AuthBase):
    """Create custom authentication for Exchange"""
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        # https://stackoverflow.com/questions/37763235/unicode-objects-must-be-encoded-before-hashing-error
        signature_b64 = base64.b64encode(signature.digest())  
        # signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


class coinbaseAPI: 

    def __init__(self, *args, **kwargs): 
        self.auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)
        self.parse_args = self._parse_args()
        self.api_url = "https://api.pro.coinbase.com/" if self.test else "https://public.sandbox.pro.coinbase.com/"

    def _parse_args(self):
        parser = ArgumentParser()
        parser.add_argument('--verbose', required=False, action='store_true', help="Print input, data, and output")
        parser.add_argument('--test', required=False, action='store_true', help="Print input, data, and output")
        # args, trash = parser.parse_known_args(namespace=self.flags)
        args, trash = parser.parse_known_args()

        return args

    def AccountInfo(self): 
        """Get accounts"""
        r = requests.get(f"{self.api_url}accounts", auth=self.auth)

        return r.json() 

    def submitOrder(self, size=1.0, price=1.0, orderType='buy', product_id='BTC-USD'):
        """Place an order"""
        order = {
            'size': 1.0,
            'price': 1.0,
            'side': orderType,
            'product_id': product_id,
        }
        r = requests.post(f"{self.api_url}orders", json=order, auth=self.auth)

        return r.json() 
