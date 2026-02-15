import os
import uuid as uuid

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from .graphql import IDENTIFY_ACCOUNT_REQUEST, TRACK_EVENT_REQUEST

VERSION = 'v1'


class DashX:
    def __init__(self, base_uri=os.environ.get('DASHX_BASE_URI', 'https://api.dashx.com/graphql'),
                 public_key=os.environ.get('DASHX_PUBLIC_KEY'), private_key=os.environ.get('DASHX_PRIVATE_KEY'),
                 target_environment=os.environ.get('DASHX_TARGET_ENVIRONMENT')):
        self.base_uri = base_uri
        self.public_key = public_key
        self.private_key = private_key
        self.target_environment = target_environment

    def identify(self, uid=None, **params):
        q_params = dict()
        if uid is None:
            q_params['anonymousUid'] = str(uuid.uuid4())
        else:
            q_params['uid'] = str(uid)
        q_params.update(params)

        return self.make_request(q_params, IDENTIFY_ACCOUNT_REQUEST)

    def track(self, event, uid=None, data=None):
        if uid is None:
            return self.make_request({'event': event, 'accountAnonymousUid': str(uuid.uuid4()), 'data': data},
                                     TRACK_EVENT_REQUEST)
        return self.make_request({'event': event, 'accountUid': str(uid), 'data': data}, TRACK_EVENT_REQUEST)

    def make_request(self, q_params, query_name):
        query = gql(query_name)

        transport = AIOHTTPTransport(url=self.base_uri, headers=self.generate_header())

        client = Client(transport=transport, fetch_schema_from_transport=False)
        result = client.execute(query, variable_values={'input': q_params})
        return result

    def generate_header(self):
        return {
            'User-Agent': 'dashx-python',
            'X-Public-Key': self.public_key,
            'X-Private-Key': self.private_key,
            'X-Target-Environment': self.target_environment,
            'Content-Type': 'application/json'
        }
