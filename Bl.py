import asyncio
import websockets
import json
import hmac
import hashlib
import time
from datetime import datetime

BYBIT_WS_URL = "wss://stream.bybit.com/v5/private"

async def test_bybit_ws_safely():
    """Advanced Bybit WebSocket test with protocol-compliant messages"""
    try:
        print("🔵 [1/5] Connecting to Bybit...")
        async with websockets.connect(BYBIT_WS_URL) as ws:
            
            # 1. Authentication (required for private channels)
            expires = int(time.time() * 1000) + 10000
            sig = hmac.new(
                b"g197OJWlyKPWnwC54lQDHoTWEIZvGsZBIgIm",  # Replace with actual secret
                f"GET/realtime{expires}".encode(),
                hashlib.sha256
            ).hexdigest()
            
            await ws.send(json.dumps({
                "op": "auth",
                "args": ["u5n5VgB4UVsMqIlLRK", expires, sig]  # Replace key
            }))
            auth_resp = await ws.recv()
            print(f"🟢 [2/5] Auth: {json.loads(auth_resp)['ret_msg']}")

            # 2. Subscribe to wallet updates (legitimate operation)
            await ws.send(json.dumps({
                "op": "subscribe",
                "args": ["wallet"]
            }))
            sub_resp = await ws.recv()
            print(f"🔵 [3/5] Subscribed: {json.loads(sub_resp)['ret_msg']}")

            # 3. Send test cases that comply with Bybit's protocol
            test_cases = [
                # Valid subscription pattern
                {"op": "subscribe", "args": ["position"]},
                
                # Parameter boundary test
                {"op": "subscribe", "args": ["wallet", "BTC"]},  # Possible variant
                
                # Heartbeat check (if supported)
                {"op": "ping", "req_id": int(time.time())}
            ]

            print("🟡 [4/5] Testing protocol boundaries...")
            for case in test_cases:
                await ws.send(json.dumps(case))
                resp = await ws.recv()
                print(f"📨 {case['op']} response: {resp}")
                await asyncio.sleep(1)  # Rate limit

            # 4. Monitor real wallet updates
            print("🔵 [5/5] Monitoring wallet stream (30s)...")
            start = time.time()
            while time.time() - start < 30:
                msg = await ws.recv()
                if "BTC" in msg:  # Look for balance updates
                    print(f"💰 Balance update: {msg}")
                    
    except Exception as e:
        print(f"🔴 Error: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_bybit_ws_safely())
