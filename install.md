Install Scrappy and packages

```
$ pip install Scrapy
$ pip install unicodedata
$ pip install psycopg2
```

Create database, user access and `articles` table with `./database.sql` script.
Fill the `DB_NAME`, `DB_USER` and `DB_PASS` in `settings.py`

Run the spider from `./news_scraper/` with command `scrapy runspider news_scraper/spiders/__spider_name__.py` 
