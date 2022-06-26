import os

PUBLIC_KEY = os.environ.get("DASHX_PUB_KEY")
BASE_URI = os.environ.get("DASHX_BASE_URI")
TARGET_ENV = os.environ.get("DASHX_TARGET_ENV")

"""
    Register/Login
    my_dict = {"query":"\n  mutation IdentifyAccount($input: IdentifyAccountInput!) {\n    identifyAccount(input: $input) {\n        id\n    }\n  }\n",
               "variables":
                   {"input":
                       {
                           "anonymousUid": "ad69dcce-bb96-4b9d-a355-94f491d84514",
                           "email": "john2@example.com"
                       }
                    }
               }
    resp = {
        "data":
            {
                "identifyAccount":
                    {
                        "id": "5ea58ee0-ba05-4b3e-8d57-4628a20f2f4d"
                    }
            }
    }"""

"""
Update
my_dict = {"query":"\n  mutation IdentifyAccount($input: IdentifyAccountInput!) {\n    identifyAccount(input: $input) {\n        id\n    }\n  }\n",
           "variables":
               {"input":
                    {
                        "anonymousUid": "ad69dcce-bb96-4b9d-a355-94f491d84514",
                        "firstName": "John",
                        "lastName": "Doe"
                    }
                }
           }
resp = {
        "data":
            {
                "identifyAccount":
                    {
                        "id":"5ea58ee0-ba05-4b3e-8d57-4628a20f2f4d"
                    }
            }
        }
"""

"""
Start Game
my_dict = {"query":"\n  mutation TrackEvent($input: TrackEventInput!) {\n    trackEvent(input: $input) {\n        id\n    }\n  }\n",
            "variables":
                {"input":
                    {
                        "event": "Clicked Button",
                        "data": {"gameName":"Tetris"},
                        "accountAnonymousUid":"ad69dcce-bb96-4b9d-a355-94f491d84514"
                    }
                }
            }
resp = {
        "data":
            {"trackEvent":
                {
                "id":"00000000-0000-0000-0000-000000000000"
                }
            }
        }
"""

"""

"""