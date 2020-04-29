# coding=utf-8
from scrapy import Field, Item


class ProductItem(Item):
    id = Field()
    link = Field()
    slug = Field()
    html_content = Field()
    images = Field()
