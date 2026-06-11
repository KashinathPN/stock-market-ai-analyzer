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
    start_price  = round(close_prices.iloc[0], 2)
    price_change = round(latest - start_price, 2)
    pct_change   = round((price_change / start_price) * 100, 2)

    if price_change >= 0:
        direction = "▲"
    else:
        direction = "▼"
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
    print("-" * 40)
    print("Start of Year :", "$" + str(start_price))
    print("Change        :", direction, "$" + str(price_change))
    print("Change %      :", direction, str(pct_change) + "%")
    print("=" * 40)

except Exception:
    print("Sorry, could not find stock:", symbol)
    print("Please check the symbol and try again.")