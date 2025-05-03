import time
import logging
from telegram.error import Conflict
from telegram.ext import Application, CommandHandler, MessageHandler
from telegram.ext import filters

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
    TOKEN = "7607446696:AAGonUJAt-jdQar9G8GKHnr3uAMPjKAjluA"  

    # Initialize the Application
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(start_sequence_handler)
    application.add_handler(end_sequence_handler)
    application.add_handler(handle_file_handler)

    logger.info("Bot started...")

    while True:
        try:
            # Start polling for updates
            application.run_polling()
            # Break the loop if run_polling() returns (usually on shutdown)
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
