import json  
import scrapy
from scrapy.http import Response
from scrapy.selector import Selector

class ListingsSpider(scrapy.Spider):
    name = "listings"
    allowed_domains = ["www.centris.ca\en"]

    position ={
        "startPosition": 0
    }


    def start_requests(self):
        query = {
        "query":{
            "UseGeographyShapes":0,
            "Filters":[
                {
                    "MatchType":"CityDistrictAll",
                    "Text":"Longueuil (All boroughs)",
                    "Id":4
                }
            ],
            "FieldsValues":[
                {
                    "fieldId":"CityDistrictAll",
                    "value":4,
                    "fieldConditionId":"",
                    "valueConditionId":""
                },
                {
                    "fieldId":"Category",
                    "value":"Commercial",
                    "fieldConditionId":"",
                    "valueConditionId":""
                },
                {
                    "fieldId":"SellingType",
                    "value":"Rent",
                    "fieldConditionId":"",
                    "valueConditionId":""
                },
                {
                    "fieldId":"RentPrice",
                    "value":0,
                    "fieldConditionId":"ForRent",
                    "valueConditionId":""
                },
                {
                    "fieldId":"RentPrice",
                    "value":999999999999,
                    "fieldConditionId":"ForRent",
                    "valueConditionId":""
                }
            ]
        },
        "isHomePage":True
        }
        yield scrapy.Request(
            url="https://www.centris.ca/property/UpdateQuery&locale=en",
            method='POST',
            body=json.dumps(query),#to convert from dect to string
            headers={
                'Content-Type':'application/json',
                'Accept-Language': 'en'
            },
            
            callback=self.update_query
            )

    def update_query(self, response):
        yield scrapy.Request(
            url="https://www.centris.ca/Property/GetInscriptions",
            method='POST',
            body=json.dumps(self.position),#to convert from dect to string
            headers={
                'Content-Type':'application/json',
                'Accept-Language': 'en'
            },
            callback=self.parse
        )
    def parse(self, response):
        resp_dict = json.loads(response.body)
        html= resp_dict.get('d').get('Result').get('html')
        sel = Selector(text=html)
        listings = sel.xpath('//div[@class="property-thumbnail-item thumbnailItem col-12 col-sm-6 col-md-4 col-lg-3"]')
        for listing in listings:
            category = (listing.xpath('.//span[@class="category"]/div/text()').get()).strip()
           # price    = listing.xpath('.//div[@class="price"]/span/font/font/text()') + listing.xpath('.//div[@class="price"]/span[@class="desc"]/font/font/text()').get()
            street   = listing.xpath('(//span[@class="address"]/div/text())[1]').get()
            city     = listing.xpath('(//span[@class="address"]/div/text())[2]').get()
            Neighborhoods = listing.xpath('(//span[@class="address"]/div/text())[3]').get()
            url = "www.centris.ca/en" + (listing.xpath('.//a[@class="a-more-detail"]/@href').get()).split("/", 2)[2]

            yield{
                'category': category,
                #'price' : price,
                'street': street,
                'city' : city,
                'Neighborhoods' : Neighborhoods,
                'url' : url
            }

        count = resp_dict.get('d').get('Result').get('count')
        increment_number = resp_dict.get('d').get(
            'Result').get('inscNumberPerPage')

        if self.position['startPosition'] <= count:
            self.position['startPosition'] += increment_number
            yield scrapy.Request(
                url="https://www.centris.ca/Mvc/Property/GetInscriptions",
                method="POST",
                body=json.dumps(self.position),
                headers={
                    'Content-Type': 'application/json'
                },
                callback=self.parse
            )