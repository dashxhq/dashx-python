import os
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportError

from src.graphql import IDENTIFY_ACCOUNT_REQUEST


class Client:
    def __init__(self, base_uri=os.env.get('DASHX_BASE_URI', 'https://api.dashx.com/graphql'),
                 public_key=os.env.get('DASHX_PUBLIC_KEY'), private_key=os.env.get('DASHX_PRIVATE_KEY'),
                 target_environment=os.env.get('DASHX_TARGET_ENVIRONMENT')):
        self.base_uri = base_uri
        self.public_key = public_key
        self.private_key = private_key
        self.target_environment = target_environment

    def identify(self, user_id, first_name, last_name, email):
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url=self.base_uri, headers=self.generate_header())

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)
        params = {"input": user_id} # To do: need to change this to take all the user information
        query = gql(IDENTIFY_ACCOUNT_REQUEST)
        try:
            result = client.execute(query, variable_values=params)
            return result
        except TransportError:
            raise Exception("GraphQL request to backend service unsuccessful")

    def generate_header(self):
        return {
            'User-Agent': 'dashx-python',
            'X-Public-Key': self.publicKey,
            'X-Private-Key': self.privateKey,
            'X-Target-Environment': self.targetEnvironment,
            'Content-Type': 'application/json'
        }