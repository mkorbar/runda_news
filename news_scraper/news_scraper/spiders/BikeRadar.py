import unicodedata
import scrapy


class BikeradarSpider(scrapy.Spider):
    name = 'BikeRadar'
    allowed_domains = ['www.bikeradar.com']
    start_urls = ['http://www.bikeradar.com/news/']

    def parse(self, response):
        for article_url in response.css('h4 a::attr("href")').getall():
            if '/news/' in article_url:
                yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):
        self.log('Parsing article at %s' % response.url)
        content_xpath = '//section[@itemprop="articleBody"]/p//text()'
        photos_xpath = '//div[@class="template-article__main-content"]//picture//img/@data-src'
        yield dict(
            url=response.url,
            published=response.css('.template-article__published-date time::attr("datetime")').get(),
            categories=[tag.strip() for tag in response.css('.post-tags__tag-group li a::text').getall()],
            title=response.css('h1::text').get(),
            subtitle=response.css('div.template-article__description p::text').get(),
            author=response.css('.author-name p span a::text').get(),
            content=' '.join([unicodedata.normalize('NFKD', p).strip() for p in response.xpath(content_xpath).getall()]),
            content_photo_urls=response.xpath(photos_xpath).getall(),
        )
