from pyrogram import Client, filters
import requests
from Madara import pgram
import Madara
from Madara import *

app = pbot

@pgram.on_message(filters.command("reel"))
async def download_instagram_reel(client, message):
    try:
        if len(message.text.split(" ")) == 1:
            await message.reply_text("Please provide an Instagram link after the command.")
            return
        
        url = message.text.split(" ", 1)[1]
        response = requests.post(f"https://api.qewertyy.dev/download/instagram?url={url}")
        
        if response.status_code == 200:
            data = response.json()
            if "content" in data and len(data["content"]) > 0:
                video_url = data["content"][0]["url"]
                await message.reply_video(video_url)
            else:
                await message.reply_text("No content found in the response.")
        else:
            await message.reply_text(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        await message.reply_text(f"Something went wrong: {e}")

__mod_name__ = "𝗥𝗘𝗘𝗟"
__help__ = """
⍟ /reel : ʏᴏᴜ ᴄᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴀ ʀᴇᴇʟ.
 """
