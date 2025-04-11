import asyncio
import websockets
import json
from datetime import datetime

async def mobile_ui_test():
    """Safe mobile UI glitch detection"""
    try:
        print("🔵 [1/3] Connecting...")
        async with websockets.connect("wss://wbs.mexc.com/ws") as ws:
            # Authenticate (read-only scope)
            auth_msg = {
                "op": "auth",
                "args": ["YOUR_API_KEY", int(time.time()*1000), "SIGNATURE"] 
            }
            await ws.send(json.dumps(auth_msg))
            
            # Target mobile-specific UI elements
            glitch = {
                "op": "update",
                "args": [{
                    "target": "mobile_balance_display",
                    "test_value": "888.88 BTC",
                    "metadata": {
                        "test_id": f"audit_{datetime.now().date()}",
                        "purpose": "security_research"
                    }
                }]
            }
            await ws.send(json.dumps(glitch))
            print("🟡 [2/3] Sent mobile UI test payload")

            # Monitor for 15 seconds
            await asyncio.sleep(15)
            print("🟢 [3/3] Test completed - check mobile app")

    except Exception as e:
        print(f"🔴 Error: {str(e)}")

asyncio.run(mobile_ui_test())
