from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

def get_prices():
    # Make the request to CoinMarketCap
    page = requests.get('https://coinmarketcap.com/')
    # Turn the content into BeautifulSoup object
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', class_='h7vnx2-2 bFpGkc cmc-table')
    tbody = list(table.children)[2]

    # Define the coins we want to get the price of
    coins = ["BTC", "ETH", "DOGE", "XRP", "USDT", "ADA", "BNB"]

    res = []
    ind = 0
    # Loop through the rows in the table
    for row in tbody.children:
        r = list(row.children)
        name_col = r[2]
        # Find the p tag that contains the name of the coin
        p = name_col.find('p', class_="coin-item-symbol")
        name = ""
        if p:
            name = p.get_text()  

        price_col = r[3]
        # Find the a tag that contains the price 
        a = price_col.find('a')

        price = 0
        if a:
            price = a.get_text()

        coin = {}
        if name in coins: 
            coin["name"] = name
            coin["price"] = price
            coin["timestamp"] = datetime.utcnow()
            res.append(coin)
            ind += 1
    # Convert any type you don't recognize to string (Datetime in this case)
    return  json.dumps(res, indent=4, sort_keys=True, default=str)