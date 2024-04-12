import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMovesSpider(CrawlSpider):
    name = 'best_moves'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield {
            'title': response.xpath("//h1[@class='sc-b73cd867-0 fbOhB']/text()").get(),
            'year': response.xpath("//span[@class='sc-8c396aa2-2 itZqyK'][1]/text()").get(),
            'hours': response.xpath("//li[@class='ipc-inline-list__item'][3]/text()").get(),
            'rating': response.xpath("//span[@class='sc-7ab21ed2-1 jGRxWM'][1]/text()").get(),
            'movie_url': response.url
        }