def create_payload(*args, **kwargs):
    body = dict()
    query = kwargs.get("query")
    body["query"] = query
    body["variables"] = dict()
    body["variables"]["input"] = dict()
    for params in kwargs.keys():
        if params != "query":
            body["variables"]["input"][params] = kwargs[params]
    return body


def create_query(query_type):
    if query_type == "identify":
        return identify_query
    if query_type == "reset":
        return reset_query


identify_query = """ "\n  mutation IdentifyAccount($input: IdentifyAccountInput!) {\n    identifyAccount(
input: $input) {\n        id\n    }\n  }\n", """
reset_query = """ "\n  mutation TrackEvent($input: TrackEventInput!) {\n    trackEvent(input: $input) {\n        id\n   
 }\n  }\n" """
