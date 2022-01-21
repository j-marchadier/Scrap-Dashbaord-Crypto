import scrapy
from scrapy.crawler import CrawlerProcess
from flask import Flask, request
from scrapy import Request
import requests




class MySpider(scrapy.Spider):
    name = "CoinMarketCap"
    start_urls = ["https://coinmarketcap.com"]

    def parse(self, response):
        crypto ={}
        for cit in response.xpath('//div[@class="sc-131di3y-0 cLgOOr"]'):
            crypto_name = cit.xpath('a/@href').get()
            if crypto_name is not None:
                crypto_name = crypto_name.replace("/currencies/","").replace("/markets/","")   #Optionel
                crypto_value = cit.xpath('a//span/text()').extract_first()
                crypto[crypto_name] = crypto_value

        links = allLinks(crypto)
        print(links)
        print(crypto)
        for link in links.values():
            yield Request('https://coinmarketcap.com/currencies/bitcoin/historical-data/',formdata={'xhr':'1'}, callback=self.parse_data)


    def parse_data(self, response):
        for rep in response.xpath('//table[@class="h7vnx2-2 hLKazY cmc-table  "]'):
            #https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=1&convertId=2781&timeStart=1637193600&timeEnd=1642464000
            print(rep)


print(requests.get(url="https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=1&convertId=2781&timeStart=1637020800&timeEnd=1642291200").json())





app = Flask(__name__)

@app.route('/')
def new_transaction():

    return "Success", 201


def allLinks(dict):
    name = list(dict.keys())
    links = {}
    for n in name:
        links[n] = "https://coinmarketcap.com/currencies/" + n + "/historical-data/"
    return links




if __name__ == "__main__":
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(MySpider)
    process.start()
    #app.run(debug=True, port=5001)
# app.run(host='0.0.0.0', port=5001)