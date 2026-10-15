from flask import render_template, request
from app import app
import yfinance as yf

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    symbol = request.form['symbol'].upper()
    
    try:
        stock   = yf.Ticker(symbol)
        info    = stock.info
        history = stock.history(period="1y")
        close   = history['Close'].dropna()

        data = {
            'symbol'  : symbol,
            'company' : info['longName'],
            'price'   : round(close.iloc[-1], 2),
            'highest' : round(close.max(), 2),
            'lowest'  : round(close.min(), 2),
            'average' : round(close.mean(), 2),
            'ma20'    : round(close.rolling(window=20).mean().iloc[-1], 2),
            'ma50'    : round(close.rolling(window=50).mean().iloc[-1], 2),
        }

        latest  = data['price']
        ma20    = data['ma20']
        ma50    = data['ma50']

        if latest > ma50 and latest > ma20:
            data['signal'] = 'BUY'
        elif latest < ma50 and latest < ma20:
            data['signal'] = 'SELL'
        else:
            data['signal'] = 'HOLD'

        return render_template('result.html', data=data)

    except Exception:
        error = "Could not find stock: " + symbol
        return render_template('index.html', error=error)