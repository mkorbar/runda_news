import scrapy


class TemplateSpider(scrapy.Spider):
    name = 'Template'
    allowed_domains = ['www.domain.com']
    start_urls = ['www.domain.com/news']

    def parse(self, response):
        for article_url in response.css('.node-news').xpath('./a/@href').getall():
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):
        self.log('Parsing article at %s' % response.url)
        content_xpath = ''
        photos_xpath = ''
        yield dict(
            # url=response.url,
            # published=response.css('').get(),
            # categories=[tag.strip() for tag in response.css('').getall()],
            # title=response.css('').get(),
            # subtitle=response.css('').get(),
            # author=response.css('').get(),
            # content=' '.join([p.strip() for p in response.xpath(content_xpath).getall()]),
            # content_photo_urls=response.xpath(photos_xpath).getall(),
        )
