# Jarvis - UserBot

from .. import udB


def get_all_snips():
    return udB.get_key("SNIP") or {}


def add_snip(word, msg, media, button):
    ok = get_all_snips()
    ok.update({word: {"msg": msg, "media": media, "button": button}})
    udB.set_key("SNIP", ok)


def rem_snip(word):
    ok = get_all_snips()
    if ok.get(word):
        ok.pop(word)
        udB.set_key("SNIP", ok)


def get_snips(word):
    ok = get_all_snips()
    if ok.get(word):
        return ok[word]
    return False


def list_snip():
    return "".join(f"👉 ${z}\n" for z in get_all_snips())
