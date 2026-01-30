import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_tsm_access_token():
    """Obtains an access token from the TSM authentication API."""
    tsm_api_key = os.getenv("TSM_API_KEY")
    if not tsm_api_key:
        logging.error("TSM_API_KEY not found in .env file.")
        return None

    auth_url = "https://auth.tradeskillmaster.com/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": tsm_api_key,
        "grant_type": "api_key",
        "scope": "app:realm-api",
        "token": tsm_api_key,
    }
    try:
        response = requests.post(auth_url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error obtaining TSM access token: {e}")
        return None

def get_tsm_regions(token):
    """Gets the list of regions from the TSM API."""
    if not token:
        return None
    
    url = "https://api.tradeskillmaster.com/regions"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting TSM regions: {e}")
        return None

def get_tsm_realms(token, region_id):
    """Gets the list of realms for a given region from the TSM API."""
    if not token:
        return None
        
    url = f"https://api.tradeskillmaster.com/regions/{region_id}/realms"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting TSM realms: {e}")
        return None

def find_tsm_realm(realm_name):
    """Finds a realm in the TSM database."""
    token = get_tsm_access_token()
    if not token:
        return

    regions = get_tsm_regions(token)
    if not regions:
        return

    for region in regions:
        if region['regionId'] == 'EU': # Search in EU region
            realms = get_tsm_realms(token, region['regionId'])
            if not realms:
                continue
            for realm in realms:
                if realm_name.lower() in realm['name'].lower():
                    logging.info(f"Found TSM realm: {realm}")
                    return realm
    
    logging.warning(f"TSM realm '{realm_name}' not found.")
    return None

if __name__ == "__main__":
    find_tsm_realm("Spineshatter")
