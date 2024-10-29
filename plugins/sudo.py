# Jarvis - UserBot

"""
✘ Commands Available -

• `{i}addsudo`
    Add Sudo Users by replying to user or using <space> separated userid(s)

• `{i}delsudo`
    Remove Sudo Users by replying to user or using <space> separated userid(s)

• `{i}listsudo`
    List all sudo users.
"""

from telethon.tl.types import User

from pyJarvis._misc import sudoers

from . import get_string, inline_mention, udB, jarvis_bot, jarvis_cmd


@jarvis_cmd(pattern="addsudo( (.*)|$)", fullsudo=True)
async def _(jar):
    inputs = jar.pattern_match.group(1).strip()
    if jar.reply_to_msg_id:
        replied_to = await jar.get_reply_message()
        id = replied_to.sender_id
        name = await replied_to.get_sender()
    elif inputs:
        try:
            id = await jar.client.parse_id(inputs)
        except ValueError:
            try:
                id = int(inputs)
            except ValueError:
                id = inputs
        try:
            name = await jar.client.get_entity(int(id))
        except BaseException:
            name = None
    elif jar.is_private:
        id = jar.chat_id
        name = await jar.get_chat()
    else:
        return await jar.eor(get_string("sudo_1"), time=5)
    if name and isinstance(name, User) and (name.bot or name.verified):
        return await jar.eor(get_string("sudo_4"))
    name = inline_mention(name) if name else f"`{id}`"
    if id == jarvis_bot.uid:
        mmm = get_string("sudo_2")
    elif id in sudoers():
        mmm = f"{name} `is already a SUDO User ...`"
    else:
        udB.set_key("SUDO", "True")
        key = sudoers()
        key.append(id)
        udB.set_key("SUDOS", key)
        mmm = f"**Added** {name} **as SUDO User**"
    await jar.eor(mmm, time=5)


@jarvis_cmd(pattern="delsudo( (.*)|$)", fullsudo=True)
async def _(jar):
    inputs = jar.pattern_match.group(1).strip()
    if jar.reply_to_msg_id:
        replied_to = await jar.get_reply_message()
        id = replied_to.sender_id
        name = await replied_to.get_sender()
    elif inputs:
        try:
            id = await jar.client.parse_id(inputs)
        except ValueError:
            try:
                id = int(inputs)
            except ValueError:
                id = inputs
        try:
            name = await jar.client.get_entity(int(id))
        except BaseException:
            name = None
    elif jar.is_private:
        id = jar.chat_id
        name = await jar.get_chat()
    else:
        return await jar.eor(get_string("sudo_1"), time=5)
    name = inline_mention(name) if name else f"`{id}`"
    if id not in sudoers():
        mmm = f"{name} `wasn't a SUDO User ...`"
    else:
        key = sudoers()
        key.remove(id)
        udB.set_key("SUDOS", key)
        mmm = f"**Removed** {name} **from SUDO User(s)**"
    await jar.eor(mmm, time=5)


@jarvis_cmd(
    pattern="listsudo$",
)
async def _(jar):
    sudos = sudoers()
    if not sudos:
        return await jar.eor(get_string("sudo_3"), time=5)
    msg = ""
    for i in sudos:
        try:
            name = await jar.client.get_entity(int(i))
        except BaseException:
            name = None
        if name:
            msg += f"• {inline_mention(name)} ( `{i}` )\n"
        else:
            msg += f"• `{i}` -> Invalid User\n"
    m = udB.get_key("SUDO") or True
    if not m:
        m = "[False](https://graph.org/Jarvis-10-29-2)"
    return await jar.eor(
        f"**SUDO MODE : {m}\n\nList of SUDO Users :**\n{msg}", link_preview=False
    )
