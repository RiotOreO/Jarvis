# Jarvis - UserBot

import random

from telethon import errors
from telethon.errors.rpcerrorlist import StickersetInvalidError
from telethon.tl.functions.messages import GetStickerSetRequest as GetSticker
from telethon.tl.functions.messages import UploadMediaRequest
from telethon.tl.functions.stickers import AddStickerToSetRequest as AddSticker
from telethon.tl.functions.stickers import CreateStickerSetRequest
from telethon.tl.types import InputPeerSelf
from telethon.tl.types import InputStickerSetItem as SetItem
from telethon.tl.types import InputStickerSetShortName, User
from telethon.utils import get_display_name, get_input_document

from pyJarvis.fns.misc import Quotly
from pyJarvis.fns.tools import TgConverter

from . import LOGS, asst, asst_cmd, udB


@asst_cmd(
    pattern="kang",
)
async def kang_cmd(jar):
    sender = await jar.get_sender()
    if not isinstance(sender, User):
        return
    if not jar.is_reply:
        return await jar.eor("`Reply to a sticker/photo..`", time=5)
    reply = await jar.get_reply_message()
    if sender.username:
        pre = sender.username[:4]
    else:
        pre = random.random_string(length=3)
    animated, dl, video = None, None, None
    try:
        emoji = jar.text.split(maxsplit=1)[1]
    except IndexError:
        emoji = None
    if reply.sticker:
        file = get_input_document(reply.sticker)
        emoji = emoji or reply.file.emoji
        name = reply.file.name
        if name.endswith(".tgs"):
            animated = True
            dl = await reply.download_media()
        elif name.endswith(".webm"):
            video = True
            dl = await reply.download_media()
    elif reply.photo:
        dl = await reply.download_media()
        name = "sticker.webp"
        image = TgConverter.resize_photo_sticker(dl)
        image.save(name, "WEBP")
    elif reply.text:
        dl = await Quotly().create_quotly(reply)
    else:
        return await jar.eor("`Reply to sticker or text to add it in your pack...`")
    if not emoji:
        emoji = "🏵"
    if dl:
        upl = await jar.client.upload_file(dl)
        file = get_input_document(
            await jar.client(UploadMediaRequest(InputPeerSelf(), upl))
        )
    get_ = udB.get_key("STICKERS") or {}
    type_ = "anim" if animated else "static"
    if not get_.get(jar.sender_id) or not get_.get(jar.sender_id, {}).get(type_):
        sn = f"{pre}_{jar.sender_id}"
        title = f"{get_display_name(sender)}'s Kang Pack"
        if animated:
            type_ = "anim"
            sn += "_anim"
            title += " (Animated)"
        elif video:
            type_ = "vid"
            sn += "_vid"
            title += " (Video)"
        sn += f"_by_{asst.me.username}"
        try:
            await asst(GetSticker(InputStickerSetShortName(sn), hash=0))
            sn = sn.replace(str(jar.sender_id), f"{jar.sender_id}_{jar.id}")
        except StickersetInvalidError:
            pass
        try:
            pack = await jar.client(
                CreateStickerSetRequest(
                    user_id=sender.id,
                    title=title,
                    short_name=sn,
                    stickers=[SetItem(file, emoji=emoji)],
                    videos=video,
                    animated=animated,
                    software="@MyJarvis",
                )
            )
        except Exception as er:
            return await jar.eor(str(er))
        sn = pack.set.short_name
        if not get_.get(jar.sender_id):
            get_.update({jar.sender_id: {type_: [sn]}})
        else:
            get_[jar.sender_id].update({type_: [sn]})
        udB.set_key("STICKERS", get_)
        return await jar.reply(
            f"**Kanged Successfully!\nEmoji :** {emoji}\n**Link :** [Click Here](https://t.me/addstickers/{sn})"
        )
    name = get_[jar.sender_id][type_][-1]
    try:
        await asst(GetSticker(InputStickerSetShortName(name), hash=0))
    except StickersetInvalidError:
        get_[jar.sender_id][type_].remove(name)
    try:
        await asst(
            AddSticker(InputStickerSetShortName(name), SetItem(file, emoji=emoji))
        )
    except (errors.StickerpackStickersTooMuchError, errors.StickersTooMuchError):
        sn = f"{pre}{jar.sender_id}_{jar.id}"
        title = f"{get_display_name(sender)}'s Kang Pack"
        if animated:
            sn += "_anim"
            title += " (Animated)"
        elif video:
            sn += "_vid"
            title += "(Video)"
        sn += f"_by_{asst.me.username}"
        try:
            pack = await jar.client(
                CreateStickerSetRequest(
                    user_id=sender.id,
                    title=title,
                    short_name=sn,
                    stickers=[SetItem(file, emoji=emoji)],
                    animated=animated,
                )
            )
        except Exception as er:
            return await jar.eor(str(er))
        get_[jar.sender_id][type_].append(pack.set.short_name)
        udB.set_key("STICKERS", get_)
        return await jar.reply(
            f"**Created New Kang Pack!\nEmoji :** {emoji}\n**Link :** [Click Here](https://t.me/addstickers/{sn})"
        )
    except Exception as er:
        LOGS.exception(er)
        return await jar.reply(str(er))
    await jar.reply(
        f"Sticker Added to Pack Successfully\n**Link :** [Click Here](https://t.me/addstickers/{name})"
    )


@asst_cmd(pattern="listpack")
async def do_magic(jar):
    ko = udB.get_key("STICKERS") or {}
    if not ko.get(jar.sender_id):
        return await jar.reply("No Sticker Pack Found!")
    al_ = []
    ul = ko[jar.sender_id]
    for _ in ul.keys():
        al_.extend(ul[_])
    msg = "• **Stickers Owned by You!**\n\n"
    for _ in al_:
        try:
            pack = await jar.client(GetSticker(InputStickerSetShortName(_), hash=0))
            msg += f"• [{pack.set.title}](https://t.me/addstickers/{_})\n"
        except StickerSetInvalidError:
            if ul.get("anim") and _ in ul["anim"]:
                ul["anim"].remove(_)
            elif ul.get("vid") and _ in ul["vid"]:
                ul["vid"].remove(_)
            else:
                ul["static"].remove(_)
            udB.set_key("STICKERS", ko)
    await jar.reply(msg)
