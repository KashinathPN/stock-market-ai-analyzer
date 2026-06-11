import yfinance as yf

symbol = input("Enter stock symbol: ")

stock = yf.Ticker(symbol)

try:
    history = stock.history(period="1mo")

    close_prices = history['Close']

    print("Stock :", symbol)
    print("Highest price this month :", round(close_prices.max(), 2))
    print("Lowest price this month  :", round(close_prices.min(), 2))
    print("Average price this month :", round(close_prices.mean(), 2))
    clean_prices = close_prices.dropna()
    print("Latest closing price     :", round(clean_prices.iloc[-1], 2))

except Exception:
    print("Sorry, could not find stock:", symbol)
    print("Please check the symbol and try again.")