# coding=utf-8
from scrapy import Field, Item
from scrapy.loader.processors import Join, MapCompose, TakeFirst

class ProductItem(Item):
	images = Field()