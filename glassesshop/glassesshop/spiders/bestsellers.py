import scrapy


class BestsellersSpider(scrapy.Spider):
    name = "bestsellers"
    allowed_domains = ["www.glassesshop"]
    start_urls = ["https://www.glassesshop.com/bestsellers"]

    def parse(self, response):
        glasses = response.xpath("//div[@id = 'product-lists']/div")
        for glass in glasses:
            yield {
                'name' : glass.xpath("normalize-space(.//div[@class ='p-title']/a/text())").get(),
                'url' : glass.xpath(".//div[@class ='product-img-outer']/a/@href").get(),
                'image_url' : glass.xpath(".//div[@class ='product-img-outer']/a/img/@src").get(),
                'price' :glass.xpath(".//div[@class ='p-price']//span/text()").get()
            }

        next_page = response.xpath(
            "//ul[@class='pagination']/li[position() = last()]/a/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)


