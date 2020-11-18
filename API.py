# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 23:15:04 2020

@author: helde
"""

import requests

import time

import urllib.parse
import hashlib
import hmac
import base64

class API(object):
    def __init__(self, key='', secret=''):
        self.key = key
        self.secret = secret
        self.uri = 'https://api.kraken.com'
        self.apiversion = '0'
        self.session = requests.Session()

        self.response = None
        return

    # close session
    def close(self):
        self.session.close()
        return

    def _query(self, urlpath, data, headers=None, timeout=None):

        if data is None:
            data = {}
        if headers is None:
            headers = {}

        url = self.uri + urlpath

        self.response = self.session.post(url, data = data, headers = headers,
                                          timeout = timeout)

        if self.response.status_code not in (200, 201, 202):
            self.response.raise_for_status()

        return self.response.json()


    def query_public(self, method, data=None, timeout=None):
        if data is None:
            data = {}

        urlpath = '/' + self.apiversion + '/public/' + method

        return self._query(urlpath, data, timeout = timeout)

    def query_private(self, method, data=None, timeout=None):
        if data is None:
            data = {}

        if not self.key or not self.secret:
            raise Exception('Either key or secret is not set!')

        data['nonce'] = self._nonce()

        urlpath = '/' + self.apiversion + '/private/' + method

        headers = {
            'API-Key': self.key,
            'API-Sign': self._sign(data, urlpath)
        }

        return self._query(urlpath, data, headers, timeout = timeout)

    def _nonce(self):
        return int(1000*time.time())

    def _sign(self, data, urlpath):
        postdata = urllib.parse.urlencode(data)

        # Unicode-objects must be encoded before hashing
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())

        return sigdigest.decode()