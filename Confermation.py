# Quick verification script (save as check_trades.py)
import requests
import json

def check_public_trades():
    try:
        response = requests.get(
            "https://www.mexc.com/open/api/v2/market/deals?symbol=BTC_USDT&limit=10",
            timeout=5
        )
        trades = response.json().get('data', [])
        for trade in trades:
            if float(trade['price']) == 85000.00 and float(trade['qty']) >= 500:
                print(f"🔴 VULNERABILITY CONFIRMED IN PUBLIC DATA: {trade}")
                with open("mexc_public_proof.txt", "w") as f:
                    json.dump(trade, f, indent=2)
                return
        print("🟢 Spoofed trade not in public feeds (may be internal only)")
    except Exception as e:
        print(f"🔴 API check failed: {str(e)}")

check_public_trades()
