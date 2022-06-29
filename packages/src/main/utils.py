from packages.src.main.client import identify_query, reset_query


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
