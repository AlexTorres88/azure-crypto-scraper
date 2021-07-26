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
        name_p = name_col.find('p', class_="coin-item-symbol")
        name = ""
        if name_p:
            name = name_p.get_text()  

        # Skip row if the we don't want that crypto
        if name not in coins:
            continue

        price_col = r[3]
        # Find the a tag that contains the price 
        price_a = price_col.find('a')

        price = 0
        if price_a:
            price = price_a.get_text()
        
        market_cap_col = r[6]
        market_cap_p = market_cap_col.find('p')

        market_cap = ""
        if market_cap_p:
            market_cap_p_children = list(market_cap_p.children)
            market_cap = market_cap_p_children[1].get_text()

        
        coin = {}
        coin["name"] = name
        coin["price"] = price
        coin["timestamp"] = datetime.utcnow()
        coin["market_cap"] = market_cap
        res.append(coin)
        ind += 1

    # Convert any type you don't recognize to string (Datetime in this case)
    return  json.dumps(res, indent=4, sort_keys=True, default=str)