import os
import psutil
import platform
import time
import shutil
import logging
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import API_ID, API_HASH, BOT_TOKEN
from yt import download_youtube_video

# Enable logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Start time for uptime calculation
START_TIME = time.time()
BOT_VERSION = "1.0 {α}"

# Initialize bot
app = Client("ftm_tubefetch", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ /start Command
@app.on_message(filters.command("start"))
async def start(client, message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id

    welcome_text = f"""🚩 जय श्री राम

ʜᴇʏ {user_name}, {user_id}

ɪ ᴀᴍ ᴛʜᴇ ᴏꜰꜰɪᴄɪᴀʟ ʙᴏᴛ ᴏꜰ **Fᴛᴍ TᴜʙᴇFᴇᴛᴄʜ** 📥  
ᴄʀᴇᴀᴛᴇᴅ ʙʏ **Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ** 🚀  
ᴜꜱᴇ ᴍᴇ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʜɪɢʜ-ꜱᴘᴇᴇᴅ 🎬 ᴠɪᴅᴇᴏꜱ & ᴀᴜᴅɪᴏꜱ ꜰʀᴏᴍ YᴏᴜTᴜʙᴇ 🚀"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Stats", callback_data="stats"),
         InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("❓ Help", callback_data="help"),
         InlineKeyboardButton("👨‍💻 Contact Developer", url="https://t.me/ftmdeveloperz")]
    ])

    await message.reply_text(welcome_text, reply_markup=keyboard, disable_web_page_preview=True)

# ✅ /stats Command (Bot Statistics)
@app.on_message(filters.command("stats"))
async def stats(client, message):
    uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - START_TIME))
    total, used, free = shutil.disk_usage("/")
    
    stats_text = (
        f"<b>╭「 💠 MY STATISTICS 」</b>\n"
        f"<b>├⏳ Uptime : {uptime}</b>\n"
        f"<b>├💾 Total Space : {total // (2**30)} GB</b>\n"
        f"<b>├📀 Used Space : {used // (2**30)} GB</b>\n"
        f"<b>├💿 Free Space : {free // (2**30)} GB</b>\n"
        f"<b>├🖥 CPU : {psutil.cpu_percent()}%</b>\n"
        f"<b>├⚙️ RAM : {psutil.virtual_memory().percent}%</b>\n"
        f"<b>├🔧 OS : {platform.system()} {platform.release()}</b>\n"
        f"<b>╰🚀 Version : {BOT_VERSION}</b>"
    )

    await message.reply_text(stats_text, parse_mode="html")

# ✅ Handle YouTube Video Link
@app.on_message(filters.text)
async def receive_video_url(client, message):
    video_url = message.text

    if "youtube.com" in video_url or "youtu.be" in video_url:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔹 MP4 1080p", callback_data=f"download|{video_url}|137"),
             InlineKeyboardButton("🔸 MP4 720p", callback_data=f"download|{video_url}|22")],
            [InlineKeyboardButton("🎵 MP3 320kbps", callback_data=f"download|{video_url}|bestaudio"),
             InlineKeyboardButton("🎵 MP3 128kbps", callback_data=f"download|{video_url}|140")]
        ])
        await message.reply_text("📥 Choose a format:", reply_markup=keyboard)
    else:
        await message.reply_text("❌ Invalid YouTube URL. Please send a valid link.")

# ✅ Handle Download Requests with Progress Bar
@app.on_callback_query(filters.regex("^download"))
async def handle_download_callback(client, callback_query: CallbackQuery):
    data = callback_query.data.split("|")
    video_url = data[1]
    format_code = data[2]

    progress_msg = await callback_query.message.edit_text("📥 Downloading... Please wait.")

    try:
        file_path = download_youtube_video(video_url, format_code)
        await callback_query.message.reply_video(video=file_path, caption="🎬 **Download Complete!** ✅")
        os.remove(file_path)  # Clean up after sending

    except Exception as e:
        await callback_query.message.reply_text(f"❌ Error: {e}")

# ✅ Run the bot
if __name__ == "__main__":
    app.run()
