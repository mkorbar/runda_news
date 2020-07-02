import scrapy


class RoadSpider(scrapy.Spider):
    name = 'Road'
    allowed_domains = ['road.cc']
    start_urls = ['https://road.cc/news']

    def parse(self, response):
        for article_url in response.css('.node-news').xpath('./a/@href').getall():
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):
        self.log('Parsing article at %s' % response.url)
        content_paragraphs = response.css('.full__body').xpath('.//p//text()').getall()
        yield dict(
            url=response.url,
            published=response.css('.full__date span').xpath('./@content').get(),
            categories=response.css('.full__tag .field-item a::text').getall(),
            title=response.css('h1::text').get(),
            subtitle=response.css('.full__description div div div::text').get(),
            author=response.css('.full__author .name a::text').get(),
            content=' '.join(content_paragraphs),
            content_photo_urls=response.css('.full__image img').xpath('@data-src').getall(),
        )
