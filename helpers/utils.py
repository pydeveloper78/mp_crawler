# coding=utf-8
import re

from urllib.parse import urlparse

from scrapy import Request

from helpers.proxies import random_proxy
from helpers.settings import SETTINGS


def make_req(url, **kwargs):
    headers = SETTINGS.get('DEFAULT_REQUEST_HEADERS')
    req = Request(url, headers=headers, **kwargs)
    proxy = random_proxy()
    proxy = None  # should be removed
    req.meta['proxy'] = proxy
    return req


def remove_uris(url):
    urls = urlparse(url)
    return urls.path.split('/')


def resize_image(url):
    if '50x50c' in url:
        url = url.replace('50x50c', '1200x900')
    elif '300x300' in url:
        url = url.replace('600x450', '1200x900')
    elif '600x450' in url:
        url = url.replace('600x450', '1200x900')
    if 'http' not in url:
        url = 'https:' + url
    return url


def get_slug_url(url):
    url = re.sub(r'\W+', '_', url.replace('https://newyork.craigslist.org/', ''))
    return url
