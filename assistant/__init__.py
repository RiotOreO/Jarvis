# Jarvis - UserBot

from telethon import Button, custom

from plugins import ATRA_COL, InlinePlugin
from pyJarvis import *
from pyJarvis import _jar_cache
from pyJarvis._misc import owner_and_sudos
from pyJarvis._misc._assistant import asst_cmd, callback, in_pattern
from pyJarvis.fns.helper import *
from pyJarvis.fns.tools import get_stored_file
from strings import get_languages, get_string

OWNER_NAME = jarvis_bot.full_name
OWNER_ID = jarvis_bot.uid

AST_PLUGINS = {}


async def setit(event, name, value):
    try:
        udB.set_key(name, value)
    except BaseException as er:
        LOGS.exception(er)
        return await event.edit("`Something Went Wrong`")


def get_back_button(name):
    return [Button.inline("« Bᴀᴄᴋ", data=f"{name}")]
