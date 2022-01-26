import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request

# import de notre Classe MongoClient
from pymongo import MongoClient


class MySpider(scrapy.Spider):
    name = "CoinGecko"
    start_urls = ["https://www.coingecko.com/en"]

    def parse(self, response):
        crypto = {}
        crypto_name = list(jsonCryptoName.keys())
        for cry in crypto_name:
            for cit in response.xpath(f'//span[@data-coin-symbol="{cry}"]'):
                if cit is not {}:
                    crypto_value = cit.xpath("text()").extract_first()
                    crypto[jsonCryptoName[cry]] = crypto_value

        links = allLinks(crypto)
        Request()

        for link, name in zip(links.values(), jsonCryptoName.values()):
            yield Request(link, callback=self.parse_data)

    def parse_data(self, response):
        value = []  # Value of crypto : "MarketCap" +"Volume" + "Open" + "Close" // 4 values par days
        date = []  # Date of each value group
        name = response.request.url.replace("https://www.coingecko.com/en/coins/", "").replace(
            "/historical_data/usd?end_date=2022-01-18&start_date=2021-10-20#panel", "")  # Name of the crypto

        # Scraping of all values
        for rep in response.xpath('//td[@class="text-center"]/text()'):
            value.append(rep.extract().replace("\n", ""))

        # Scraping all dates
        for d in response.xpath('//th[@class="font-semibold text-center"]/text()'):
            date.append(d.extract())

        # Put data in mongo db
        coll = db[name]
        coll.delete_many({})
        for i in range(len(value) // 4):
            coll.insert_one(
                {"date": date[i], "MarketCap": value[(i * 4)], "Volume": value[(i * 4) + 1], "Open": value[(i * 4) + 2],
                 "Close": value[(i * 4) + 3]})


def allLinks(dict):
    name = list(dict.keys())
    links = {}
    for n in name:
        links[n] = "https://www.coingecko.com/en/coins/" + n + "/historical_data/usd?end_date=2022-01-18&start_date=2021-10-20#panel"
    return links


if __name__ == "__main__":
    jsonCryptoName = {"btc": "bitcoin", "eth": "ethereum", "bnb": "binance-coin", "ada": "cardano", "sol": "solana"}

    # Coonect to MONGODB
    client = MongoClient("mongo")
    if client.connect == False:
        print("Mongo not connected")

    # Create our database
    db = client["coingecko"]

    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()

    for document in db["ethereum"].find() :
        print('-----')
        print(document)
    print(db.list_collection_names())