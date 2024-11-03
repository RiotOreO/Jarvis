# Jarvis - Userbot

"""
✘ Commands Available -

• `{i}mediainfo <reply to media>/<file path>/<url>`
   To get info about it.
"""

import os
import time
from datetime import datetime as dt

from pyJarvis.fns.misc import rotate_image
from pyJarvis.fns.tools import make_html_telegraph

from . import (
    LOGS,
    Telegraph,
    bash,
    downloader,
    get_string,
    is_url_ok,
    mediainfo,
    jarvis_cmd,
)

@jarvis_cmd(pattern="mediainfo( (.*)|$)")
async def mi(e):
    r = await e.get_reply_message()
    match = e.pattern_match.group(1).strip()
    taime = time.time()
    extra = ""
    if r and r.media:
        xx = mediainfo(r.media)
        murl = r.media.stringify()
        url = await make_html_telegraph("Mediainfo", f"<pre>{murl}</pre>")
        extra = f"**[{xx}]({url})**\n\n"
        e = await e.eor(f"{extra}`Loading More...`", link_preview=False)

        if hasattr(r.media, "document"):
            file = r.media.document
            mime_type = file.mime_type
            filename = r.file.name
            if not filename:
                if "audio" in mime_type:
                    filename = "audio_" + dt.now().isoformat("_", "seconds") + ".ogg"
                elif "video" in mime_type:
                    filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
            dl = await downloader(
                f"resources/downloads/{filename}",
                file,
                e,
                taime,
                f"{extra}`Loading More...`",
            )

            naam = dl.name
        else:
            naam = await r.download_media()
    elif match and (
        os.path.isfile(match)
        or (match.startswith("https://") and (await is_url_ok(match)))
    ):
        naam, xx = match, "file"
    else:
        return await e.eor(get_string("cvt_3"), time=5)
    out, er = await bash(f"mediainfo '{naam}'")
    if er:
        LOGS.info(er)
        out = extra or str(er)
        return await e.edit(out, link_preview=False)
    makehtml = ""
    if naam.endswith((".jpg", ".png")):
        if os.path.exists(naam):
            med = "https://graph.org" + Telegraph.upload_file(naam)[0]["src"]
        else:
            med = match
        makehtml += f"<img src='{med}'><br>"
    for line in out.split("\n"):
        line = line.strip()
        if not line:
            makehtml += "<br>"
        elif ":" not in line:
            makehtml += f"<h3>{line}</h3>"
        else:
            makehtml += f"<p>{line}</p>"
    try:
        urll = await make_html_telegraph("Mediainfo", makehtml)
    except Exception as er:
        LOGS.exception(er)
        return
    await e.eor(f"{extra}[{get_string('mdi_1')}]({urll})", link_preview=False)
    if not match:
        os.remove(naam)
