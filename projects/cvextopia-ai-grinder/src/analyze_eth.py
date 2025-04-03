import requests
import openai


# === CONFIG ===
openai.api_key = "sk-proj-"

CVEX_API_URL = "https://api.cvex.trade"
headers = {
    "X-API-Key": "cvex platform key"
}
ETH_SYMBOL = "ETH-25APR25"

# === 1. Fetch ALL Contracts & Filter for ETH ===
def get_eth_data():
    res = requests.get(f"{CVEX_API_URL}/v1/market/futures", headers=headers)
    res.raise_for_status()
    all_contracts = res.json()["contracts"]

    for contract in all_contracts:
        if contract["symbol"] == ETH_SYMBOL:
            return contract
    raise Exception("ETH contract not found")

# === 2. Ask GPT to Analyze It ===
def ask_gpt_about_eth(data):
    prompt = f"""
You are an AI trading assistant analyzing ETH perpetual futures on CVEX.
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

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# === 3. Run It ===
if __name__ == "__main__":
    eth_data = get_eth_data()
    print("DEBUG CONTRACT FIELDS:\n", eth_data)
    analysis = ask_gpt_about_eth(eth_data)
    print("\nGPT's ETH Market Opinion:\n")
    print(analysis)

    lines = analysis.splitlines()
    try:
        decision_line = [l for l in lines if l.startswith("Decision:")][0]
        confidence_line = [l for l in lines if l.startswith("Confidence:")][0]

        decision = decision_line.split(":")[1].strip()
        confidence = float(confidence_line.split(":")[1].replace("%", "").strip())

        if decision == "LONG" and confidence > 70:
            print("\n Let's buy! GPT is confident.")
        elif decision == "SHORT" and confidence > 70:
            print("\n GPT suggests shorting.")
        else:
            print("\n GPT recommends staying out or isn't confident enough.")
    except Exception as e:
        print("\n Could not parse GPT response properly:", e)
