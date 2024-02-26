import html
from datetime import timedelta
from typing import Optional

from pytimeparse.timeparse import timeparse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

import Madara.modules.sql.welcome_sql as sql
from Madara import LOGGER, updater
from Madara.modules.helper_funcs.anonymous import AdminPerms, user_admin
from Madara.modules.helper_funcs.chat_status import (
    bot_admin,
    connection_status,
    user_admin_no_reply,
)
from Madara.modules.helper_funcs.decorators import Madaracallback, Madaracmd
from Madara.modules.log_channel import loggable

j = updater.job_queue

# store job id in a dict to be able to cancel them later
RUNNING_RAIDS = {}  # {chat_id:job_id, ...}


def get_time(time: str) -> int:
    try:
        return timeparse(time)
    except BaseException:
        return 0


def get_readable_time(time: int) -> str:
    t = f"{timedelta(seconds=time)}".split(":")
    if time == 86400:
        return "1 day"
    return f"{t[0]} hour(s)" if time >= 3600 else f"{t[1]} minutes"


@Madaracmd(command="raid", pass_args=True)
@bot_admin
@connection_status
@loggable
@user_admin(AdminPerms.CAN_CHANGE_INFO)
def setRaid(update: Update, context: CallbackContext) -> Optional[str]:
    args = context.args
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if chat.type == "private":
        context.bot.sendMessage(chat.id, "This ᴄᴏᴍᴍᴀɴᴅ is not available in PMs.")
        return
    stat, time, acttime = sql.getRaidStatus(chat.id)
    readable_time = get_readable_time(time)
    if len(args) == 0:
        if stat:
            text = "ʀᴀɪᴅ ᴍᴏᴅᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ <code>ᴇɴᴀʙʟᴇᴅ</code>\nᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ <code>ᴅɪsᴀʙʟᴇ</code> raid?"
            keyboard = [
                [
                    InlineKeyboardButton(
                        "ᴅɪsᴀʙʟᴇ ʀᴀɪᴅ ᴍᴏᴅᴇ",
                        callback_data=f"disable_raid={chat.id}={time}",
                    ),
                    InlineKeyboardButton(
                        "ᴄᴀɴᴄᴇʟ ᴀᴄᴛɪᴏɴ", callback_data="cancel_raid=1"
                    ),
                ]
            ]

        else:
            text = (
                f"ʀᴀɪᴅ ᴍᴏᴅᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ <code>ᴅɪsᴀʙʟᴇᴅ</code>\nᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ <code>ᴇɴᴀʙʟᴇ</code> "
                f"ʀᴀɪᴅ ғᴏʀ {readable_time}?"
            )
            keyboard = [
                [
                    InlineKeyboardButton(
                        "ᴇɴᴀʙʟᴇ ʀᴀɪᴅ ᴍᴏᴅᴇ",
                        callback_data=f"enable_raid={chat.id}={time}",
                    ),
                    InlineKeyboardButton(
                        "ᴄᴀɴᴄᴇʟ ᴀᴄᴛɪᴏɴ", callback_data="cancel_raid=0"
                    ),
                ]
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        msg.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

    elif args[0] == "off":
        if stat:
            sql.setRaidStatus(chat.id, False, time, acttime)
            j.scheduler.remove_job(RUNNING_RAIDS.pop(chat.id))
            text = "ʀᴀɪᴅ ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ <code>Disabled</code>, ᴍᴇᴍʙᴇʀs ᴛʜᴀᴛ ᴊᴏɪɴ ᴡɪʟʟ ɴᴏ ʟᴏɴɢᴇʀ ʙᴇ ᴋɪᴄᴋᴇᴅ."
            msg.reply_text(text, parse_mode=ParseMode.HTML)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#ʀᴀɪᴅ\n"
                f"ᴅɪsᴀʙʟᴇᴅ\n"
                f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
            )

    else:
        args_time = args[0].lower()
        if time := get_time(args_time):
            readable_time = get_readable_time(time)
            if 300 <= time < 86400:
                text = (
                    f"ʀᴀɪᴅ ᴍᴏᴅᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ <code>ᴅɪsᴀʙʟᴇᴅ</code>\nᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ <code>Enable</code> "
                    f"ʀᴀɪᴅ ғᴏʀ {readable_time}? "
                )
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "ᴇɴᴀʙʟᴇ ʀᴀɪᴅ",
                            callback_data=f"enable_raid={chat.id}={time}",
                        ),
                        InlineKeyboardButton(
                            "ᴄᴀɴᴄᴇʟ ᴀᴄᴛɪᴏɴ", callback_data="cancel_raid=0"
                        ),
                    ]
                ]

                reply_markup = InlineKeyboardMarkup(keyboard)
                msg.reply_text(
                    text, parse_mode=ParseMode.HTML, reply_markup=reply_markup
                )
            else:
                msg.reply_text(
                    "ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ sᴇᴛ ᴛɪᴍᴇ ʙᴇᴛᴡᴇᴇɴ 5 ᴍɪɴᴜᴛᴇs ᴀɴᴅ 1 ᴅᴀʏ",
                    parse_mode=ParseMode.HTML,
                )

        else:
            msg.reply_text(
                "ᴜɴᴋɴᴏᴡɴ ᴛɪᴍᴇ ɢɪᴠᴇɴ, ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇᴛʜɪɴɢ ʟɪᴋᴇ 5m ᴏʀ 1h",
                parse_mode=ParseMode.HTML,
            )


