import sqlite3
from datetime import datetime, timedelta
from binance.client import Client
import os

class CryptoScanner:
    def __init__(self):
        self.client = Client()
        self.symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']
        os.makedirs('/data', exist_ok=True)
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect('/data/levels.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS levels
                        (symbol TEXT, date TEXT, poc REAL, val REAL, vah REAL)''')
        conn.commit()
        conn.close()
    
    def scan_all(self):
        for symbol in self.symbols:
            try:
                ticker = self.client.get_symbol_ticker(symbol=symbol)
                price = float(ticker['price'])
                
                # Simulated levels (will work immediately)
                yield {
                    'symbol': symbol,
                    'price': price,
                    'vwap': price * 0.998,
                    'touching_vwap': abs(price - price*0.998) / price < 0.0005,
                    'prev_poc': price * 0.99,
                    'touching_prev_poc': False,
                    'prev_val': price * 0.98,
                    'touching_prev_val': False,
                    'prev_vah': price * 1.02,
                    'touching_prev_vah': False
                }
            except Exception as e:
                yield {'symbol': symbol, 'price': 0, 'error': str(e)}
