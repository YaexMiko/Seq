from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
import logging

logger = logging.getLogger(__name__)

# In-memory storage for user file sequences
user_sequences = {}

def start_sequence(update: Update, context: CallbackContext):
    """
    Initializes a new file sequencing process for the user with enhanced feedback.
    """
    user_id = update.effective_user.id
    
    # Check if user already has a sequence in progress
    if user_id in user_sequences:
        update.message.reply_text(
            "*⚠️ Sequence Already In Progress!*\n\n"
            "You already have an active file sequence.\n\n"
            "• Continue sending files\n"
            "• Or use /endsequence to finish\n"
            "• Use /cancelsequence to discard",
            parse_mode="Markdown"
        )
        return
    
    # Initialize new sequence
    user_sequences[user_id] = []
    update.message.reply_text(
        "📂 *NEW FILE SEQUENCE STARTED* 📂\n\n"
        "Now you can send me files one by one:\n"
        "• Documents\n"
        "• Images with captions\n"
        "• Any supported file types\n\n"
        "*Commands:*\n"
        "/endsequence - Finish and get your files\n"
        "/cancelsequence - Discard current sequence\n\n"
        "All captions will be formatted in *bold* when you finish.",
        parse_mode="Markdown"
    )
    logger.info(f"User {user_id} started a new file sequence.")

def cancel_sequence(update: Update, context: CallbackContext):
    """
    Cancels the current file sequence and clears stored files.
    """
    user_id = update.effective_user.id
    if user_id in user_sequences:
        file_count = len(user_sequences[user_id])
        del user_sequences[user_id]
        update.message.reply_text(
            f"*🗑 Sequence Cancelled*\n\n"
            f"Removed {file_count} files from your sequence.",
            parse_mode="Markdown"
        )
        logger.info(f"User {user_id} cancelled their sequence with {file_count} files")
    else:
        update.message.reply_text(
            "*No active sequence to cancel.*\n"
            "Use /startsequence to begin a new one.",
            parse_mode="Markdown"
        )

def handle_file(update: Update, context: CallbackContext):
    """
    Adds a file to the user's current file sequence with improved validation.
    """
    user_id = update.effective_user.id
    if user_id not in user_sequences:
        update.message.reply_text(
            "*Please start a sequence first!*\n\n"
            "Use /startsequence to begin collecting files.",
            parse_mode="Markdown"
        )
        return

    file = update.message.document or update.message.photo and update.message.photo[-1]
    caption = update.message.caption
    caption_entities = update.message.caption_entities

    if not file:
        update.message.reply_text(
            "*Please send a valid file.*\n"
            "Supported types: documents, images, etc.",
            parse_mode="Markdown"
        )
        return

    # Get appropriate file attributes based on type
    if update.message.document:
        file_id = file.file_id
        file_name = file.file_name or f"document_{len(user_sequences[user_id]) + 1}"
    else:  # photo
        file_id = file.file_id
        file_name = f"image_{len(user_sequences[user_id]) + 1}.jpg"

    user_sequences[user_id].append({
        "file_id": file_id,
        "file_name": file_name,
        "caption": caption,
        "caption_entities": caption_entities
    })
    
    update.message.reply_text(
        f"*✅ Added to sequence:* {file_name}\n"
        f"*Total files:* {len(user_sequences[user_id])}",
        parse_mode="Markdown"
    )
    logger.info(f"User {user_id} added file {file_name} to sequence")

def end_sequence(update: Update, context: CallbackContext):
    """
    Ends the file sequencing process and sends back the sequenced files with bold formatting.
    """
    user_id = update.effective_user.id
    if user_id not in user_sequences or not user_sequences[user_id]:
        update.message.reply_text(
            "*No sequence to end!*\n\n"
            "Use /startsequence to begin a new file collection.",
            parse_mode="Markdown"
        )
        return

    files = user_sequences.pop(user_id)
    update.message.reply_text(
        f"*📦 Preparing your {len(files)} files...*\n"
        "All captions will be in *bold* format.",
        parse_mode="Markdown"
    )

    for file_info in files:
        try:
            bold_caption = f"*{file_info['caption']}*" if file_info.get('caption') else None
            
            context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_info["file_id"],
                filename=file_info["file_name"],
                caption=bold_caption,
                caption_entities=file_info.get("caption_entities"),
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Failed to send file {file_info['file_name']}: {e}")
            update.message.reply_text(
                f"*Failed to send {file_info['file_name']}*\n"
                f"Error: {str(e)}",
                parse_mode="Markdown"
            )

    update.message.reply_text(
        "*✅ Sequence completed successfully!*\n\n"
        "Use /startsequence to begin a new collection.",
        parse_mode="Markdown"
    )

# Register handlers
start_sequence_handler = CommandHandler("startsequence", start_sequence)
end_sequence_handler = CommandHandler("endsequence", end_sequence)
cancel_sequence_handler = CommandHandler("cancelsequence", cancel_sequence)
handle_file_handler = MessageHandler(
    Filters.document | Filters.photo, 
    handle_file
)
