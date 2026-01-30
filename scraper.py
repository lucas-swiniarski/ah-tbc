import os
import sqlite3
import logging
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("scraper.log"),
                        logging.StreamHandler()
                    ])

DB_FILE = "ah_data.sqlite"
access_token = None
token_expires_at = None
last_modified = None

def get_access_token(client_id, client_secret):
    global access_token, token_expires_at
    if access_token and token_expires_at and datetime.now() < token_expires_at:
        return access_token
    logging.info("Requesting new access token...")
    url = "https://oauth.battle.net/token"
    data = {"grant_type": "client_credentials"}
    try:
        response = requests.post(url, data=data, auth=(client_id, client_secret))
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 86400)
        token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
        logging.info("New access token obtained.")
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting access token: {e}")
        return None

def setup_database():
    """Create the database and table if they don't exist."""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS auctions (
                snapshot_time TEXT,
                auction_id INTEGER,
                item_id INTEGER,
                buyout INTEGER,
                quantity INTEGER,
                time_left TEXT,
                PRIMARY KEY (snapshot_time, auction_id)
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def scrape_auction_house():
    """Scrape the auction house data and save it to the database."""
    global last_modified
    
    client_id = os.getenv("BLIZZ_CLIENT_ID")
    client_secret = os.getenv("BLIZZ_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        logging.error("BLIZZ_CLIENT_ID or BLIZZ_CLIENT_SECRET not set in .env file.")
        return
        
    token = get_access_token(client_id, client_secret)
    if not token:
        return
        
    try:
        headers = {
            'Authorization': f'Bearer {token}'
        }
        if last_modified:
            headers['If-Modified-Since'] = last_modified
            
        logging.info("Checking for new auction data...")
        
        connected_realm_id = 3656  # Spinebreaker EU
        region = "eu"
        namespace = f"dynamic-{region}"
        
        url = f"https://{region}.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}/auctions"
        
        params = {
            'namespace': namespace,
            'locale': 'en_GB',
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 304:
            logging.info("Auction data has not been modified since last check.")
            return

        response.raise_for_status()

        if response.status_code == 200:
            last_modified = response.headers.get('Last-Modified')
            auction_data = response.json()
            
            snapshot_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            
            auctions_to_insert = []
            for auction in auction_data.get('auctions', []):
                auction_id = auction.get('id')
                item_id = auction.get('item', {}).get('id')
                buyout = auction.get('buyout')
                quantity = auction.get('quantity')
                time_left = auction.get('time_left')
                
                if auction_id and item_id and quantity and time_left:
                    auctions_to_insert.append((snapshot_time, auction_id, item_id, buyout, quantity, time_left))

            if auctions_to_insert:
                c.executemany('''
                    INSERT OR IGNORE INTO auctions (snapshot_time, auction_id, item_id, buyout, quantity, time_left)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', auctions_to_insert)
            
            conn.commit()
            logging.info(f"Successfully saved {len(auctions_to_insert)} new auctions to the database.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error making API request: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    setup_database()
    scrape_auction_house()
