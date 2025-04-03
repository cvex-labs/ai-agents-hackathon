import requests
import time
import json
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from config_loader import load_config

# Load configuration
config = load_config()

# Configuration
CVEX_API_URL = config.get("cvex_api_url", "https://api.cvex.trade")
API_KEY = config.get("cvex_api_key", "")
PRIVATE_KEY_PATH = config.get("private_key_path", "./cvexapi.pem")

def load_private_key(file_path):
    try:
        with open(file_path, "rb") as pem_file:
            private_key = serialization.load_pem_private_key(pem_file.read(), password=None)
        return private_key
    except Exception as e:
        print(f"Error loading private key: {e}")
        return None

def generate_signature(method, url, body):
    try:
        private_key = load_private_key(PRIVATE_KEY_PATH)
        if not private_key:
            return None
        message = f"{method} {url}\n{json.dumps(body)}"
        hash_digest = hashlib.sha256(message.encode()).digest()
        signature = private_key.sign(hash_digest)
        return signature.hex()
    except Exception as e:
        print(f"Error generating signature: {e}")
        return None

def place_order(contract_id, order_side, quantity, order_type="market", limit_price="0", time_in_force="GTC", reduce_only=False):
    url = f'{CVEX_API_URL}/v1/trading/order'
    timestamp = int(time.time() * 1000)
    customer_order_id = f"cli-{timestamp}"
    
    quantity_value = str(quantity) if order_side == "buy" else str(-quantity)

    payload = {
        "customer_order_id": customer_order_id,
        "contract": str(contract_id),
        "type": order_type,
        "limit_price": str(limit_price) if order_type == "limit" else "0",
        "time_in_force": time_in_force,
        "reduce_only": reduce_only,
        "quantity_steps": quantity_value,
        "timestamp": timestamp,
        "recv_window": 5000,
        "premium_limit": "100"
    }

    # Debug print to verify the payload
    print("Order Payload:", json.dumps(payload, indent=4))

    signature = generate_signature("POST", url, payload)
    headers = {
        "X-API-Key": API_KEY,
        "X-Signature": signature,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def cancel_all_orders():
    url = f'{CVEX_API_URL}/v1/trading/cancel-all-orders'
    timestamp = int(time.time() * 1000)
    payload = {
        "timestamp": timestamp,
        "recv_window": 5000,
        "premium_limit": "100"
    }
    signature = generate_signature("POST", url, payload)
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Key": API_KEY,
        "X-Signature": signature
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Cancel all orders failed: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def list_orders():
    url = f'{CVEX_API_URL}/v1/portfolio/orders'
    headers = {
        "accept": "application/json",
        "X-API-Key": API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            orders = response.json().get("orders", [])
            return orders
        else:
            return [{"error": f"Failed to fetch orders: {response.status_code} - {response.text}"}]
    except Exception as e:
        return [{"error": str(e)}]

def get_account_overview():
    url = f'{CVEX_API_URL}/v1/portfolio/overview'
    headers = {"X-API-Key": API_KEY}
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_open_orders():
    url = f'{CVEX_API_URL}/v1/portfolio/orders'
    headers = {
        "accept": "application/json",
        "X-API-Key": API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        return response.json().get("orders", [])
    except Exception as e:
        return [{"error": str(e)}]

def get_positions():
    url = f'{CVEX_API_URL}/v1/portfolio/positions'
    headers = {
        "accept": "application/json",
        "X-API-Key": API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        return response.json().get("positions", [])
    except Exception as e:
        return [{"error": str(e)}]
