from pyrogram import Client, filters
from pyrogram.types import Message

# Replace with your own API ID and API HASH
API_ID = 12345
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Global variable to store the cover file_id
COVER_FILE_ID = None

@app.on_message(filters.photo)
async def handle_photo(client: Client, message: Message):
    global COVER_FILE_ID
    # Get the file_id of the largest photo variant
    COVER_FILE_ID = message.photo.file_id
    await message.reply_text(f"Cover photo saved! File ID: {COVER_FILE_ID}")

@app.on_message(filters.video)
async def handle_video(client: Client, message: Message):
    global COVER_FILE_ID

    video_file_id = message.video.file_id

    if COVER_FILE_ID:
        await message.reply_text("Sending video with the saved cover...")
        # Send the video using its file_id and the stored cover file_id
        await client.send_video(
            chat_id=message.chat.id,
            video=video_file_id,
            cover=COVER_FILE_ID,
            caption="Here is your video with the custom cover!"
        )
    else:
        await message.reply_text("Please send a photo first to set it as a cover.")

if __name__ == "__main__":
    app.run()
