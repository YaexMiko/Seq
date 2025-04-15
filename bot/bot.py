from telegram.ext import Updater
from bot.handlers import start_sequence, end_sequence, handle_file

def main():
    TOKEN = "YOUR_BOT_TOKEN"  # Replace with your actual bot token

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(start_sequence)
    dp.add_handler(end_sequence)

    # Register file handler
    dp.add_handler(handle_file)

    print("Bot started...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
  
