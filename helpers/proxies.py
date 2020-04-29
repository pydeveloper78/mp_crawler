import os
import random


with open(os.environ.get('PROXY_FILE_PATH')) as f:
    PROXY_LIST = [p.strip() for p in f.readlines() if p]


def random_proxy():
    proxy_length = len(PROXY_LIST)
    if proxy_length > 0:
        return PROXY_LIST[random.randint(0, proxy_length - 1)]
    else:
        return None


def next_proxy(proxy):
    if len(PROXY_LIST) > 0:
        current_index = PROXY_LIST.index(proxy)
        next_index = current_index + 1 if current_index < len(PROXY_LIST) - 1 else 0
        return PROXY_LIST[next_index]
    else:
        return None
