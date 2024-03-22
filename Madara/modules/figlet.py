from pyrogram import filters
import asyncio
import pyfiglet 
from random import choice
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.handlers import MessageHandler
from .. import pgram
def figle(text):
    x = pyfiglet.FigletFont.getFonts()
    font = choice(x)
    figled = str(pyfiglet.figlet_format(text,font=font))
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="ᴄʜᴀɴɢᴇ", callback_data="figlet"),InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close_reply")]])
    return figled, keyboard

@pgram.on_message(filters.command("figlet"))
async def echo(bot, message):
    global text
    try:
        text = message.text.split(' ',1)[1]
    except IndexError:
        return await message.reply_text("❍ ᴇxᴀᴍᴘʟᴇ ➛ /figlet ʀᴏʏ-ᴇᴅɪᴛx")
    kul_text, keyboard = figle(text)
    await message.reply_text(f"❍ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ғɪɢʟᴇᴛ ➛\n<pre>{kul_text}</pre>", quote=True, reply_markup=keyboard)

@pgram.on_callback_query(filters.regex("figlet"))
async def figlet_handler(Client, query: CallbackQuery):
  try:
      kul_text, keyboard = figle(text)
      await query.message.edit_text(f"❍ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ғɪɢʟᴇᴛ ➛\n<pre>{kul_text}</pre>", reply_markup=keyboard)
  except Exception as e : 
      await message.reply(e)
__mod_name__ = "𝗙𝗜𝗚𝗟𝗘𝗧" 
__help__="""
» /figlet* ➛* ᴍᴀᴋᴇs ғɪɢʟᴇᴛ ᴏғ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ
» ᴇxᴀᴍᴘʟᴇ ➛ /figlet Shikimori"""
