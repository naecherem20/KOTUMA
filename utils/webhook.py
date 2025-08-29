# utils/webhook.py
import os
import requests

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:8001/webhook")

def send_webhook(event: str, payload):
    try:
        data = payload.dict() if hasattr(payload, "dict") else payload
        requests.post(WEBHOOK_URL, json={"event": event, "data": data}, timeout=3)
    except Exception as e:
        print(f"[webhook] failed: {e}")
