# Jarvis - UserBot

from . import get_help

__doc__ = get_help("help_database")

import re

from . import Redis, eor, get_string, udB, jarvis_cmd


@jarvis_cmd(pattern="setdb( (.*)|$)", fullsudo=True)
async def _(jar):
    match = jar.pattern_match.group(1).strip()
    if not match:
        return await jar.eor("Provide key and value to set!")
    try:
        delim = " " if re.search("[|]", match) is None else " | "
        data = match.split(delim, maxsplit=1)
        if data[0] in ["--extend", "-e"]:
            data = data[1].split(maxsplit=1)
            data[1] = f"{str(udB.get_key(data[0]))} {data[1]}"
        udB.set_key(data[0], data[1])
        await jar.eor(
            f"**DB Key Value Pair Updated\nKey :** `{data[0]}`\n**Value :** `{data[1]}`"
        )

    except BaseException:
        await jar.eor(get_string("com_7"))


@jarvis_cmd(pattern="deldb( (.*)|$)", fullsudo=True)
async def _(jar):
    key = jar.pattern_match.group(1).strip()
    if not key:
        return await jar.eor("Give me a key name to delete!", time=5)
    _ = key.split(maxsplit=1)
    try:
        if _[0] == "-m":
            for key in _[1].split():
                k = udB.del_key(key)
            key = _[1]
        else:
            k = udB.del_key(key)
        if k == 0:
            return await jar.eor("`No Such Key.`")
        await jar.eor(f"`Successfully deleted key {key}`")
    except BaseException:
        await jar.eor(get_string("com_7"))


@jarvis_cmd(pattern="rendb( (.*)|$)", fullsudo=True)
async def _(jar):
    match = jar.pattern_match.group(1).strip()
    if not match:
        return await jar.eor("`Provide Keys name to rename..`")
    delim = " " if re.search("[|]", match) is None else " | "
    data = match.split(delim)
    if Redis(data[0]):
        try:
            udB.rename(data[0], data[1])
            await eor(
                jar,
                f"**DB Key Rename Successful\nOld Key :** `{data[0]}`\n**New Key :** `{data[1]}`",
            )

        except BaseException:
            await jar.eor(get_string("com_7"))
    else:
        await jar.eor("Key not found")
