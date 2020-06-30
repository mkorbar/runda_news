# -*- coding: utf-8 -*-
import scrapy


class CyclingtipsComSpider(scrapy.Spider):
    name = 'CyclingTips.com'
    allowed_domains = ['cyclingtips.com']
    start_urls = ['http://cyclingtips.com/']

    def parse(self, response):
        for article_url in response.css('h1 a ::attr("href")').extract():
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):

        self.log('Parsing article at %s' % response.url)
        yield dict(
            title=response.css('div.titles h1::text').get(),
            url=response.url,
            content=response.css("div.entry-content").get()
        )
