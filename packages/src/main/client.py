import json

import requests

from packages.src.main.constants import PUBLIC_KEY, BASE_URI, TARGET_ENV
from packages.src.main.utils import create_payload, create_query


class Client:
    __shared_instance = "HTTP Client"

    pub_key = None
    base_uri = None

    def __init__(self):

        if Client.__shared_instance != "HTTP Client":
            raise Exception("This class is a singleton class !")
        else:
            self.pub_key = PUBLIC_KEY
            self.base_uri = BASE_URI
            self.target_env = TARGET_ENV
            Client.__shared_instance = self

    @staticmethod
    def get_instance():

        """Static Access Method"""
        if Client.__shared_instance == "HTTP Client":
            Client()
        return Client.__shared_instance

    def get_header(self):
        return {
            'User-Agent': 'dashx-py',
            'X-Public-Key': self.pub_key,
            'X-Target-Environment': self.target_env,
            'Content-Type': 'application/json'
        }

    def make_http_req(self, req_uri, body):
        header = self.get_header()
        return requests.post(url=self.base_uri + req_uri, headers=header, data=body)

    def identify(self, uuid):
        body = create_payload(query=create_query("identify"), anonymousAccountId=uuid)
        return self.make_http_req(self.base_uri, json.dumps(body))

    def reset(self, uuid):
        body = create_payload(query=create_query("reset"), anonymousAccountId=uuid)
        return self.make_http_req(self.base_uri, json.dumps(body))

