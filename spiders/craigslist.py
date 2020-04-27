# coding=utf-8

from scrapy import Request, Spider


class CraigslistCrawler(Spider):
    name = 'craigslist'
    start_urls = [
        'https://newyork.craigslist.com'
    ]

    def start_requests(self):
        req = Request(self.start_urls[0])
        yield req

    def parse(self, response):
        print(response.url)
