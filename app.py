from flask import Flask, render_template, jsonify
from binance.client import Client
import os

app = Flask(__name__)

# ==============================
# LOAD API KEYS
# ==============================


API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

client = Client(API_KEY, API_SECRET)
client.session.headers.update({"User-Agent": "Mozilla/5.0"})
client.API_URL = "https://testnet.binance.vision/api"

SYMBOL = "BTCUSDT"

# ==============================
# ROUTES
# ==============================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/assets")
def assets():
    account = client.get_account()

    balances = {
        b['asset']: float(b['free']) + float(b['locked'])
        for b in account['balances']
        if float(b['free']) > 0 or float(b['locked']) > 0
    }

    btc_qty = balances.get('BTC', 0)
    usdt_qty = balances.get('USDT', 0)

    price = float(client.get_symbol_ticker(symbol=SYMBOL)['price'])
    btc_value = btc_qty * price
    total_value = btc_value + usdt_qty
    unrealized_pl = total_value - 10000

    return jsonify({
        "BTC_qty": btc_qty,
        "USDT_qty": usdt_qty,
        "BTC_price": price,
        "BTC_value": btc_value,
        "Total_value": total_value,
        "Unrealized_PL": unrealized_pl
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
