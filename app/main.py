import yfinance as yf

symbol = input("Enter stock symbol: ").upper()

stock = yf.Ticker(symbol)

try:
    info = stock.info
    history = stock.history(period="1y")
    close_prices = history['Close'].dropna()

    highest = round(close_prices.max(), 2)
    lowest  = round(close_prices.min(), 2)
    average = round(close_prices.mean(), 2)
    latest  = round(close_prices.iloc[-1], 2)
    ma20 = round(close_prices.rolling(window=20).mean().iloc[-1], 2)
    ma50 = round(close_prices.rolling(window=50).mean().iloc[-1], 2)
    company = info['longName']

    print("=" * 40)
    print("       STOCK ANALYSIS REPORT")
    print("=" * 40)
    print("Symbol  :", symbol)
    print("Company :", company)
    print("-" * 40)
    print("Highest :", "$" + str(highest))
    print("Lowest  :", "$" + str(lowest))
    print("Average :", "$" + str(average))
    print("Latest  :", "$" + str(latest))
    print("MA20    :", "$" + str(ma20))
    print("MA50    :", "$" + str(ma50))
    print("=" * 40)

except Exception:
    print("Sorry, could not find stock:", symbol)
    print("Please check the symbol and try again.")