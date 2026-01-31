import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_token():
    auth = (os.getenv("BLIZZ_CLIENT_ID"), os.getenv("BLIZZ_CLIENT_SECRET"))
    r = requests.post("https://oauth.battle.net/token", data={'grant_type': 'client_credentials'}, auth=auth)
    return r.json().get('access_token')

def check_specific_ids():
    token = get_token()
    # These are the reported IDs for the Anniversary TBC Clusters
    # 6001 = Spineshatter Cluster (EU)
    # 6002 = Thunderstrike Cluster (EU)
    test_ids = ["5249", "6027", "5001", "5002"] 
    
    # We use 'dynamic-classic-eu' because that's where Progression lives now
    ns = "dynamic-classic-eu"
    region = "eu"

    print(f"🚀 Attempting direct handshake with IDs in {ns}...")

    for c_id in test_ids:
        url = f"https://{region}.api.blizzard.com/data/wow/connected-realm/{c_id}"
        params = {"namespace": ns, "access_token": token}
        
        r = requests.get(url, params=params)
        if r.status_code == 200:
            data = r.json()
            realm_names = [realm['name']['en_US'] for realm in data.get('realms', [])]
            print(f"✅ SUCCESS! ID {c_id} contains: {', '.join(realm_names)}")
        else:
            print(f"❌ ID {c_id} failed (Status: {r.status_code})")

if __name__ == "__main__":
    check_specific_ids()