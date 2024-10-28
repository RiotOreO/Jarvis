# Jarvis - UserBot

import os
import sys
import telethonpatch
from .version import __version__

run_as_module = __package__ in sys.argv or sys.argv[0] == "-m"


class JARConfig:
    lang = "en"
    thumb = "resources/extras/jarvis.jpg"


if run_as_module:
    import time

    from .configs import Var
    from .startup import *
    from .startup._database import JarvisDB
    from .startup.BaseClient import JarvisClient
    from .startup.connections import validate_session, vc_connection
    from .startup.funcs import _version_changes, autobot, enable_inline, update_envs
    from .version import jarvis_version

    if not os.path.exists("./plugins"):
        LOGS.error(
            "'plugins' folder not found!\nMake sure that, you are on correct path."
        )
        exit()

    start_time = time.time()
    _jar_cache = {}
    _ignore_eval = []

    udB = JarvisDB()
    update_envs()

    LOGS.info(f"Connecting to {udB.name}...")
    if udB.ping():
        LOGS.info(f"Connected to {udB.name} Successfully!")

    BOT_MODE = udB.get_key("BOTMODE")
    DUAL_MODE = udB.get_key("DUAL_MODE")

    USER_MODE = udB.get_key("USER_MODE")
    if USER_MODE:
        DUAL_MODE = False

    if BOT_MODE:
        if DUAL_MODE:
            udB.del_key("DUAL_MODE")
            DUAL_MODE = False
        jarvis_bot = None

        if not udB.get_key("BOT_TOKEN"):
            LOGS.critical(
                '"BOT_TOKEN" not Found! Please add it, in order to use "BOTMODE"'
            )

            sys.exit()
    else:
        jarvis_bot = JarvisClient(
            validate_session(Var.SESSION, LOGS),
            udB=udB,
            app_version=jarvis_version,
            device_model="Jarvis",
        )
        jarvis_bot.run_in_loop(autobot())

    if USER_MODE:
        asst = jarvis_bot
    else:
        asst = JarvisClient("asst", bot_token=udB.get_key("BOT_TOKEN"), udB=udB)

    if BOT_MODE:
        jarvis_bot = asst
        if udB.get_key("OWNER_ID"):
            try:
                jarvis_bot.me = jarvis_bot.run_in_loop(
                    jarvis_bot.get_entity(udB.get_key("OWNER_ID"))
                )
            except Exception as er:
                LOGS.exception(er)
    elif not asst.me.bot_inline_placeholder and asst._bot:
        jarvis_bot.run_in_loop(enable_inline(jarvis_bot, asst.me.username))

    vcClient = vc_connection(udB, jarvis_bot)

    _version_changes(udB)

    HNDLR = udB.get_key("HNDLR") or "."
    DUAL_HNDLR = udB.get_key("DUAL_HNDLR") or "/"
    SUDO_HNDLR = udB.get_key("SUDO_HNDLR") or HNDLR
else:
    print("pyJarvis 2024 © myjarvis.t.me")

    from logging import getLogger

    LOGS = getLogger("pyJarvis")

    jarvis_bot = asst = udB = vcClient = None
