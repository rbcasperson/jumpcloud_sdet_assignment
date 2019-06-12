from client import HashServeClient

HASH_SERVE_PORT = 8088


def before_all(context):
    context.client = HashServeClient(HASH_SERVE_PORT)
