import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from scraper import scrape_auction_house, setup_database

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("scraper.log"),
                        logging.StreamHandler()
                    ])

if __name__ == "__main__":
    setup_database()
    
    scheduler = BlockingScheduler()
    
    # Run once immediately
    scrape_auction_house()

    # Then run every 15 minutes
    scheduler.add_job(scrape_auction_house, 'interval', minutes=15)
    
    logging.info("Scheduler started. Next run in 15 minutes. Press Ctrl+C to exit.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
