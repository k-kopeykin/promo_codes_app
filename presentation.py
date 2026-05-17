from constants import HEADERS


def build_object(row):
    client = dict(zip(HEADERS, row))
    return client

def do_callable_phone(client):
    if '+' not in client['phone']:
        client['phone'] = '+' + str(client['phone'])
    return client