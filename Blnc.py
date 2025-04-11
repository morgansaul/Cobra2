import hmac
import hashlib
import requests
import time

api_key = "mx0vgljUyNUYQzJrOk"
api_secret = "60fe1e4b81c148438ef8efdf2a7ff7bd"

timestamp = int(time.time() * 1000)
signature = hmac.new(
    api_secret.encode(),
    f"timestamp={timestamp}".encode(),
    hashlib.sha256
).hexdigest()

response = requests.get(
    f"https://api.mexc.com/api/v3/account?timestamp={timestamp}&signature={signature}",
    headers={"X-MEXC-APIKEY": api_key}
)

print("BTC Balance:", [b for b in response.json()['balances'] if b['asset'] == 'BTC'])
