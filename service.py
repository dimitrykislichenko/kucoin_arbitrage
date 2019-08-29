import requests

# The URL for REST API
REST_API_URL = "https://api.kucoin.com/api"

def main():
    print("Starting service")

    orderbook = {}
    symbols = getSymbols()
    # symbols = list(["REQ-ETH", "REQ-BTC", "ETH-BTC"])
    for symbol in symbols:
        print("-> Processing %s symbol" % symbol)
        
        parts = symbol.split("-")
        if parts[0] not in orderbook:
            orderbook[parts[0]] = {}
        orderbook[parts[0]][parts[1]] = getOrderBook(symbol);

    findArbitrage(orderbook)

# Returns order book for specified symbol
def getOrderBook(symbol):
    response = requests.get(url = "%s/v2/market/orderbook/level2" % REST_API_URL, params = {"symbol": symbol})
    return response.json()["data"]

# Returns set of symbols avilable on exchange
def getSymbols():
    response = requests.get(url = "%s/v1/symbols" % REST_API_URL)
    return [item["symbol"] for item in response.json()["data"]]

# Try to find possible arbitrage in provided order book
def findArbitrage(orderbook):
    # Take market for each tradable symbol
    for symbol, market in orderbook.items():
        # Take each tradable pair
        for tradingPair in market:
            # ... and find it's own market
            if tradingPair in orderbook:
                for subSymbol, subMarket in orderbook[tradingPair].items():
                    # Continue if tradable pair has maket that is available in the market of the symbol that we are processing
                    if subSymbol in market:
                        # print("Checking arbitrage for combination of %s - %s - %s" % (symbol, tradingPair, subSymbol))
                        firstPrice = float(market[subSymbol]["bids"][1][0])
                        secondPrice = float(subMarket["bids"][1][0]) / (1 / float(market[tradingPair]["bids"][1][0]))
                        if firstPrice > secondPrice:
                            print("Buy %s for %s and sell for %s, price diff %f" % (symbol, subSymbol, tradingPair, firstPrice - secondPrice))
                        else:
                            print("Buy %s for %s and sell for %s, price diff %.10f" % (symbol, tradingPair, subSymbol, secondPrice - firstPrice))

if __name__ == "__main__":
    main()