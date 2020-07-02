import unicodedata
import scrapy


class CyclingnewsComSpider(scrapy.Spider):
    name = 'CyclingNews'
    allowed_domains = ['cyclingnews.com']
    start_urls = ['http://cyclingnews.com/']

    def parse(self, response):
        for article_url in response.css('a.article-link ::attr("href")').getall():
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):

        self.log('Parsing article at %s' % response.url)
        content_parts = response.css("div#article-body").xpath('./p//text()|h2//text()').getall()
        yield dict(
                url=response.url,
                published=response.css('p.byline time::attr("datetime")').get(),
                categories=[],
                title=response.css('h1::text').get(),
                subtitle=response.css('p.strapline::text').get(),
                author=response.css('span.by-author a span::text').get(),
                content=' '.join([unicodedata.normalize('NFKD', p).strip() for p in content_parts]),
                content_photo_urls=response.css("img.hero-image::attr('src')").getall(),
        )
        return