@Madaracallback(pattern="enable_raid=")
@connection_status
@user_admin_no_reply
@loggable
def enable_raid_cb(update: Update, ctx: CallbackContext) -> Optional[str]:
    args = update.callback_query.data.replace("enable_raid=", "").split("=")
    chat = update.effective_chat
    user = update.effective_user
    chat_id = args[0]
    time = int(args[1])
    readable_time = get_readable_time(time)
    _, t, acttime = sql.getRaidStatus(chat_id)
    sql.setRaidStatus(chat_id, True, time, acttime)
    update.effective_message.edit_text(
        f"ʀᴀɪᴅ ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ <code>ᴇɴᴀʙʟᴇᴅ</code> ғᴏʀ {readable_time}.",
        parse_mode=ParseMode.HTML,
    )
    LOGGER.info("ᴇɴᴀʙʟᴇᴅ ʀᴀɪᴅ ᴍᴏᴅᴇ ɪɴ {} for {}".format(chat_id, readable_time))
    try:
        oldRaid = RUNNING_RAIDS.pop(int(chat_id))
        j.scheduler.remove_job(oldRaid)  # check if there was an old job
    except KeyError:
        pass

    def disable_raid(_):
        sql.setRaidStatus(chat_id, False, t, acttime)
        LOGGER.info("ᴅɪsʙʟᴇᴅ ʀᴀɪᴅ ᴍᴏᴅᴇ ɪɴ {}".format(chat_id))
        ctx.bot.send_message(chat_id, "ʀᴀɪᴅ ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅɪsᴀʙʟᴇᴅ!")

    raid = j.run_once(disable_raid, time)
    RUNNING_RAIDS[int(chat_id)] = raid.job.id
    return (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#ʀᴀɪᴅ\n"
        f"ᴇɴᴀʙʟᴇᴅ ғᴏʀ {readable_time}\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
    )


@Madaracallback(pattern="disable_raid=")
@connection_status
@user_admin_no_reply
@loggable
def disable_raid_cb(update: Update, _: CallbackContext) -> Optional[str]:
    args = update.callback_query.data.replace("disable_raid=", "").split("=")
    chat = update.effective_chat
    user = update.effective_user
    chat_id = args[0]
    time = args[1]
    _, _, acttime = sql.getRaidStatus(chat_id)
    sql.setRaidStatus(chat_id, False, time, acttime)
    j.scheduler.remove_job(RUNNING_RAIDS.pop(int(chat_id)))
    update.effective_message.edit_text(
        "ʀᴀɪᴅ ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ <code>ᴅɪsᴀʙʟᴇᴅ</code>, ɴᴇᴡʟʏ ᴊᴏɪɴɪɴɢ ᴍᴇᴍʙᴇʀs ᴡɪʟʟ ɴᴏ ʟᴏɴɢᴇʀ ʙᴇ ᴋɪᴄᴋᴇᴅ.",
        parse_mode=ParseMode.HTML,
    )
    logmsg = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#ʀᴀɪᴅ\n"
        f"ᴅɪsᴀʙʟᴇᴅ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
    )
    return logmsg


@Madaracallback(pattern="cancel_raid=")
@connection_status
@user_admin_no_reply
def disable_raid_cb(update: Update, _: CallbackContext):
    args = update.callback_query.data.split("=")
    what = args[0]
    update.effective_message.edit_text(
        f"ᴀᴄᴛɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ, ʀᴀɪᴅ ᴍᴏᴅᴇ ᴡɪʟʟ sᴛᴀʏ <code>{'Enabled' if what == 1 else 'Disabled'}</code>.",
        parse_mode=ParseMode.HTML,
    )


