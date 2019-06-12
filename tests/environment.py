from client import HashServeClient

HASH_SERVE_PORT = 8088
# I've hard-coded this in here and checked the binary into the repo
# to make things work for me, and make it clear how things were working for me.
# Ideally, this executable would be set up with a common name regardless of OS,
# but that is beyond the scope of this assignment.
PATH_TO_EXECUTABLE = "./bin/broken-hashserve_darwin"


def before_all(context):
    context.client = HashServeClient(HASH_SERVE_PORT, PATH_TO_EXECUTABLE)
    context.client.start()


def after_all(context):
    context.client.shut_down()
