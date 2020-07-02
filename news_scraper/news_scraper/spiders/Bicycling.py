import scrapy


class BicyclingSpider(scrapy.Spider):
    name = 'Bicycling'
    allowed_domains = ['www.bicycling.com']
    start_urls = ['http://www.bicycling.com/news']

    def parse(self, response):
        for article_url in response.css('div.full-item a::attr("href")').getall():
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):
        self.log('Parsing article at %s' % response.url)
        content_parts = response.css('p.body-text').xpath('.//text()').getall()
        yield dict(
            url=response.url,
            published=response.css('time.content-info-date::attr("datetime")').get(),
            categories=[],
            title=response.css('h1::text').get(),
            subtitle=response.css('div.content-dek p::text').get().strip(),
            author=response.css('span.byline-name::text').get(),
            content=' '.join([p.strip() for p in content_parts]),
            content_photo_urls=[response.css('div.content-lede-image-wrap img').attrib['data-src']],
        )
