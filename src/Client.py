import os


class Client:
    def __init__(self, base_uri=os.env.get('DASHX_BASE_URI', 'https://api.dashx.com/graphql'),
                 public_key=os.env.get('DASHX_PUBLIC_KEY'), private_key=os.env.get('DASHX_PRIVATE_KEY'),
                 target_environment=os.env.get('DASHX_TARGET_ENVIRONMENT')):
        self.base_uri = base_uri
        self.public_key = public_key
        self.private_key = private_key
        self.target_environment = target_environment
