from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

# In-memory storage for user file sequences
user_sequences = {}

def start_sequence(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_sequences[user_id] = []
    update.message.reply_text(
        "ʏᴏᴜ'ᴠᴇ ꜱᴛᴀʀᴛᴇᴅ ᴀ ꜰɪʟᴇ ꜱᴇǫᴜᴇɴᴄɪɴɢ ᴘʀᴏᴄᴇꜱꜱ. ꜱᴇɴᴅ ᴛʜᴇ ꜰɪʟᴇꜱ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ꜱᴇǫᴜᴇɴᴄᴇ ᴏɴᴇ ʙʏ ᴏɴᴇ.\n\n"
        "ᴡʜᴇɴ ʏᴏᴜ'ʀᴇ ᴅᴏɴᴇ, ᴜꜱᴇ /endsequence ᴛᴏ ꜰɪɴɪꜱʜ ᴀɴᴅ ɢᴇᴛ ᴛʜᴇ ꜱᴇǫᴜᴇɴᴄᴇᴅ ꜰɪʟᴇꜱ."
    )

def handle_file(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in user_sequences:
        update.message.reply_text("Please start a sequence using /startsequence first.")
        return

    file = update.message.document
    caption = update.message.caption  # Can be None
    caption_entities = update.message.caption_entities  # Can be None

    if file:
        user_sequences[user_id].append({
            "file_id": file.file_id,
            "file_name": file.file_name,
            "caption": caption,
            "caption_entities": caption_entities
        })
        print(f"Stored file: {file.file_name} with caption: {caption}")
        update.message.reply_text(f"File added to sequence: {file.file_name}")
    else:
        update.message.reply_text("Please send a valid file.")

def end_sequence(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in user_sequences or not user_sequences[user_id]:
        update.message.reply_text("No sequence to end. Use /startsequence first.")
        return

    files = user_sequences.pop(user_id)

    update.message.reply_text("Sending your sequenced files now...")

    for file_info in files:
        print(f"Sending file: {file_info['file_name']} with caption: {file_info.get('caption')}")
        try:
            update.message.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_info["file_id"],
                filename=file_info["file_name"],
                caption=file_info.get("caption"),
                caption_entities=file_info.get("caption_entities")
            )
        except Exception as e:
            update.message.reply_text(f"Failed to send file {file_info['file_name']}: {e}")

# Handlers to register in dispatcher
start_sequence = CommandHandler("startsequence", start_sequence)
end_sequence = CommandHandler("endsequence", end_sequence)
handle_file = MessageHandler(Filters.document, handle_file)
