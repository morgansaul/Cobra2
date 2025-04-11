import websockets
import json

async def check_third_party_vulnerability():
    async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
        # Subscribe to account updates
        await ws.send(json.dumps({"op": "subscribe", "args": ["account:BTC-USDT"]}))
        
        while True:
            msg = await ws.recv()
            if "BTC" in msg:
                print("Raw WebSocket Balance:", msg)
                break  # Compare this to real API balance

asyncio.run(check_third_party_vulnerability())
