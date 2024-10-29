# Jarvis - Userbot

from telethon.errors import (
    BotMethodInvalidError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
)

from . import LOG_CHANNEL, LOGS, Button, asst, eor, get_string, jarvis_cmd

REPOMSG = """
• **Jarvis UserBot** •\n
• Repo - [Click Here](https://github.com/btworeo/Jarvis)
• Addons - [Click Here](https://github.com/btworeo/JarvisAddons)
• Support - @JarvisSupportChat
"""

RP_BUTTONS = [
    [
        Button.url(get_string("bot_3"), "https://github.com/btworeo/Jarvis"),
        Button.url("Addons", "https://github.com/btworeo/JarvisAddons"),
    ],
    [Button.url("Support Group", "t.me/JarvisSupportChat")],
]

JARSTRING = """🎇 **Thanks for Deploying Jarvis Userbot!**

• Here, are the Some Basic stuff from, where you can Know, about its Usage."""


@jarvis_cmd(
    pattern="repo$",
    manager=True,
)
async def repify(e):
    try:
        q = await e.client.inline_query(asst.me.username, "")
        await q[0].click(e.chat_id)
        return await e.delete()
    except (
        ChatSendInlineForbiddenError,
        ChatSendMediaForbiddenError,
        BotMethodInvalidError,
    ):
        pass
    except Exception as er:
        LOGS.info(f"Error while repo command : {str(er)}")
    await e.eor(REPOMSG)


@jarvis_cmd(pattern="jarvis$")
async def useJarvis(rs):
    button = Button.inline("Start >>", "initft_2")
    msg = await asst.send_message(
        LOG_CHANNEL,
        JARSTRING,
        file="https://raw.githubusercontent.com/btwOreO/JarvisMedia/refs/heads/main/img7.jpg",
        buttons=button,
    )
    if not (rs.chat_id == LOG_CHANNEL and rs.client._bot):
        await eor(rs, f"**[Click Here]({msg.message_link})**")
