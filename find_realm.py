import os
import requests
from dotenv import load_dotenv

load_dotenv()

def find_active_namespaces():
    auth = (os.getenv("BLIZZ_CLIENT_ID"), os.getenv("BLIZZ_CLIENT_SECRET"))
    token = requests.post("https://oauth.battle.net/token", 
                          data={'grant_type': 'client_credentials'}, auth=auth).json().get('access_token')

    # The grid of potential Anniversary/TBC/Era namespaces as of Jan 2026
    prefixes = ["dynamic-classic", "dynamic-classic1x", "dynamic-classicann", "static-classic", "static-classic1x"]
    regions = ["eu", "us"]
    
    # Target realm slug
    target = "spineshatter"

    print(f"📡 Scanning Blizzard API for active {target} namespaces...")

    for region in regions:
        for prefix in prefixes:
            ns = f"{prefix}-{region}"
            url = f"https://{region}.api.blizzard.com/data/wow/realm/index"
            params = {"namespace": ns, "locale": "en_US", "access_token": token}
            
            try:
                r = requests.get(url, params=params)
                if r.status_code == 200:
                    realms = r.json().get('realms', [])
                    for realm in realms:
                        if target in realm.get('slug', ''):
                            # FOUND IT - Now get the Connected Realm ID
                            realm_data = requests.get(realm['key']['href'], params={"access_token": token}).json()
                            cr_id = realm_data.get('connected_realm', {}).get('href').split('/')[-1].split('?')[0]
                            
                            print(f"\n🎯 MATCH FOUND!")
                            print(f"   Namespace: {ns}")
                            print(f"   Slug: {realm.get('slug')}")
                            print(f"   Connected Realm ID: {cr_id}")
                            return
                else r.status_code == 401:
                    print(f"🛑 Status: {r.status_code}")
                    return
            except Exception as e:
                continue
                
    print("\n❌ Spineshatter not found in standard or seasonal namespaces.")

if __name__ == "__main__":
    find_active_namespaces()