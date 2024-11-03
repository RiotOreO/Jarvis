<h1 align="center">
  <b>──「 Jαяνιѕ Uѕєявσᴛ 」──</b>
</h1>

<b>A stable pluggable Telegram userbot + Voice & Video Call music bot, based on Telethon.</b>

<details>
<summary>
<b> Nє¢єѕѕαяу Vαяιαвℓєѕ </b>
</summary>

* `API_ID` & `API_HASH` - API_ID & API_HASH for your account. Get it from [MyTelegramOrg](https://my.telegram.org/auth)
* `SESSION` - SessionString for your accounts login session. Get it from Sєѕѕισи. 👇
</details>

<details>
<summary>
<b> Sєѕѕισи </b>
</summary>

* Linux : `wget -O session.py https://raw.githubusercontent.com/btwOreO/Jarvis/refs/heads/main/resources/session/ssgen.py && python3 session.py`
* PowerShell : `cd desktop ; wget https://raw.githubusercontent.com/btwOreO/Jarvis/refs/heads/main/resources/session/ssgen.py ; python jarvis.py`

</details>

<details>
<summary>
<b> Dαтαвαѕє Vαяιαвℓєѕ </b>
</summary>

One of the following database:
- For **Redis** (tutorial [here](./resources/extras/redistut.md))
  - `REDIS_URI` - Redis endpoint URL, from [redislabs](http://redislabs.com/).
  - `REDIS_PASSWORD` - Redis endpoint Password, from [redislabs](http://redislabs.com/).
- For **MONGODB**
  - `MONGO_URI` - Get it from [mongodb](https://mongodb.com/atlas).
- For **SQLDB**
  - `DATABASE_URL`- Get it from [elephantsql](https://elephantsql.com).

</details>

<details>
<summary>
<b> ᴠᴘs/ʟᴏᴄᴀʟ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ ᴍᴇᴛʜᴏᴅ </b>
</summary>

- Get your [Necessary Variables](#Nє¢єѕѕαяу_Vαяιαвℓєѕ)
- Clone The Repository:
  `git clone https://github.com/btwOreO/jarvis`
- Go to the cloned folder:
  `cd jarvis`
- Install the requirements:
  `pip install -r requirements.txt`
- Fill your details in a `.env` file, as given in [`.env.sample`](https://github.com/btwOreO/Jarvis/blob/main/.env.sample).
- Run the Bot:
  - Linux Users:
   `bash startup`
  - Windows Users:
    `python -m pyJarvis`

</details>

━━━━━━━━━━━━━━━━━━━━
<h3 align="center">
    ─「 sᴜᴩᴩᴏʀᴛ 」─
</h3>

<p align="center">
<a href="https://telegram.me/JarvisSupportChat"><img src="https://img.shields.io/badge/-Support%20Group-blue.svg?style=for-the-badge&logo=Telegram"></a>
</p>
<p align="center">
<a href="https://telegram.me/MyJarvis"><img src="https://img.shields.io/badge/-Support%20Channel-blue.svg?style=for-the-badge&logo=Telegram"></a>
</p>

━━━━━━━━━━━━━━━━━━━━

<h3 align="center">
    ─「 ᴄʀᴇᴅɪᴛs 」─
</h3>

* [Lonami](https://github.com/LonamiWebs/) for [Telethon.](https://github.com/LonamiWebs/Telethon)
* [MarshalX](https://github.com/MarshalX) for [PyTgCalls.](https://github.com/MarshalX/tgcalls)

---
