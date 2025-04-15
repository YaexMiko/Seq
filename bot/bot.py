import time
import logging
from telegram.error import Conflict
from telegram.ext import Updater
from bot.handlers import start_sequence, end_sequence, handle_file

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    TOKEN = "8066028578:AAE0f8wgbClox9N5Lkh04Cq83w16WNzq8a0"  # Replace with your actual bot token

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(start_sequence)
    dp.add_handler(end_sequence)
    dp.add_handler(handle_file)

    logger.info("Bot started...")

    while True:
        try:
            updater.start_polling()
            updater.idle()
            break  # Exit loop if idle() returns (usually on shutdown)
        except Conflict as e:
            logger.error(f"Conflict error: {e}. Another instance might be running.")
            logger.info("Waiting 10 seconds before retrying...")
            time.sleep(10)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.info("Waiting 10 seconds before retrying...")
            time.sleep(10)

if __name__ == "__main__":
    main()
