import hmac
import hashlib
import requests
import time

api_key = "mx0vgljUyNUYQzJrOk"
api_secret = "60fe1e4b81c148438ef8efdf2a7ff7bd"  # Never hardcode in scripts
address = "bc1q5s699tp4smz6fe6r42d44yrntpmms9xy2yu7dq"  # Your test address

timestamp = int(time.time() * 1000)
params = {
    "coin": "BTC",
    "address": address,
    "amount": "0.001",  # Minimal test amount
    "timestamp": timestamp
}
query_string = "&".join(f"{k}={v}" for k,v in params.items())
signature = hmac.new(
    api_secret.encode(),
    query_string.encode(),
    hashlib.sha256
).hexdigest()

response = requests.post(
    f"https://api.mexc.com/api/v3/withdraw?{query_string}&signature={signature}",
    headers={"X-MEXC-APIKEY": api_key}
)
print(response.json())
