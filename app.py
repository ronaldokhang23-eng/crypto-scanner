from flask import Flask, render_template, jsonify
from scanner import CryptoScanner
import threading
import time
import os
from datetime import datetime

app = Flask(__name__)
scanner = CryptoScanner()
latest_results = []
last_scan_time = None

def continuous_scanner():
    global latest_results, last_scan_time
    while True:
        try:
            print(f"[{datetime.now()}] Scanning...")
            results = list(scanner.scan_all())
            latest_results = results
            last_scan_time = datetime.now()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(30)

threading.Thread(target=continuous_scanner, daemon=True).start()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/results')
def get_results():
    return jsonify({
        'results': latest_results,
        'last_scan': last_scan_time.isoformat() if last_scan_time else None
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