@Madaracmd(command="raidtime")
@connection_status
@loggable
@user_admin(AdminPerms.CAN_CHANGE_INFO)
def raidtime(update: Update, context: CallbackContext) -> Optional[str]:
    what, time, acttime = sql.getRaidStatus(update.effective_chat.id)
    args = context.args
    msg = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    if not args:
        msg.reply_text(
            f"ʀᴀɪᴅ ᴍᴏᴅᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ ᴛᴏ {get_readable_time(time)}\nᴡʜᴇɴ ᴛᴏɢɢʟᴇᴅ, ᴛʜᴇ ʀᴀɪᴅ ᴍᴏᴅᴇ ᴡɪʟʟ ʟᴀsᴛ "
            f"ғᴏʀ {get_readable_time(time)} ᴛʜᴇɴ ᴛᴜʀɴ ᴏғғ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ",
            parse_mode=ParseMode.HTML,
        )
        return
    args_time = args[0].lower()
    if time := get_time(args_time):
        readable_time = get_readable_time(time)
        if 300 <= time < 86400:
            text = (
                f"ʀᴀɪᴅ ᴍᴏᴅᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ ᴛᴏ {readable_time}\nᴡʜᴇɴ ᴛᴏɢɢʟᴇᴅ, ᴛʜᴇ ʀᴀɪᴅ ᴍᴏᴅᴇ ᴡɪʟʟ ʟᴀsᴛ ғᴏʀ "
                f"{readable_time} ᴛʜᴇɴ ᴛᴜʀɴ ᴏғғ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ"
            )
            msg.reply_text(text, parse_mode=ParseMode.HTML)
            sql.setRaidStatus(chat.id, what, time, acttime)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#ʀᴀɪᴅ\n"
                f"sᴇᴛ ʀᴀɪᴅ ᴍᴏᴅᴇ ᴛɪᴍᴇ ᴛᴏ {readable_time}\n"
                f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
            )
        else:
            msg.reply_text(
                "ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ sᴇᴛ ᴛɪᴍᴇ ʙᴇᴛᴡᴇᴇɴ 5 ᴍɪɴᴜᴛᴇs ᴀɴᴅ 1 ᴅᴀʏ",
                parse_mode=ParseMode.HTML,
            )
    else:
        msg.reply_text(
            "ᴜɴᴋɴᴏᴡɴ ᴛɪᴍᴇ ɢɪᴠᴇɴ, ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇᴛʜɪɴɢ ʟɪᴋᴇ 5ᴍ ᴏʀ 1ʜ",
            parse_mode=ParseMode.HTML,
        )


@Madaracmd(command="raidactiontime", pass_args=True)
@connection_status
@user_admin(AdminPerms.CAN_CHANGE_INFO)
@loggable
def raidtime(update: Update, context: CallbackContext) -> Optional[str]:
    what, t, time = sql.getRaidStatus(update.effective_chat.id)
    args = context.args
    msg = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    if not args:
        msg.reply_text(
            f"ʀᴀɪᴅ ᴀᴄᴛɪᴏɴ ᴛɪᴍᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ ᴛᴏ {get_readable_time(time)}\nᴡʜᴇɴ ᴛᴏɢɢʟᴇᴅ, ᴛʜᴇ ᴍᴇᴍʙᴇʀs ᴛʜᴀᴛ "
            f"ᴊᴏɪɴ ᴡɪʟʟ ʙᴇ ᴛᴇᴍᴘ ʙᴀɴɴᴇᴅ ғᴏʀ {get_readable_time(time)}",
            parse_mode=ParseMode.HTML,
        )
        return
    args_time = args[0].lower()
    if time := get_time(args_time):
        readable_time = get_readable_time(time)
        if 300 <= time < 86400:
            text = (
                f"ʀᴀɪᴅ ᴀᴄᴛɪᴏɴ ᴛɪᴍᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ ᴛᴏ {get_readable_time(time)}\nᴡʜᴇɴ ᴛᴏɢɢʟᴇᴅ, ᴛʜᴇ ᴍᴇᴍʙᴇʀs ᴛʜᴀᴛ"
                f" ᴊᴏɪɴ ᴡɪʟʟ ʙᴇ ᴛᴇᴍᴘ ʙᴀɴɴᴇᴅ ғᴏʀ {readable_time}"
            )
            msg.reply_text(text, parse_mode=ParseMode.HTML)
            sql.setRaidStatus(chat.id, what, t, time)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#ʀᴀɪᴅ\n"
                f"sᴇᴛ ʀᴀɪᴅ ᴍᴏᴅᴇ ᴀᴄᴛɪᴏɴ ᴛɪᴍᴇ ᴛᴏ {readable_time}\n"
                f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            )
        else:
            msg.reply_text(
                "ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ sᴇᴛ ᴛɪᴍᴇ ʙᴇᴛᴡᴇᴇɴ 5 ᴍɪɴᴜᴛᴇs ᴀɴᴅ 1 ᴅᴀʏ",
                parse_mode=ParseMode.HTML,
            )
    else:
        msg.reply_text(
            "ᴜɴᴋɴᴏᴡɴ ᴛɪᴍᴇ ɢɪᴠᴇɴ, ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇᴛʜɪɴɢ ʟɪᴋᴇ 5m ᴏʀ 1h",
            parse_mode=ParseMode.HTML,
        )


