import yfinance as yf

symbol = input("Enter stock symbol: ")

stock = yf.Ticker(symbol)

info = stock.info

try:
    print("Company  :", info['longName'])
    print("Price    :", info['currentPrice'])
    print("Currency :", info['currency'])
    print("Market Cap:", info['marketCap'])
    print("52W High :", info['fiftyTwoWeekHigh'])
    print("52W Low  :", info['fiftyTwoWeekLow'])

except KeyError:
    print("Sorry, could not find stock:", symbol)
    print("Please check the symbol and try again.")