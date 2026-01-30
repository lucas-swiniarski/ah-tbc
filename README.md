# WoW Auction House Scraper

This project contains a Python script to scrape the World of Warcraft auction house data for a specific realm and save it to a SQLite database.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file:**
    Create a file named `.env` in the root of the project and add your Blizzard API credentials:
    ```
    BLIZZ_CLIENT_ID=your_client_id
    BLIZZ_CLIENT_SECRET=your_client_secret
    ```

## How to Run

To start the scraper, which will run once immediately and then every 15 minutes, run the following command:

```bash
python app.py
```

The script will log its activity to `scraper.log` and to the console. You can stop the scraper by pressing `Ctrl+C`.

## How to Check the Database

You can use the `sqlite3` command-line tool to inspect the `ah_data.sqlite` database.

1.  **Open the database file:**
    ```bash
    sqlite3 ah_data.sqlite
    ```

2.  **Run SQL queries:**
    *   To see the tables: `.tables`
    *   To count the auctions: `SELECT COUNT(*) FROM auctions;`
    *   To see 10 auctions: `SELECT * FROM auctions LIMIT 10;`

3.  **Exit sqlite3:**
    ```
    .quit
    ```
    If you don't have `sqlite3` installed, you can install it on Debian/Ubuntu with:
    ```bash
    sudo apt-get update && sudo apt-get install sqlite3
    ```
