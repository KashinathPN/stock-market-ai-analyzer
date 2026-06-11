import yfinance as yf

def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    history = stock.history(period="1y")
    return info, history

def analyze_prices(close_prices):
    highest      = round(close_prices.max(), 2)
    lowest       = round(close_prices.min(), 2)
    average      = round(close_prices.mean(), 2)
    latest       = round(close_prices.iloc[-1], 2)
    ma20         = round(close_prices.rolling(window=20).mean().iloc[-1], 2)
    ma50         = round(close_prices.rolling(window=50).mean().iloc[-1], 2)
    start_price  = round(close_prices.iloc[0], 2)
    price_change = round(latest - start_price, 2)
    pct_change   = round((price_change / start_price) * 100, 2)
    return highest, lowest, average, latest, ma20, ma50, start_price, price_change, pct_change

def print_report(symbol, company, highest, lowest, average, latest, ma20, ma50, start_price, price_change, pct_change):
    direction = "▲" if price_change >= 0 else "▼"
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

def compare_stocks(symbols):
    print("=" * 60)
    print("              STOCK COMPARISON")
    print("=" * 60)
    print(f"{'Symbol':<8} {'Latest':>8} {'MA20':>8} {'MA50':>8} {'Change%':>10} {'Trend':>6}")
    print("-" * 60)

    for symbol in symbols:
        try:
            info, history = get_stock_data(symbol)
            close_prices = history['Close'].dropna()
            highest, lowest, average, latest, ma20, ma50, start_price, price_change, pct_change = analyze_prices(close_prices)
            direction = "▲" if price_change >= 0 else "▼"
            print(f"{symbol:<8} ${latest:>7} ${ma20:>7} ${ma50:>7} {pct_change:>9}% {direction:>6}")
        except Exception:
            print(f"{symbol:<8} Could not fetch data")

    print("=" * 60)

def main():
    print("1. Single Stock Analysis")
    print("2. Compare Multiple Stocks")
    choice = input("Choose (1 or 2): ")

    if choice == "1":
        symbol = input("Enter stock symbol: ").upper()
        try:
            info, history = get_stock_data(symbol)
            close_prices  = history['Close'].dropna()
            highest, lowest, average, latest, ma20, ma50, start_price, price_change, pct_change = analyze_prices(close_prices)
            print_report(symbol, info['longName'], highest, lowest, average, latest, ma20, ma50, start_price, price_change, pct_change)
        except Exception:
            print("Sorry, could not find stock:", symbol)

    elif choice == "2":
        symbols = input("Enter symbols separated by comma (e.g. AAPL,TSLA,MSFT): ").upper().split(",")
        compare_stocks(symbols)

main()