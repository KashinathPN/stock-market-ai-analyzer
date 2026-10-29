from flask import render_template, request
from app import app
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from sklearn.linear_model import LinearRegression

def get_rsi(close, period=14):
    delta    = close.diff()
    gain     = delta.where(delta > 0, 0)
    loss     = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs       = avg_gain / avg_loss
    rsi      = 100 - (100 / (1 + rs))
    return rsi

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

def get_ml_prediction(history):
    df = history[['Close', 'Volume']].copy()
    df['MA20']     = df['Close'].rolling(window=20).mean()
    df['MA50']     = df['Close'].rolling(window=50).mean()
    df['Upper']    = df['MA20'] + (df['Close'].rolling(window=20).std() * 2)
    df['Lower']    = df['MA20'] - (df['Close'].rolling(window=20).std() * 2)
    df['RSI']      = get_rsi(df['Close'])
    df['Tomorrow'] = df['Close'].shift(-1)
    df = df.dropna()

    features = ['Close', 'Volume', 'MA20', 'MA50', 'Upper', 'Lower', 'RSI']
    X = df[features]
    y = df['Tomorrow']

    model = LinearRegression()
    model.fit(X, y)

    latest     = df[features].iloc[-1].values.reshape(1, -1)
    prediction = model.predict(latest)[0]
    return round(prediction, 2)

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

        prediction = get_ml_prediction(history)

        data = {
            'symbol'    : symbol,
            'company'   : info['longName'],
            'price'     : round(close.iloc[-1], 2),
            'highest'   : round(close.max(), 2),
            'lowest'    : round(close.min(), 2),
            'average'   : round(close.mean(), 2),
            'ma20'      : round(close.rolling(window=20).mean().iloc[-1], 2),
            'ma50'      : round(close.rolling(window=50).mean().iloc[-1], 2),
            'chart'     : generate_chart(history),
            'prediction': prediction,
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

        change = prediction - latest
        data['pred_change']    = round(abs(change), 2)
        data['pred_direction'] = '▲' if change >= 0 else '▼'

        return render_template('result.html', data=data)

    except Exception:
        error = "Could not find stock: " + symbol
        return render_template('index.html', error=error)