import yfinance as yf

symbol = input("Enter stock symbol: ")

stock = yf.Ticker(symbol)

info = stock.info

print("Company  :", info['longName'])
print("Price    :", info['currentPrice'])
print("Currency :", info['currency'])
print("Market Cap:", info['marketCap'])
print("52W High :", info['fiftyTwoWeekHigh'])
print("52W Low  :", info['fiftyTwoWeekLow'])