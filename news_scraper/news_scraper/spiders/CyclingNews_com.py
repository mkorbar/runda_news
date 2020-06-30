# -*- coding: utf-8 -*-
import json

import scrapy


class CyclingnewsComSpider(scrapy.Spider):
    name = 'CyclingNews.com'
    allowed_domains = ['cyclingnews.com']
    start_urls = ['http://cyclingnews.com/']

    def parse(self, response):
        for article_url in response.css('a.article-link ::attr("href")').extract():
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):

        self.log('Parsing article at %s' % response.url)
        yield dict(
                title=response.css('h1::text').get(),
                url=response.url,
                content=response.css("div#article-body").get()
        )
        return
