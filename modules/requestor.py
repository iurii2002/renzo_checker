import requests
from typing import MutableMapping
from fake_useragent import UserAgent


class Requestor:
    def __init__(self, _headers=None, _proxy=None):
        self.session = requests.Session()
        self.update_headers({
            'User-Agent': UserAgent().random,
        })
        if _headers:
            self.update_headers(_headers)
        if _proxy:
            self.update_proxy(_proxy)

    def update_headers(self, new_header: dict) -> None:
        self.session.headers.update(new_header)

    def get_headers(self) -> MutableMapping[str, str | bytes]:
        return self.session.headers

    def update_proxy(self, new_proxy: dict) -> None:
        self.session.proxies.update(new_proxy)

    def get_proxy(self) -> MutableMapping[str, str | bytes]:
        return self.session.proxies

    @staticmethod
    def handle_response(resp) -> dict:
        if resp.status_code == 200:
            return resp.json()
        else:
            raise requests.exceptions.ConnectionError(resp.status_code)

    def get_request(self, url, data=None, json=None) -> dict:
        return self.handle_response(self.session.get(url=url, data=data, json=json, timeout=10))

    def post_request(self, url, data=None, json=None) -> dict:
        return self.handle_response(self.session.post(url=url, data=data, json=json, timeout=10))

    def put_request(self, url, data=None, json=None) -> dict:
        return self.handle_response(self.session.put(url=url, data=data, json=json, timeout=10))
