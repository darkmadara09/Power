from telegram import TelegramError, Update
from telegram.ext import CommandHandler
from telegram.ext.dispatcher import CallbackContext, run_async

from Madara import LOGGER, dispatcher
from Madara.modules.helper_funcs.filters import CustomFilters


@run_async
def snipe(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError:
        update.effective_message.reply_text("❍ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ ᴀ ᴄʜᴀᴛ ᴛᴏ ᴇᴄʜᴏ ᴛᴏ !")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("❍ ᴄᴏᴜʟᴅɴ'ᴛ sᴇɴᴅ ᴛᴏ ɢʀᴏᴜᴘ %s", str(chat_id))
            update.effective_message.reply_text(
                "❍ ᴄᴏᴜʟᴅɴ'ᴛ sᴇɴᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ. ᴘᴇʀʜᴀᴘs ɪ'ᴍ ɴᴏᴛ ᴘᴀʀᴛ ᴏғ ᴛʜᴀᴛ ɢʀᴏᴜᴘ ?"
            )


__help__ = """
✿ *ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴏɴʟʏ* ✿

❍ /snipe <ᴄʜᴀᴛɪᴅ> <sᴛʀɪɴɢ> ➛ ᴍᴀᴋᴇ ᴍᴇ sᴇɴᴅ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀ sᴘᴇᴄɪғɪᴄ ᴄʜᴀᴛ.
"""

__mod_name__ = "𝗦𝗡𝗜𝗣𝗘"

SNIPE_HANDLER = CommandHandler(
    "snipe", snipe, pass_args=True, filters=CustomFilters.dev_filter
)

dispatcher.add_handler(SNIPE_HANDLER)
