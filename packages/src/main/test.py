import json

from packages.src.main.client import Client, create_payload

http_client = Client.get_instance()
q = "\n  mutation IdentifyAccount($input: IdentifyAccountInput!) {\n    identifyAccount(input: $input) {\n        " \
    "id\n    }\n  }\n"
payload = create_payload(query=q, anonymousUid="", firstName="", lastName="")
response = http_client.make_http_req("", json.dumps(payload))