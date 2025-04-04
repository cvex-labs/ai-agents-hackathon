import requests
import openai
from config_loader import load_config

# Load configuration
config = load_config()

# Configuration
openai.api_key = config.get("openai_api_key", "")
CVEX_API_URL = config.get("cvex_api_url", "")
HEADERS = {
    "X-API-Key": config.get("cvex_api_key", "")
}

def get_all_contracts():
    """Fetches all available contracts from CVEX."""
    try:
        res = requests.get(f"{CVEX_API_URL}/v1/market/futures", headers=HEADERS)
        res.raise_for_status()
        contracts = res.json().get("contracts", [])
        print("DEBUG: Fetched contracts:")
        print(contracts)  # Print the raw contract data for inspection
        return contracts
    except Exception as e:
        print(f"Error fetching contracts: {e}")
        return []

def analyze_market(data):
    """Analyzes market data using GPT."""
    try:
        prompt = f"""
        You are an AI trading assistant analyzing perpetual futures on CVEX.
        Here is the current contract data:

        - Symbol: {data['symbol']}
        - Mark Price: {data['mark_price']}
        - Index Price: {data['index_price']}
        - 24h Volume: {data['volume_24h']}
        - 24h High: {data['high_24h']}
        - 24h Low: {data['low_24h']}
        - Open Interest: {data['open_interest']}

        Based on this, please do the following:
        1. Decide if the best move is to: LONG, SHORT, or STAY OUT.
        2. Provide a confidence score from 0 to 100% for that decision.
        3. Explain the reasoning briefly (in less than 5 sentences).
        Only return your answer in this format:
        Decision: <LONG/SHORT/STAY OUT>
        Confidence: <number>% 
        Reason: <your reason>
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error analyzing market data: {e}")
        return None

def parse_gpt_response(analysis):
    """Parses GPT response to extract decision and confidence."""
    try:
        lines = analysis.splitlines()
        decision_line = [l for l in lines if l.startswith("Decision:")][0]
        confidence_line = [l for l in lines if l.startswith("Confidence:")][0]

        decision = decision_line.split(":")[1].strip()
        confidence = float(confidence_line.split(":")[1].replace("%", "").strip())

        return decision, confidence
    except Exception as e:
        print(f"Error parsing GPT response: {e}")
        return None, None
