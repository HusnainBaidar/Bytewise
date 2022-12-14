# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class ScrapyProjectPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = '127.0.0.1',
            user = 'root',
            password = 'admin',
            database = 'myquotes',
            auth_plugin='mysql_native_password'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS qoutes_tb""")
        self.curr.execute("""create table qoutes_tb(title text,
                            author text,
                            tag text)""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute("""insert into qoutes_tb values(%s,%s,%s)""",
        (item['title'][0],
        item['author'][0],
        item['tag'][0])
        )
        self.conn.commit()
