import os

PHANTOMJS_PATH = "/usr/bin/phantomjs"
BROKER_URL = "redis://{0}:6379/0".format(os.environ['REDIS_PORT_6379_TCP_ADDR'])
BACKEND_URL = "redis://{0}:6379/1".format(os.environ['REDIS_PORT_6379_TCP_ADDR'])
STORE_URL = os.environ['REDIS_PORT_6379_TCP_ADDR']