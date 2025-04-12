import asyncio
import websockets
import json
import hmac
import hashlib
import time
from datetime import datetime

BYBIT_WS_URL = "wss://stream.bybit.com/v5/private"  # Private channel

async def test_bybit_ws():
    """Safe WebSocket validation test for Bybit"""
    try:
        print("🔵 [1/4] Connecting to Bybit WebSocket...")
        async with websockets.connect(BYBIT_WS_URL) as ws:
            
            # 1. Authentication
            expires = int(time.time() * 1000) + 10000
            signature = hmac.new(
                b"g197OJWlyKPWnwC54lQDHoTWEIZvGsZBIgIm",  # Replace with actual secret
                f"GET/realtime{expires}".encode(),
                hashlib.sha256
            ).hexdigest()
            
            auth_msg = {
                "op": "auth",
                "args": ["u5n5VgB4UVsMqIlLRK", expires, signature]  # Replace key
            }
            await ws.send(json.dumps(auth_msg))
            auth_resp = await ws.recv()
            print(f"🟢 [2/4] Auth response: {auth_resp}")

            # 2. Subscribe to balance updates
            await ws.send(json.dumps({
                "op": "subscribe",
                "args": ["wallet"]
            }))
            print("🔵 [3/4] Subscribed to wallet updates")

            # 3. Test message (non-destructive)
            test_msg = {
                "op": "update",
                "args": [{
                    "coin": "BTC",
                    "wallet_balance": "888.88",
                    "test_flag": True,  # Explicit test marker
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }]
            }
            await ws.send(json.dumps(test_msg))
            print("🟡 [4/4] Sent test payload")

            # Monitor for 15 seconds
            start = time.time()
            while time.time() - start < 15:
                msg = await ws.recv()
                print(f"📨 Response: {msg}")
                
    except Exception as e:
        print(f"🔴 Error: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_bybit_ws())
