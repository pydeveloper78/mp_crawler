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
            link = link.split('#')[0]
            if link in ['#', '/', '', None] or '?sale_date=' in link or '?lang=' in link or '?sort=' in link:
                continue
            elif '//' not in link:
                link = response.urljoin(link)
            elif 'http' not in link:
                link = 'https:' + link
            if 'newyork.craigslist.org' in link:
                req = make_req(link)
                yield req
