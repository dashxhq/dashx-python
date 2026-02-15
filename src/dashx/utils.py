"""Utility functions for the DashX SDK."""


def parse_filter_object(filter_object=None):
    """
    Parse a filter dict for searchRecords: keys starting with '_' are top-level,
    others are nested under 'data'.
    """
    if filter_object is None:
        filter_object = {}
    filter_by = {}
    for key, value in filter_object.items():
        if key.startswith('_'):
            filter_by[key[1:]] = value
        else:
            filter_by.setdefault('data', {})[key] = value
    return filter_by
