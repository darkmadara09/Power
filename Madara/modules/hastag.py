import requests
from bs4 import BeautifulSoup as  BSP
from Madara import pgram
from pyrogram import filters
url = "https://all-hashtag.com/library/contents/ajax_generator.php"

@pgram.on_message(filters.command("hastag"))
async def hastag(bot, message):
    global content
    try:
        text = message.text.split(' ',1)[1]
        data = dict(keyword=text, filter="top")

        res = requests.post(url, data).text

        content = BSP(res, 'html.parser').find("div", {"class":"copy-hashtags"}).string
    except IndexError:
        return await message.reply_text("Example:\n\n/hastag python")
        
    
    await message.reply_text(f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ  ʜᴀsᴛᴀɢ :\n<pre>{content}</pre>", quote=True)
    
__mod_name__ = "𝗛𝗔𝗦𝗛𝗧𝗔𝗚"
__help__ = """
Yᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʜᴀsʜᴛᴀɢ ɢᴇɴᴇʀᴀᴛᴏʀ ᴡʜɪᴄʜ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴛʜᴇ ᴛᴏᴘ 𝟹𝟶 ᴀɴᴅ ᴍᴏʀᴇ ʜᴀsʜᴛᴀɢs ʙᴀsᴇᴅ ᴏғғ ᴏғ ᴏɴᴇ ᴋᴇʏᴡᴏʀᴅ sᴇʟᴇᴄᴛɪᴏɴ.
⍟ /hastag ᴇɴᴛᴇʀ ᴡᴏʀᴋ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ʜᴀsʜᴛᴀɢ.
⍟ Exᴀᴍᴘʟᴇ:  /hastag ᴘʏᴛʜᴏɴ """
