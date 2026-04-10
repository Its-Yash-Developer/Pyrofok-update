import asyncio
import os
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaVideo
from pymediainfo import MediaInfo

api_id = 1234567  # Replace with your API ID
api_hash = "your_api_hash"  # Replace with your API Hash
bot_token = "your_bot_token"  # Replace with your bot token

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

async def create_cover_and_thumb(video_path):
    cover_path = f"{video_path}_cover.jpg"
    thumb_path = f"{video_path}_thumb.jpg"

    # Simple logic using ffmpeg
    try:
        media_info = MediaInfo.parse(video_path)
        duration_s = 0
        for track in media_info.tracks:
            if track.track_type == "Video":
                duration_s = track.duration / 1000.0
                break

        target_time = max(0, duration_s * 0.3)

        # Extract frame for cover
        os.system(f"ffmpeg -y -ss {target_time} -i '{video_path}' -vframes 1 '{cover_path}'")

        # Extract frame and resize for thumb (max 320x320)
        os.system(f"ffmpeg -y -i '{cover_path}' -vf \"scale='min(320,iw)':'min(320,ih)'\" '{thumb_path}'")

        return cover_path, thumb_path
    except Exception as e:
        print(f"Failed to extract cover/thumb: {e}")
        return None, None

@app.on_message(filters.video & ~filters.media_group)
async def handle_single_video(client, message: Message):
    msg = await message.reply("Downloading video...")
    video_path = await message.download()

    await msg.edit("Creating cover and thumb...")
    cover_path, thumb_path = await create_cover_and_thumb(video_path)

    if cover_path and thumb_path:
        await msg.edit("Uploading video with cover...")
        await message.reply_video(
            video=video_path,
            cover=cover_path,
            thumb=thumb_path,
            caption="Here is your video with a custom cover!"
        )
    else:
        await msg.edit("Failed to process video.")

    if os.path.exists(video_path): os.remove(video_path)
    if cover_path and os.path.exists(cover_path): os.remove(cover_path)
    if thumb_path and os.path.exists(thumb_path): os.remove(thumb_path)

@app.on_message(filters.media_group)
async def handle_media_group(client, message: Message):
    msg = await message.reply("Processing media group...")

    media_group = await message.get_media_group()

    input_medias = []
    files_to_delete = []

    for item in media_group:
        if item.video:
            video_path = await item.download()
            files_to_delete.append(video_path)

            cover_path, thumb_path = await create_cover_and_thumb(video_path)
            if cover_path and thumb_path:
                files_to_delete.extend([cover_path, thumb_path])

                input_medias.append(
                    InputMediaVideo(
                        media=video_path,
                        cover=cover_path,
                        thumb=thumb_path,
                        caption="Video with custom cover in album!"
                    )
                )

    if input_medias:
        await msg.edit("Uploading media group with covers...")
        await message.reply_media_group(media=input_medias)
    else:
        await msg.edit("No videos could be processed in the group.")

    for f in files_to_delete:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    app.run()
