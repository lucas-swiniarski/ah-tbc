import os
from dotenv import load_dotenv
from blizzardapi2 import BlizzardApi

load_dotenv()

def find_realm():
    api = BlizzardApi(os.getenv("BLIZZ_CLIENT_ID"), os.getenv("BLIZZ_CLIENT_SECRET"))
    try:
        data = api.wow.game_data.get_connected_realms_index("eu", "en_GB")
        for connected_realm in data['connected_realms']:
            href = connected_realm['href']
            # extract connected_realm_id from href
            # e.g. "https://eu.api.blizzard.com/data/wow/connected-realm/1080?namespace=dynamic-eu"
            connected_realm_id = int(href.split("connected-realm/")[1].split("?")[0])
            response = api.wow.game_data.get_connected_realm("eu", "en_GB", connected_realm_id)
            for realm in response['realms']:
                if "spineshatter" in realm['slug']:
                    print(response)
    except Exception as e:
        print(f"--- ERROR --- {e}")

if __name__ == "__main__":
    find_realm()