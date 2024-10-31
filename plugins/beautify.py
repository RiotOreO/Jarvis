# Jarvis - Userbot

from . import get_help

__doc__ = get_help("help_beautify")


import os
import random

from telethon.utils import get_display_name
from urllib.parse import urlencode
from . import Carbon, jarvis_cmd, get_string, inline_mention
from secrets import token_hex

_colorspath = "resources/colorlist.txt"

if os.path.exists(_colorspath):
    with open(_colorspath, "r") as f:
        all_col = f.read().split()
else:
    all_col = []


@jarvis_cmd(
    pattern="(rc|c)arbon",
)
async def cr_bn(event):
    xxxx = await event.eor(get_string("com_1"))
    te = event.pattern_match.group(1)
    col = random.choice(all_col) if te[0] == "r" else "White"
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            b = await event.client.download_media(temp)
            with open(b) as a:
                code = a.read()
            os.remove(b)
        else:
            code = temp.message
    else:
        try:
            code = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            return await xxxx.eor(get_string("carbon_2"))
    xx = await Carbon(code=code, file_name="jarvis_carbon", backgroundColor=col)
    if isinstance(xx, dict):
        await xxxx.edit(f"`{xx}`")
        return
    await xxxx.delete()
    await event.reply(
        f"Carbonised by {inline_mention(event.sender)}",
        file=xx,
    )


@jarvis_cmd(
    pattern="ccarbon( (.*)|$)",
)
async def crbn(event):
    match = event.pattern_match.group(1).strip()
    if not match:
        return await event.eor(get_string("carbon_3"))
    msg = await event.eor(get_string("com_1"))
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            b = await event.client.download_media(temp)
            with open(b) as a:
                code = a.read()
            os.remove(b)
        else:
            code = temp.message
    else:
        try:
            match = match.split(" ", maxsplit=1)
            code = match[1]
            match = match[0]
        except IndexError:
            return await msg.eor(get_string("carbon_2"))
    xx = await Carbon(code=code, backgroundColor=match)
    await msg.delete()
    await event.reply(
        f"Carbonised by {inline_mention(event.sender)}",
        file=xx,
    )
