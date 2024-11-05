# Jarvis - Userbot

"""
✘ Command Available -

• `{i}semd <plugin_name>`

    To Send any Installed Plugin to the Chat!
"""

import os

from . import *


def send(fn):
    lst = ["plugins", "addons"]
    if not fn.endswith(".py"):
        fn += ".py"
    for i in lst:
        path = os.path.join(i, fn)
        if os.path.exists(path):
            return path
    else:
        return


def alt_send(fn):
    import re
    for k, v in LIST.items():
        for fx in v:
            if re.findall(fn, fx):
                return send(k)
    else:
        return


async def pastee(path):
    with open(path, "r") as f:
        data = f.read()
    err, linky = await get_paste(data)
    if err:
        return f"<b>>> <a href='https://spaceb.in/{linky}'>Pasted Here!</a></b> \n"
    else:
        LOGS.error(linky)
        return ""


@jarvis_cmd(pattern="semd ?(.*)")
async def semd_plugin(jar):
    repo = "https://github.com/btworeo/jarvis"
    args = jar.pattern_match.group(1)
    if not args:
        return await jar.eod("`Give a plugin name too`")

    eris = await jar.eor("`...`")
    path = send(args)
    if not path:
        path = alt_send(args)
    if not path:
        return await eris.edit(f"No plugins were found for: `{args}`")

    paste = await pastee(path)
    caption = f"<b>>> </b><code>{path}</code> \n{paste} \n" \
        f"© <a href='{repo}'>Jarvis</a>"
    try:
        await jar.client.send_file(
            jar.chat_id, path,
            caption=caption, parse_mode="html",
            thumb="resources/extras/jarvis.jpg",
            silent=True, reply_to=jar.reply_to_msg_id,
        )
        await eris.delete()
    except Exception as fx:
        return await eris.edit(str(fx))
