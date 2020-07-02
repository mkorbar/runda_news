import datetime
import scrapy


class CyclingtipsComSpider(scrapy.Spider):
    name = 'CyclingTips'
    allowed_domains = ['cyclingtips.com']
    start_urls = ['http://cyclingtips.com/category/news/']

    def parse(self, response):
        for article_url in set(response.css('h1.PostSnippet__title a::attr("href")').getall()):
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):
        self.log('Parsing article at %s' % response.url)
        published = datetime.datetime.strptime(response.css('div.meta p.date::text').get(), '%B %d, %Y')
        yield dict(
            url=response.url,
            published=str(published),
            categories=response.css('div.article-tags a::text').getall(),
            title=response.css('div.titles h1::text').get(),
            subtitle=None,
            author=response.css('div.titles p.author::text').get()[3:],
            content=' '.join(response.css("div#soft-paywall-container p::text").getall()),
            content_photo_urls=response.css('div.feature-large img::attr("src")').getall(),
        )
