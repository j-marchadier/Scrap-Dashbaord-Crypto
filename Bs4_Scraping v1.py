import requests
from bs4 import BeautifulSoup

# Dictionnaire pour les urls
urls = dict()
urls['BTC'] = "https://www.coingecko.com/en/coins/bitcoin/historical_data/usd#panel"
urls['ETH'] = "https://www.coingecko.com/en/coins/ethereum/historical_data/usd#panel"

# Boucle Scraping 
for (name, url) in urls.items():
    
    # get request to the url website to download its content
    content = requests.get(url).content
    
    # parsing the page content with BeautifulSoup
    soup = BeautifulSoup(content,'html.parser')
    
    tds=soup.find_all("td")
    data = [td.text.strip() for td in tds]
    
    dates=soup.find_all("th", class_="font-semibold text-center")
    data_dates= [date.text.strip() for date in dates]
    
    
    
    print("\n",name,"\n")
    print("Dates :\n\n",data_dates,"\n")
    print ("Values :\n\n",data)    
    
    print("\n\n------------------------\n")