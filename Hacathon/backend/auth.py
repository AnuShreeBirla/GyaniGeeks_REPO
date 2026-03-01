"""Simple JWT-style token for auth (no external deps). For demo we use a fixed secret."""
import hashlib
import json
import base64
import time

SECRET = "learning-iq-secret-2025"

def encode_token(user_id, name, email):
    payload = {"user_id": user_id, "name": name, "email": email, "exp": time.time() + 7 * 24 * 3600}
    b = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    sig = hashlib.sha256((SECRET + b).encode()).hexdigest()
    return b + "." + sig

def decode_token(token):
    if not token or "." not in token:
        return None
    b, sig = token.rsplit(".", 1)
    if hashlib.sha256((SECRET + b).encode()).hexdigest() != sig:
        return None
    try:
        payload = json.loads(base64.urlsafe_b64decode(b.encode()).decode())
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None
