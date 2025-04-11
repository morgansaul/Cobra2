import asyncio
import websockets
import json

async def cancel_spoofed_order():
    try:
        async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
            # Cancel by price (adjust to your spoofed order's price)
            cancel_msg = {
                "op": "cancel",
                "args": [{
                    "symbol": "BTC-USDT",
                    "price": "82000.00"  # Match your spoofed price
                }]
            }
            await ws.send(json.dumps(cancel_msg))
            print("Sent cancellation request - verify in MEXC UI")
            
            # Check response
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            print("Server response:", response)
            
    except Exception as e:
        print("Cancellation failed:", str(e))

asyncio.run(cancel_spoofed_order())
