import requests

CVEX_API_URL = 'https://api.cvex.trade'
API_KEY = 'manualy insert your key here'

def get_positions():
    url = f'{CVEX_API_URL}/v1/portfolio/positions'
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        if response.status_code == 200:
            positions = response.json().get("positions", [])
            print(f"Positions Data: {positions}")
            return positions
        else:
            print(f"Error: {response.text}")
            return [{"error": f"Failed to fetch positions: {response.text}"}]
    except Exception as e:
        print(f"Exception: {str(e)}")
        return [{"error": str(e)}]

# Run the test
positions = get_positions()
print("Positions Retrieved:")
print(positions)
