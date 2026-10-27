from flask import render_template, request
from app import app
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

def generate_chart(history):
    close = history['Close'].dropna()
    ma20  = close.rolling(window=20).mean()
    ma50  = close.rolling(window=50).mean()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(close.index, close, color='#1D9E75', linewidth=1.5, label='Price')
    ax.plot(close.index, ma20,  color='#F5A623', linewidth=1.5, label='MA20', linestyle='--')
    ax.plot(close.index, ma50,  color='#E24B4A', linewidth=1.5, label='MA50', linestyle='--')
    ax.set_facecolor('#1a1a1a')
    fig.patch.set_facecolor('#1a1a1a')
    ax.tick_params(colors='white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.legend(facecolor='#1a1a1a', labelcolor='white')
    ax.grid(True, alpha=0.2)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#1a1a1a')
    buf.seek(0)
    chart = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return chart

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
            'chart'   : generate_chart(history),
        }

        latest = data['price']
        ma20   = data['ma20']
        ma50   = data['ma50']

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