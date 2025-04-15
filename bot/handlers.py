from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

# Dictionary to store user sequences
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
    if file:
        # Save file_id and file_name for sequencing
        user_sequences[user_id].append({
            "file_id": file.file_id,
            "file_name": file.file_name
        })
        update.message.reply_text(f"File added to sequence: {file.file_name}")
    else:
        update.message.reply_text("Please send a valid file.")

def end_sequence(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in user_sequences or not user_sequences[user_id]:
        update.message.reply_text("No sequence to end. Use /startsequence first.")
        return

    files = user_sequences.pop(user_id)

    # Format the list of files nicely
    file_list_text = "\n".join([f"{idx+1}. {f['file_name']}" for idx, f in enumerate(files)])

    update.message.reply_text(
        "Your file sequence is complete! Here are the files in order:\n\n" + file_list_text
    )

# Create handlers to be added in bot.py
start_sequence = CommandHandler("startsequence", start_sequence)
end_sequence = CommandHandler("endsequence", end_sequence)
handle_file = MessageHandler(Filters.document, handle_file)
