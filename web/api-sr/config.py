import os


class Config(object):

    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    TMP_DIR = os.environ.get('TMP_DIR') or './'
