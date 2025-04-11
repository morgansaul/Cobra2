import requests
import json
from datetime import datetime

def verify_spoofed_trade():
    """Check if the spoofed trade appears in public data"""
    try:
        print("🔵 Checking MEXC public trade API...")
        response = requests.get(
            "https://api.mexc.com/api/v3/trades?symbol=BTCUSDT&limit=100",
            headers={"User-Agent": "MEXC-Audit-Tool/1.0"},
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"🔴 API Error: HTTP {response.status_code}")
            return

        trades = response.json()
        spoofed_price = 85000.00
        
        for trade in trades:
            # Handle both string and numeric price formats
            price = float(trade.get('price') or trade.get('p', 0))
            qty = float(trade.get('qty') or trade.get('q', 0))
            
            if abs(price - spoofed_price) < 0.01 and qty >= 500:
                print(f"🔴 CRITICAL: Spoofed trade found in public data!")
                print(json.dumps(trade, indent=2))
                
                with open("mexc_confirmed_poc.txt", "w") as f:
                    f.write(f"Public Trade Verification - {datetime.now()}\n")
                    f.write("Spoofed Trade Confirmed:\n")
                    f.write(json.dumps(trade, indent=2))
                    f.write("\n\nCompare with original injection:\n")
                    f.write(open("mexc_trades_poc.txt").read())
                return
                
        print("🟢 Spoofed trade not found in public API (may affect internal systems only)")
        
    except Exception as e:
        print(f"🔴 Verification failed: {str(e)}")

verify_spoofed_trade()
