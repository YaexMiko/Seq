import time
import logging
from telegram.error import Conflict
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Import handlers from handlers.py
from bot.handlers import start_sequence_handler, end_sequence_handler, handle_file_handler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    # Replace with your actual bot token
    TOKEN = "8066028578:AAF7y-f6xryRbK_xUNfV6sjIVilBrVUeBcI"  

    # Initialize the Updater and Dispatcher
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(start_sequence_handler)
    dp.add_handler(end_sequence_handler)
    dp.add_handler(handle_file_handler)

    logger.info("Bot started...")

    while True:
        try:
            # Start polling for updates
            updater.start_polling()
            # Idle the bot until it is stopped
            updater.idle()
            # Break the loop if idle() returns (usually on shutdown)
            break  
        except Conflict as e:
            # Handle conflict errors (e.g., another instance running)
            logger.error(f"Conflict error: {e}. Another instance might be running.")
            logger.info("Waiting 10 seconds before retrying...")
            time.sleep(10)
        except Exception as e:
            # Handle other unexpected errors
            logger.error(f"Unexpected error: {e}")
            logger.info("Waiting 10 seconds before retrying...")
            time.sleep(10)

if __name__ == "__main__":
    main()
