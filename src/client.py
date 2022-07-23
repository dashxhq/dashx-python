import hashlib
import os
import base64
from Crypto.Cipher import AES
from Crypto import Random

import uuid as uuid
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from src.graphql import IDENTIFY_ACCOUNT_REQUEST

VERSION = "v1"

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class Client:
    def __init__(self, base_uri=os.env.get('DASHX_BASE_URI', 'https://api.dashx.com/graphql'),
                 public_key=os.env.get('DASHX_PUBLIC_KEY'), private_key=os.env.get('DASHX_PRIVATE_KEY'),
                 target_environment=os.env.get('DASHX_TARGET_ENVIRONMENT')):
        self.base_uri = base_uri
        self.public_key = public_key
        self.private_key = private_key
        self.target_environment = target_environment

    def identify(self, **params):
        q_params = dict()
        if "uid" not in params:
            q_params["anonymous_uid"] = uuid()
            q_params.update(params)
        else:
            q_params = params

        return self.make_request(q_params, IDENTIFY_ACCOUNT_REQUEST)

    def generate_identity_token(self, uid, **options):
        if self.privateKey is None:
            raise Exception('Private key not set')
        kind = options.get("kind", "regular")
        private_key = hashlib.sha256(self.privateKey.encode("utf-8")).digest()
        raw = pad("{};{};{}".format(VERSION, kind, uid))
        nonce = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_GCM, nonce)
        return base64.b64encode(nonce + cipher.encrypt(raw) + cipher.get_auth_tag()).decode("utf-8")

    def make_request(self, q_params, query_name):
        query = gql(query_name)
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url=self.base_uri, headers=self.generate_header())
        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)
        result = client.execute(query, variable_values=q_params)
        return result

    def generate_header(self):
        return {
            'User-Agent': 'dashx-python',
            'X-Public-Key': self.publicKey,
            'X-Private-Key': self.privateKey,
            'X-Target-Environment': self.targetEnvironment,
            'Content-Type': 'application/json'
        }
