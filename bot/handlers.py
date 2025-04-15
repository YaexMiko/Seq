from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
import logging

logger = logging.getLogger(__name__)

# In-memory storage for user file sequences
user_sequences = {}

def start_sequence(update: Update, context: CallbackContext):
    """
    Initializes a new file sequencing process for the user.
    """
    user_id = update.effective_user.id
    user_sequences[user_id] = []  # Initialize an empty list for the user's file sequence
    update.message.reply_text(
        "You've started a file sequencing process. Send the files you want to sequence one by one.\n\n"
        "When you're done, use /endsequence to finish and get the sequenced files."
    )
    logger.info(f"User {user_id} started a new file sequence.")

# Handler for the /startsequence command
start_sequence_handler = CommandHandler("startsequence", start_sequence)

def handle_file(update: Update, context: CallbackContext):
    """
    Adds a file to the user's current file sequence.
    """
    user_id = update.effective_user.id
    if user_id not in user_sequences:
        update.message.reply_text("Please start a sequence using /startsequence first.")
        return

    file = update.message.document
    caption = update.message.caption  # Can be None
    caption_entities = update.message.caption_entities  # Can be None

    if file:
        # Ensure we have a filename (some files might not have one)
        file_name = file.file_name or f"file_{len(user_sequences[user_id]) + 1}"
        
        user_sequences[user_id].append({
            "file_id": file.file_id,
            "file_name": file_name,
            "caption": caption,
            "caption_entities": caption_entities
        })
        update.message.reply_text(f"File added to sequence: {file_name}")
        logger.info(f"User {user_id} added file {file_name} to sequence.")
    else:
        update.message.reply_text("Please send a valid file.")

# Handler for file messages
handle_file_handler = MessageHandler(Filters.document, handle_file)

def end_sequence(update: Update, context: CallbackContext):
    """
    Ends the file sequencing process and sends back the sequenced files with original filenames.
    """
    user_id = update.effective_user.id
    if user_id not in user_sequences or not user_sequences[user_id]:
        update.message.reply_text("No sequence to end. Use /startsequence first.")
        return

    files = user_sequences.pop(user_id)  # Retrieve and remove the user's file sequence
    update.message.reply_text(f"Sending your {len(files)} sequenced files now...")

    for file_info in files:
        try:
            # Send document with original filename
            context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_info["file_id"],
                filename=file_info["file_name"],  # This ensures the original filename is used
                caption=file_info.get("caption"),
                caption_entities=file_info.get("caption_entities")
            )
            logger.info(f"Sent file {file_info['file_name']} with caption: {file_info.get('caption')}")
        except Exception as e:
            update.message.reply_text(f"Failed to send file {file_info['file_name']}: {e}")
            logger.error(f"Failed to send file {file_info['file_name']}: {e}")

# Handler for the /endsequence command
end_sequence_handler = CommandHandler("endsequence", end_sequence)
