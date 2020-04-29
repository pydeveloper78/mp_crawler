# coding=utf-8
import argparse
import logging
import os
from datetime import datetime

from helpers.settings import SETTINGS
from helpers.models import create_table

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from spiders.craigslist import CraigslistCrawler

from twisted.internet import defer, reactor


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Handle the crawler')
    parser.add_argument('--url', '-u', type=str, help='set the start url of a vendor', default=None)
    parser.add_argument('--limit', '-l', type=int, help='set the limt items to close the spider', default=None)
    parser.add_argument('--create', '-c', type=str, help='create the tables at the first time (y / n)', default=None)
    args = parser.parse_args()
    if args.create == 'y':
        create_table()
        exit(0)

    if not os.path.exists('log'):
        os.mkdir('log')
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler('log/cl_%s.log' % (datetime.utcnow().strftime("%Y%m%d%H%M%S"))),
            logging.StreamHandler()
        ]
    )
    logging.getLogger('scrapy').setLevel(logging.ERROR)
    # custom settings for Scrapy

    custom_settings = get_project_settings()
    custom_settings.update(SETTINGS)
    if args.limit:
        custom_settings.update({
            'CLOSESPIDER_ITEMCOUNT': args.limit
        })
    # create the runner
    runner = CrawlerRunner(custom_settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(CraigslistCrawler)
        reactor.stop()
    crawl()
    reactor.run()
