# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import json
import psycopg2


class SaveItemToJsonLines:

    def process_item(self, item, spider):
        with open(spider.name + '_scraped_items.jsonl', 'a') as out_file:
            out_file.write(json.dumps(dict(item)) + '\n')
        return item


class SaveItemsToPostgres:
    db_conn = None
    db_cursor = None

    def __init__(self, db_name, db_user, db_pass):
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_name=crawler.settings.get('DB_NAME'),
            db_user=crawler.settings.get('DB_USER'),
            db_pass=crawler.settings.get('DB_PASS')
        )

    def open_spider(self, spider):
        self.db_conn = psycopg2.connect("dbname={} user={} password={}".format(self.db_name, self.db_user, self.db_pass))
        self.db_cursor = self.db_conn.cursor()

    def process_item(self, item, spider):
        if not item['content']:
            logging.warning(item['url'] + ' has no content, skipping DB insert')
            return item

        try:
            self.db_cursor.execute(
                'INSERT INTO articles'
                '(spider_name, url, title, content, published, categories, subtitle, author, photo_urls)'
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                'ON CONFLICT DO NOTHING',
                (
                    spider.name,
                    item['url'],
                    item['title'],
                    item['content'],
                    item['published'],
                    json.dumps(item['categories']),
                    item['subtitle'],
                    item['author'],
                    json.dumps(item['content_photo_urls']),
                )
            )
            self.db_conn.commit()
        except Exception as err:
            with open(spider.name + '_sql.errors', 'a') as err_file:
                err_file.write(str(err))
            self.db_conn.rollback()
        return item

    def close_spider(self, spider):
        self.db_cursor.close()
        self.db_conn.close()
