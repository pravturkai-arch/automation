from flask import Flask, request, jsonify
from waitress import serve
import logging
import datetime

app = Flask(__name__)

# Setup logging
logging.basicConfig(
    filename='webhook_trade_log.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        logging.warning("No JSON received in webhook")
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    # Extract scanner name and basic fields
    scanner = data.get("scanner_name") or data.get("trigger_name") or "UNKNOWN"
    symbol = data.get("symbol")
    price = data.get("price")

    # Route based on scanner name
    if "PRAV_SWTR_BUY" in scanner:
        handle_swtr_buy(symbol, price, scanner)
    elif "PRAV_RRBO_BUY" in scanner:
        handle_rrbo_buy(symbol, price, scanner)
    else:
        logging.warning(f"Unknown scanner: {scanner} | Payload: {data}")

    return jsonify({"status": "received"}), 200

def handle_swtr_buy(symbol, price, scanner):
    logging.info(f"[{scanner}] EMA crossover BUY triggered for {symbol} at {price}")
    # TODO: Add Dhan order execution here
    print(f"Executing SWTR trade for {symbol} at {price}")

def handle_rrbo_buy(symbol, price, scanner):
    logging.info(f"[{scanner}] 125-day breakout BUY triggered for {symbol} at {price}")
    # TODO: Add Dhan order execution here
    print(f"Executing RRBO trade for {symbol} at {price}")

if __name__ == '__main__':
    print("Starting enhanced webhook listener...")
    serve(app, host="0.0.0.0", port=5000)
