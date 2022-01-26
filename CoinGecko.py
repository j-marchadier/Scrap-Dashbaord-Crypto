import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


# docker-compose up -d --build  && docker compose down -v

def scrapingAll(names, links):
    # Boucle Scraping
    for (name, url) in zip(names, links.values()):

        # get request to the url website to download its content
        content = requests.get(url).content

        # parsing the page content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        tds = soup.find_all("td")
        data = [float(str(td.text.strip()).replace("$", "").replace(",", "").replace("N/A", "0")) for td in tds]

        dates = soup.find_all("th", class_="font-semibold text-center")
        data_dates = [date.text.strip() for date in dates]

        # Put data in mongo db
        coll = db[jsonCryptoName[name]]
        coll.delete_many({})
        for i in range(len(data) // 4):
            coll.insert_one(
                {"date": data_dates[i], "marketcap": data[(i * 4)], "volume": data[(i * 4) + 1],
                 "open": data[(i * 4) + 2],
                 "close": data[(i * 4) + 3]})


def allLinks(dict, date):
    name = list(dict.values())
    links = {}
    for n in name:
        links[
            n] = "https://www.coingecko.com/en/coins/" + n + "/historical_data/usd?end_date=" + date[
            0] + "&start_date=" + date[1] + "#panel"
    return links


if __name__ == "__main__":
    jsonCryptoName = {"btc": "bitcoin", "eth": "ethereum", "bnb": "binance-coin", "ada": "cardano", "sol": "solana"}
    links = allLinks(jsonCryptoName, ["2022-01-18", "2021-10-21"])

    # Coonect to MONGODB
    client = MongoClient("0.0.0.0:27017")

    # Create our database
    db = client["coingecko"]

    scrapingAll(jsonCryptoName, links)

    # for document in db["ethereum"].find():
    #    print('-----')
    #    print(document)
    print(db.list_collection_names())
