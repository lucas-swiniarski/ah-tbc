import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

load_dotenv()

def get_access_token(client_id, client_secret):
    url = "https://oauth.battle.net/token"
    data = {"grant_type": "client_credentials"}
    try:
        response = requests.post(url, data=data, auth=(client_id, client_secret))
        response.raise_for_status()
        token_data = response.json()
        print(token_data["access_token"])
    except requests.exceptions.RequestException as e:
        print(f"Error getting access token: {e}")

if __name__ == "__main__":
    client_id = os.getenv("BLIZZ_CLIENT_ID")
    client_secret = os.getenv("BLIZZ_CLIENT_SECRET")
    get_access_token(client_id, client_secret)
