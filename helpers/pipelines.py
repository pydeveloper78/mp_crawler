# -*- coding: utf-8 -*-
import hashlib
import logging
import os

from urllib.parse import urlparse

from helpers.models import PageModel, ImageModel, RelationModel, db_connect
from helpers.utils import make_req
from scrapy.pipelines.images import ImagesPipeline
from sqlalchemy.orm import sessionmaker


class CraigslistImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img_id, image_url in enumerate(item['images']):
            req = make_req(image_url)
            yield req

    def item_completed(self, results, item, info):
        item["images"] = results.copy()
        return item

    def file_path(self, request, response=None, info=None):
        return os.path.basename(urlparse(request.url).path)


class CraigslistItemsPipeline(object):
    """ A pipeline to store the items to MySQL """

    def __init__(self):
        engine = db_connect()
        session_maker = sessionmaker(bind=engine)
        self.session = session_maker()

    def process_item(self, item, spider):
        file_path = "{}{}.html".format(os.environ.get("FILES_STORE"), item["id"])
        page_item = {
            "id": item["id"],
            "link": item["link"],
            "store": file_path
        }
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(item['html_content'])
        exist_page = self.session.query(PageModel).filter_by(id=page_item['id']).first()
        if not exist_page:
            new_page_item = PageModel(**page_item)
            self.session.add(new_page_item)

        m = hashlib.md5()
        for img in item['images']:
            m.update(img[1]['path'].encode('utf-8'))
            image_id = m.hexdigest()
            image_item = {
                "id": image_id,
                "link": img[1]['url'],
                "store": "{}{}".format(os.environ.get("FILES_STORE"), img[1]['path'])
            }
            exist_image = self.session.query(ImageModel).filter_by(id=image_item['id']).first()
            if not exist_image:
                new_image_item = ImageModel(**image_item)
                self.session.add(new_image_item)
            relate_item = {
                "page_id": item['id'],
                "image_id": image_id
            }
            exist_relate = self.session.query(RelationModel).filter_by(page_id=relate_item['page_id']).filter_by(
                page_id=relate_item['image_id']).first()
            if not exist_relate:
                new_relate_item = RelationModel(**relate_item)
                self.session.add(new_relate_item)
        try:
            self.session.commit()
        except Exception as e:
            logging.warning("DB Commit Issue: %s" % e)
            self.session.rollback()
            raise
        finally:
            self.session.close()

        return item
