import os
from dotenv import load_dotenv
from blizzardapi2 import BlizzardApi

load_dotenv()

def test():
    api = BlizzardApi(os.getenv("BLIZZ_CLIENT_ID"), os.getenv("BLIZZ_CLIENT_SECRET"))
    try:
        # Fetching the "Connected Realms" index for TBC/Classic
        data = api.wow.game_data.get_connected_realms_index("us", "en_US")
        print("--- SUCCESS! ---")
        print(f"Found {len(data['connected_realms'])} connected realms.")
    except Exception as e:
        print(f"--- ERROR --- \n{e}")

if __name__ == "__main__":
    test()