"""
BSD 2-Clause License

Copyright (C) 2017-2019, Paul Larsen
Copyright (C) 2021-2022, Awesome-RJ, [ https://github.com/Awesome-RJ ]
Copyright (c) 2021-2022, Yūki • Black Knights Union, [ https://github.com/Awesome-RJ/CutiepiiRobot ]

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import random

from telegram import ParseMode
from telethon import Button

from Madara import OWNER_ID, SUPPORT_CHAT
from Madara import telethn as tbot

from ..events import register


@register(pattern="/feedback ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    HOTTIE = (
        "https://telegra.ph/file/2fc46a598084cb1b305ae.jpg",
        "https://telegra.ph/file/85bc2e49966a58ce001a7.jpg",
        "https://telegra.ph/file/fe2fb3807437c7955442f.jpg",
        "https://telegra.ph/file/f1bbdb337914f76434503.jpg",
        "https://telegra.ph/file/082cd8a4eccca6b93e0cb.jpg",
        "https://telegra.ph/file/bb061e8fc2a4ebee496d7.jpg",
        "https://telegra.ph/file/c77483b0061e01342ab75.jpg",
    )
    FEED = ("https://telegra.ph/file/c30e6b78b571e7d63724e.jpg", )
    BUTTON = [[
        Button.url("Go To Support Group", f"https://t.me/{SUPPORT_CHAT}")
    ]]
    TEXT = "Thanks For Your Feedback, I Hope You Happy With Our Service"
    GIVE = "Give Some Text For Feedback ✨"
    logger_text = f"""
**New Feedback**
**From User:** {mention}
**Username:** @{e.sender.username}
**User ID:** `{e.sender.id}`
**Feedback:** `{e.text}`
"""
    if user_id == 1926801217:
        await e.reply("**Sry I Can't Identify ur Info**",
                      parse_mode=ParseMode.MARKDOWN)
        return

    if user_id == 1087968824:
        await e.reply("**Turn Off Ur Anonymous Mode And Try**",
                      parse_mode=ParseMode.MARKDOWN)
        return

    if e.sender_id != OWNER_ID and not quew:
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=random.choice(FEED),
        ),
        return

    await tbot.send_message(
        SUPPORT_CHAT,
        f"{logger_text}",
        file=random.choice(HOTTIE),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(HOTTIE), buttons=BUTTON)

__mod_name__ = "𝗙𝗘𝗘𝗗𝗕𝗔𝗖𝗞"
__help__ = """
⍟ /feedback : ʏᴏᴜ ᴄᴀɴ ɢɪᴠᴇ ғᴇᴇᴅʙᴀᴄᴋ.
"""
