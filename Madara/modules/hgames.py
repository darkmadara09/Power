import random

from telethon import Button, events

from .. import telethn as asst

BUTTON = [[Button.url("ꜱᴜᴘᴘᴏʀᴛ", f"https://t.me/Muichiro_support")]]
HOT = "https://telegra.ph/file/daad931db960ea40c0fca.gif"
SMEXY = "https://telegra.ph/file/a23e9fd851fb6bc771686.gif"
LEZBIAN = "https://telegra.ph/file/5609b87f0bd461fc36acb.gif"
BIGBALL = "https://i.gifer.com/8ZUg.gif"
LANG = "https://telegra.ph/file/423414459345bf18310f5.gif"
CUTIE = "https://64.media.tumblr.com/d701f53eb5681e87a957a547980371d2/tumblr_nbjmdrQyje1qa94xto1_500.gif"
LESBIANX = "https://te.legra.ph/file/c77752d415a03cee9f67e.gif"
IQX = "https://te.legra.ph/file/96ff21a001d0de18e0e2c.gif"
DRUNKX = "https://te.legra.ph/file/bdf9c6b83a8f77fca7fd8.gif"
HAPPYX = "https://te.legra.ph/file/7c62329239e49545eff0a.gif"
DIPRESSIONX = "https://te.legra.ph/file/d796c4015a481d57ccea8.gif"
CHADX = "https://te.legra.ph/file/0bc901f8418b32f5d4e8e.gif"
GAYX = "https://te.legra.ph/file/d5f43f7319250ab1de3f4.gif"
SIGMAX = "https://te.legra.ph/file/c3cce554ce0b50db72403.gif"
BATMANX = "https://te.legra.ph/file/d51fd915432bfbe7a1bbe.gif"

@asst.on(events.NewMessage(pattern="/horny ?(.*)"))
async def horny(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    HORNY = f"**» ** {mention} **ɪꜱ** {mm}**% ʜᴏʀɴʏ !**"
    await e.reply(HORNY, buttons=BUTTON, file=HOT)


@asst.on(events.NewMessage(pattern="/gay ?(.*)"))
async def gay(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    GAY = f"**» ** {mention} **ɪꜱ** {mm}**% ɢᴀʏ !**"
    await e.reply(GAY, buttons=BUTTON, file=GAYX)


@asst.on(events.NewMessage(pattern="/lezbian ?(.*)"))
async def lezbian(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    FEK = f"**» ** {mention} **ɪꜱ** {mm}**% ʟᴇᴢʙɪᴀɴ !**"
    await e.reply(FEK, buttons=BUTTON, file=LEZBIAN)


@asst.on(events.NewMessage(pattern="/boob ?(.*)"))
async def boob(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    BOOBS = f"**» ** {mention}**'ꜱ ʙᴏᴏʙꜱ ꜱɪᴢᴇ ɪᴢ** {mm}** !**"
    await e.reply(BOOBS, buttons=BUTTON, file=BIGBALL)


@asst.on(events.NewMessage(pattern="/cock ?(.*)"))
async def cock(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    COCK = f"**» ** {mention}**'ꜱ ᴄᴏᴄᴋ ꜱɪᴢᴇ ɪᴢ** {mm}**ᴄᴍ !**"
    await e.reply(COCK, buttons=BUTTON, file=LANG)


@asst.on(events.NewMessage(pattern="/dull ?(.*)"))
async def cute(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    CUTE = f"**» ** {mention} {mm}**% ᴅᴜʟʟ !**"
    await e.reply(CUTE, buttons=BUTTON, file=CUTIE)


@asst.on(events.NewMessage(pattern="/lesbian ?(.*)"))
async def lezbian(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    LESBIAN = f"**» ** {mention} **ɪꜱ** {mm}**% ʟᴇsʙɪᴀɴ !**"
    await e.reply(FEK, buttons=BUTTON, file=LESBIANX)
    
    
@asst.on(events.NewMessage(pattern="/iq ?(.*)"))
async def lezbian(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    IQ = f"**» ** {mention} **ʜᴀs** {mm}**% ɪǫ ʟᴇᴠᴇʟ !**"
    await e.reply(FEK, buttons=BUTTON, file=IQX)
    
    
@asst.on(events.NewMessage(pattern="/drunk ?(.*)"))
async def lezbian(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    DRUNK = f"**» ** {mention} **ɪs** {mm}**% ᴅʀɪɴᴋɪɴɢ !**"
    await e.reply(FEK, buttons=BUTTON, file=DRUNKX)
    
    
@asst.on(events.NewMessage(pattern="/happy ?(.*)"))
async def lezbian(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    HAPPY = f"**» ** {mention} **ɪs** {mm}**% ʜᴀᴘᴘʏ !**"
    await e.reply(FEK, buttons=BUTTON, file=HAPPYX)
    
    
@asst.on(events.NewMessage(pattern="/depression ?(.*)"))
async def lezbian(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    DEPRESSION = f"**» ** {mention} **ɪs** {mm}**% ᴅɪᴘʀᴇssᴇᴅ !**"
    await e.reply(FEK, buttons=BUTTON, file=DIPRESSIONX)
    

@asst.on(events.NewMessage(pattern="/chad ?(.*)"))
async def lezbian(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    CHAD = f"**» ** {mention} **ɪs** {mm}**% ɢɪɢᴀ-ᴄʜᴀᴅ !**"
    await e.reply(FEK, buttons=BUTTON, file=CHADX)
    
    
@asst.on(events.NewMessage(pattern="/sigma ?(.*)"))
async def lezbian(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    SIGMA = f"**» ** {mention} **ɪs** {mm}**% sɪɢᴍᴀ !**"
    await e.reply(FEK, buttons=BUTTON, file=SIGMAX)
    
    
@asst.on(events.NewMessage(pattern="/batman ?(.*)"))
async def lezbian(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    BATMAN = f"**» ** {mention} **ɪs** {mm}**% ʙᴀᴛᴍᴀɴ !**"
    await e.reply(FEK, buttons=BUTTON, file=BATMANX)
    
    

__help__ = """
⍟ /horny ➛ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ʜᴏʀɴʏᴇꜱꜱ.

⍟ /gay ➛ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ɢᴜʏɴᴇꜱꜱ.

⍟ /lezbian ➛ ᴄʜᴇᴄᴋ ᴜʀ ᴄᴜʀʀᴇɴᴛ ʟᴀᴢʙɪᴀɴ.

⍟ /boob ➛ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ʙᴏᴏʙꜱ ꜱɪᴢᴇ.

⍟ /cock ➛ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴄᴏᴄᴋ sɪᴢᴇ.

⍟ /dull ➛ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴅᴜʟʟɴᴇss.
"""

__mod_name__ = "𝗦𝗘𝗫𝗬"
