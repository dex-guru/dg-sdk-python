import urllib


def get_query_from_params(**kwargs):
    params = {k: v for k, v in kwargs.items() if v}
    params.pop('self', None)
    params.pop('chain_id', None)
    query = urllib.parse.urlencode(params)
    return query
