#!/usr/bin/env python3
"""
This module aims to wrap every request done.
It handles session cookies, but it's up to the user to:
* enable authentication
* decide ip/host
* decide if http or https should be used.
"""

import requests
import time
from .bbox_api_endpoints import BboxApiEndpoints

class BboxRequests():

    def __init__(self, api_host: str=None, password: str=None) -> None:
        self.api_host = api_host or 'https://mabbox.bytel.fr'
        self.password = password
        self.needs_auth = self.password is not None

        self.session = requests.session()
        self.session.headers = {}
        self.cookies = {}

    def url(self, api_path: str) -> str:
        return f'{self.api_host}/api/v1/{api_path}'

    def request(self, kind: str, path: str, data: dict=None) -> requests.Response:
        assert kind in [ 'get', 'put', 'post', 'delete' ]
        url = self.url(path)
        data = data or {}

        print(kind, path, data)

        # post needs a token.
        if kind == 'post':
            token = self.get_token()
            symbol = '&' if '?' in url else '?'
            url = f'{url}{symbol}btoken={token}'

        result = self.session.request(kind, url, data=data)

        # Retry if authentication was needed
        if result.status_code == 401 and self.needs_auth:
            self.do_auth()
            result = self.session.request(kind, url, data=data)

        if int(result.status_code/100) != 2:
            raise RuntimeError(f'Error for request at {url}: {result.text}')

        return result.json()[0]

    def do_auth(self) -> requests.Response:
        kind, api = BboxApiEndpoints.login
        url = self.url(api)
        result = self.session.request(kind, url, data={'password': self.password})
        if result.status_code != 200:
            result.raise_for_status()
        else:
            return result

    def get_token(self) -> str:
        result = self.request(*BboxApiEndpoints.get_token)
        return result.json()[0]['device']['token']
