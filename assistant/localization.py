# Jarvis - Userbot

import re

from . import (
    Button,
    JARConfig,
    callback,
    get_back_button,
    get_languages,
    get_string,
    udB,
)


@callback("lang", owner=True)
async def setlang(event):
    languages = get_languages()
    tjard = [
        Button.inline(
            f"{languages[jar]['natively']} [{jar.lower()}]",
            data=f"set_{jar}",
        )
        for jar in languages
    ]
    buttons = list(zip(tjard[::2], tjard[1::2]))
    if len(tjard) % 2 == 1:
        buttons.append((tjard[-1],))
    buttons.append([Button.inline("« Back", data="mainmenu")])
    await event.edit(get_string("ast_4"), buttons=buttons)


@callback(re.compile(b"set_(.*)"), owner=True)
async def settt(event):
    lang = event.data_match.group(1).decode("UTF-8")
    languages = get_languages()
    JARConfig.lang = lang
    udB.del_key("language") if lang == "en" else udB.set_key("language", lang)
    await event.edit(
        f"Your language has been set to {languages[lang]['natively']} [{lang}].",
        buttons=get_back_button("lang"),
    )
