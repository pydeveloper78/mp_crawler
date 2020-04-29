# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv


load_dotenv('.env')

SETTINGS = {
    "USER_AGENT": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/79.0.3945.117 Safari/537.36',
    "CONCURRENT_REQUESTS": 10,
    "CONCURRENT_REQUESTS_PER_DOMAIN": 10,
    "DOWNLOAD_DELAY": 0.2,
    "RANDOMIZE_DOWNLOAD_DELAY": True,
    "DEFAULT_REQUEST_HEADERS": {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113'
                      ' Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,applicati'
                  'on/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
    },
    "RETRY_ENABLED": True,
    "RETRY_TIMES": 5,
    "ITEM_PIPELINES": {
        'helpers.pipelines.CraigslistImagesPipeline': 10,
        'helpers.pipelines.CraigslistItemsPipeline': 200,
    },
    "IMAGES_EXPIRES": "180",
    "FILES_STORE": os.environ.get("FILES_STORE"),
    "IMAGES_STORE": os.environ.get("IMAGES_STORE"),
    "IMAGE_MIN_WIDTH": 50,
    "IMAGE_MIN_HEIGHT": 50
}