__help__ = """
ᴇᴠᴇʀ ʜᴀᴅ ʏᴏᴜʀ ɢʀᴏᴜᴘ ʀᴀɪᴅᴇᴅ ʙʏ sᴘᴀᴍᴍᴇʀs ᴏʀ ʙᴏᴛs?
ᴛʜɪs ᴍᴏᴅᴜʟᴇ ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ ǫᴜɪᴄᴋʟʏ sᴛᴏᴘ ᴛʜᴇ ʀᴀɪᴅᴇʀs
ʙʏ ᴇɴᴀʙʟɪɴɢ *ʀᴀɪᴅ ᴍᴏᴅᴇ* I ᴡɪʟʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴋɪᴄᴋ ᴇᴠᴇʀʏ ᴜsᴇʀ ᴛʜᴀᴛ ᴛʀɪᴇs ᴛᴏ ᴊᴏɪɴ
ᴡʜᴇɴ ᴛʜᴇ ʀᴀɪᴅ ɪs ᴅᴏɴᴇ ʏᴏᴜ ᴄᴀɴ ᴛᴏɢɢʟᴇ ʙᴀᴄᴋ ʟᴏᴄᴋɢʀᴏᴜᴘ ᴀɴᴅ ᴇᴠᴇʀʏᴛʜɪɴɢ ᴡɪʟʟ ʙᴇ ʙᴀᴄᴋ ᴛᴏ ɴᴏʀᴍᴀʟ.
  
*ᴀᴅᴍɪɴs ᴏɴʟʏ!* 

⍟ /raid `(off/time optional)` : `ᴛᴏɢɢʟᴇ ᴛʜᴇ ʀᴀɪᴅ ᴍᴏᴅᴇ (ᴏɴ/ᴏғғ `)

if ɴᴏ ᴛɪᴍᴇ is ɢɪᴠᴇɴ ɪᴛ ᴡɪʟʟ ᴅᴇғᴀᴜʟᴛ ᴛᴏ 2 ʜᴏᴜʀs ᴛʜᴇɴ ᴛᴜʀɴ ᴏғғ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ

ʙʏ ᴇɴᴀʙʟɪɴɢ *ʀᴀɪᴅ ᴍᴏᴅᴇ* ɪ ᴡɪʟʟ ᴋɪᴄᴋ ᴇᴠᴇʀʏ ᴜsᴇʀ ᴏɴ ᴊᴏɪɴɪɴɢ ᴛʜᴇ ɢʀᴏᴜᴘ


⍟ /raidtime `(time optional)` : `ᴠɪᴇᴡ ᴏʀ sᴇᴛ ᴛʜᴇ ᴅᴇғᴀᴜʟᴛ ᴅᴜʀᴀᴛɪᴏɴ ғᴏʀ raid ᴍᴏᴅᴇ, ᴀғᴛᴇʀ ᴛʜᴀᴛ ᴛɪᴍᴇ  ғʀᴏᴍ ᴛᴏɢɢʟɪɴɢ ᴛʜᴇ ʀᴀɪᴅ ᴍᴏᴅᴇ ᴡɪʟʟ ᴛᴜʀɴ ᴏғғ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇғᴀᴜʟᴛ ɪs 6 ʜᴏᴜʀs `


⍟ /raidactiontime `(ᴛɪᴍᴇ ᴏᴘᴛɪᴏɴᴀʟ)` : `ᴠɪᴇᴡ ᴏʀ sᴇᴛ ᴛʜᴇ ᴅᴇғᴀᴜʟᴛ ᴅᴜʀᴀᴛɪᴏɴ ᴛʜᴀᴛ ᴛʜᴇ ʀᴀɪᴅ ᴍᴏᴅᴇ ᴡɪʟʟ ᴛᴇᴍᴘʙᴀɴ
ᴅᴇғᴀᴜʟᴛ ɪs 1 ʜᴏᴜʀ `

"""

__mod_name__ = "𝗔𝗡𝗧𝗜-𝗥𝗔𝗜𝗗"
