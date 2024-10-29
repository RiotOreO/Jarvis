# Jarvis - UserBot

import asyncio

from telethon import events
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.utils import get_display_name

from pyJarvis.dB import stickers
from pyJarvis.dB.echo_db import check_echo
from pyJarvis.dB.forcesub_db import get_forcesetting
from pyJarvis.dB.gban_mute_db import is_gbanned
from pyJarvis.dB.greetings_db import get_goodbye, get_welcome, must_thank
from pyJarvis.dB.nsfw_db import is_profan
from pyJarvis.fns.helper import inline_mention
from pyJarvis.fns.tools import async_searcher, create_tl_btn, get_chatbot_reply

try:
    from ProfanityDetector import detector
except ImportError:
    detector = None
from . import LOG_CHANNEL, LOGS, asst, get_string, types, udB, jarvis_bot
from ._inline import something


@jarvis_bot.on(events.ChatAction())
async def Function(event):
    try:
        await DummyHandler(event)
    except Exception as er:
        LOGS.exception(er)


async def DummyHandler(jar):
    # clean chat actions
    key = udB.get_key("CLEANCHAT") or []
    if jar.chat_id in key:
        try:
            await jar.delete()
        except BaseException:
            pass

    # thank members
    if must_thank(jar.chat_id):
        chat_count = (await jar.client.get_participants(jar.chat_id, limit=0)).total
        if chat_count % 100 == 0:
            stik_id = chat_count / 100 - 1
            sticker = stickers[stik_id]
            await jar.respond(file=sticker)
    # force subscribe
    if (
        udB.get_key("FORCESUB")
        and ((jar.user_joined or jar.user_added))
        and get_forcesetting(jar.chat_id)
    ):
        user = await jar.get_user()
        if not user.bot:
            joinchat = get_forcesetting(jar.chat_id)
            try:
                await jarvis_bot(GetParticipantRequest(int(joinchat), user.id))
            except UserNotParticipantError:
                await jarvis_bot.edit_permissions(
                    jar.chat_id, user.id, send_messages=False
                )
                res = await jarvis_bot.inline_query(
                    asst.me.username, f"fsub {user.id}_{joinchat}"
                )
                await res[0].click(jar.chat_id, reply_to=jar.action_message.id)

    if jar.user_joined or jar.added_by:
        user = await jar.get_user()
        chat = await jar.get_chat()
        # gbans and @JarvisBans checks
        if udB.get_key("JARVIS_BANS"):
            try:
                is_banned = await async_searcher(
                    "https://bans.jarvis.tech/api/status",
                    json={"userId": user.id},
                    post=True,
                    re_json=True,
                )
                if is_banned["is_banned"]:
                    await jar.client.edit_permissions(
                        chat.id,
                        user.id,
                        view_messages=False,
                    )
                    await jar.respond(
                        f'**@JarvisBans:** Banned user detected and banned!\n`{str(is_banned)}`.\nBan reason: {is_banned["reason"]}',
                    )

            except BaseException:
                pass
        reason = is_gbanned(user.id)
        if reason and chat.admin_rights:
            try:
                await jar.client.edit_permissions(
                    chat.id,
                    user.id,
                    view_messages=False,
                )
                gban_watch = get_string("can_1").format(inline_mention(user), reason)
                await jar.reply(gban_watch)
            except Exception as er:
                LOGS.exception(er)

        # greetings
        elif get_welcome(jar.chat_id):
            user = await jar.get_user()
            chat = await jar.get_chat()
            title = chat.title or "this chat"
            count = (
                chat.participants_count
                or (await jar.client.get_participants(chat, limit=0)).total
            )
            mention = inline_mention(user)
            name = user.first_name
            fullname = get_display_name(user)
            uu = user.username
            username = f"@{uu}" if uu else mention
            wel = get_welcome(jar.chat_id)
            msgg = wel["welcome"]
            med = wel["media"] or None
            userid = user.id
            msg = None
            if msgg:
                msg = msgg.format(
                    mention=mention,
                    group=title,
                    count=count,
                    name=name,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                )
            if wel.get("button"):
                btn = create_tl_btn(wel["button"])
                await something(jar, msg, med, btn)
            elif msg:
                send = await jar.reply(
                    msg,
                    file=med,
                )
                await asyncio.sleep(150)
                await send.delete()
            else:
                await jar.reply(file=med)
    elif (jar.user_left or jar.user_kicked) and get_goodbye(jar.chat_id):
        user = await jar.get_user()
        chat = await jar.get_chat()
        title = chat.title or "this chat"
        count = (
            chat.participants_count
            or (await jar.client.get_participants(chat, limit=0)).total
        )
        mention = inline_mention(user)
        name = user.first_name
        fullname = get_display_name(user)
        uu = user.username
        username = f"@{uu}" if uu else mention
        wel = get_goodbye(jar.chat_id)
        msgg = wel["goodbye"]
        med = wel["media"]
        userid = user.id
        msg = None
        if msgg:
            msg = msgg.format(
                mention=mention,
                group=title,
                count=count,
                name=name,
                fullname=fullname,
                username=username,
                userid=userid,
            )
        if wel.get("button"):
            btn = create_tl_btn(wel["button"])
            await something(jar, msg, med, btn)
        elif msg:
            send = await jar.reply(
                msg,
                file=med,
            )
            await asyncio.sleep(150)
            await send.delete()
        else:
            await jar.reply(file=med)


@jarvis_bot.on(events.NewMessage(incoming=True))
async def chatBot_replies(e):
    sender = await e.get_sender()
    if not isinstance(sender, types.User) or sender.bot:
        return
    if check_echo(e.chat_id, e.sender_id):
        try:
            await e.respond(e.message)
        except Exception as er:
            LOGS.exception(er)
    key = udB.get_key("CHATBOT_USERS") or {}
    if e.text and key.get(e.chat_id) and sender.id in key[e.chat_id]:
        msg = await get_chatbot_reply(e.message.message)
        if msg:
            sleep = udB.get_key("CHATBOT_SLEEP") or 1.5
            await asyncio.sleep(sleep)
            await e.reply(msg)
    chat = await e.get_chat()
    if e.is_group and sender.username:
        await uname_stuff(e.sender_id, sender.username, sender.first_name)
    elif e.is_private and chat.username:
        await uname_stuff(e.sender_id, chat.username, chat.first_name)
    if detector and is_profan(e.chat_id) and e.text:
        x, y = detector(e.text)
        if y:
            await e.delete()


@jarvis_bot.on(events.Raw(types.UpdateUserName))
async def uname_change(e):
    await uname_stuff(e.user_id, e.usernames[0] if e.usernames else None, e.first_name)


async def uname_stuff(id, uname, name):
    if udB.get_key("USERNAME_LOG"):
        old_ = udB.get_key("USERNAME_DB") or {}
        old = old_.get(id)
        # Ignore Name Logs
        if old and old == uname:
            return
        if old and uname:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_2").format(old, uname),
            )
        elif old:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_3").format(f"[{name}](tg://user?id={id})", old),
            )
        elif uname:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_4").format(f"[{name}](tg://user?id={id})", uname),
            )

        old_[id] = uname
        udB.set_key("USERNAME_DB", old_)
