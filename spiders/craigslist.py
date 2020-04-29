# coding=utf-8
import hashlib
import logging
# from base64 import b64encode
# from zlib import compress

from helpers.items import ProductItem
from helpers.utils import make_req, resize_image

from scrapy import Spider


class CraigslistCrawler(Spider):
    name = 'craigslist'
    allowed_domains = ['images.craigslist.org', 'newyork.craigslist.org']
    start_urls = [
        'https://newyork.craigslist.org'
    ]
    url_seen = set()

    def start_requests(self):
        for start_url in self.start_urls:
            yield make_req(start_url)

    def parse(self, response):
        if response.url in self.url_seen:
            return
        logging.info("URL: %s" % response.url)
        self.url_seen.add(response.url)
        item = ProductItem()
        m = hashlib.md5()
        m.update(response.url.encode('utf-8'))
        item['id'] = m.hexdigest()
        item['link'] = response.url
        item['html_content'] = response.text
        item['images'] = list(set([resize_image(img) for img in response.css('img[src]::attr(src)').getall() if img]))
        yield item

        links = response.css('a[href]::attr(href)').getall()
        for link in links:
            _link = link.rstrip('/').strip()
            _link = _link.split('#')[0].strip()
            if _link in ['#', '/', '', None] or '?sale_date' in _link or '?lang=' in _link or '?sort=' in _link:
                continue
            elif '//' not in _link:
                _link = response.urljoin(_link)
            if 'http' not in _link and '//' in _link:
                _link = 'https:' + _link
            _link = _link.strip()
            if 'newyork.craigslist.org' in _link:
                req = make_req(_link)
                yield req
