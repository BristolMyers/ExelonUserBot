# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import nekos
import requests
import time
from PIL import Image
from telethon import version
from userbot import StartTime
from platform import python_version
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from userbot import CMD_HELP, ALIVE_NAME, exelondef, exelonversion
from ..uniborgConfig import Config

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "exelon"
EXELON_IMG = Config.ALIVE_PIC


@borg.on(admin_cmd(outgoing=True, pattern="alive$"))
@borg.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    reply_to_id = alive.message
    uptime = await exelondef.get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    hmm = bot.uid
    if alive.reply_to_msg_id:
        reply_to_id = await alive.get_reply_message()
    if EXELON_IMG:
        exelon_caption = f"__**✮ EXELON BAŞARIYLA ÇALIŞIYOR ✮**__\n\n"
        exelon_caption += f"**✧ Veri Tabanı :** `{check_sgnirts}`\n"
        exelon_caption += f"**✧ Telethon Sürümü :** `{version.__version__}\n`"
        exelon_caption += f"**✧ ExelonUserBot Sürümü :** `{exelonversion}`\n"
        exelon_caption += f"**✧ Python Sürümü :** `{python_version()}\n`"
        exelon_caption += f"**✧ Çalışma Süresi :** `{uptime}\n`"
        exelon_caption += f"**✧ Benim Ustam :** [{DEFAULTUSER}](tg://user?id={hmm})\n"
        await borg.send_file(alive.chat_id, EXELON_IMG, caption=exelon_caption, reply_to=reply_to_id)
        await alive.delete()
    else:
        await edit_or_reply(alive, f"__**✮ EXELON BAŞARIYLA ÇALIŞIYOR ✮**__\n\n"
                            f"**✧ Veri Tabanı :** `{check_sgnirts}`\n"
                            f"**✧ Telethon Sürümü :** `{version.__version__}\n`"
                            f"**✧ ExelonUserBot Sürümü :** `{exelonversion}`\n"
                            f"**✧ Python Sürümü :** `{python_version()}\n`"
                            f"**✧ Çalışma Süresi :** `{uptime}\n`"
                            f"**✧ Benim Ustam :** [{DEFAULTUSER}](tg://user?id={hmm})\n"
                            )


@borg.on(admin_cmd(outgoing=True, pattern="ialive$"))
@borg.on(sudo_cmd(pattern="ialive$", allow_sudo=True))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
    reply_to_id = alive.message
    if alive.reply_to_msg_id:
        reply_to_id = await alive.get_reply_message()
    hmm = bot.uid
    exelon_caption = f"__**ExelonUserBot Çalışıyor**__\n"
    exelon_caption += f"**  -Telethon Sürümü :** `{version.__version__}\n`"
    exelon_caption += f"**  -ExelonUserBot Sürümü :** `{exelonversion}`\n"
    exelon_caption += f"**  -Python Sürümü :** `{python_version()}\n`"
    exelon_caption += f"**  -Benim ustam :** [{DEFAULTUSER}](tg://user?id={hmm})\n"
    results = await bot.inline_query(  # pylint:disable=E0602
        tgbotusername,
        exelon_caption
    )
    await results[0].click(
        alive.chat_id,
        reply_to=reply_to_id,
        hide_via=True
    )
    await alive.delete()


@borg.on(admin_cmd(pattern="exelon$"))
@borg.on(sudo_cmd(pattern="exelon$", allow_sudo=True))
async def _(event):
    try:
        await event.delete()
    except BaseException:
        pass
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.cat()).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    img.seek(0)
    await bot.send_file(event.chat_id, open("temp.webp", "rb"), reply_to=reply_to_id)


# UniBorg Telegram UseRBot
# Copyright (C) 2020 @UniBorg
# This code is licensed under
# the "you can't use this for anything - public or private,
# unless you know the two prime factors to the number below" license
# 543935563961418342898620676239017231876605452284544942043082635399903451854594062955
# വിവരണം അടിച്ചുമാറ്റിക്കൊണ്ട് പോകുന്നവർ
# ക്രെഡിറ്റ് വെച്ചാൽ സന്തോഷമേ ഉള്ളു..!
# uniborg


def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "Veritabanı ayarlanmadı"
    if not Var.DB_URI:
        return is_database_working, output
    from userbot.plugins.sql_helper import SESSION
    try:
        # to check database we will execute raw query
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"❌ {str(e)}"
        is_database_working = False
    else:
        output = "Normal Çalışıyor"
        is_database_working = True
    return is_database_working, output


CMD_HELP.update({"alive": "**PLUGİN İSMİ:** `alive`\
      \n\n**📌Komut ➥ **`.alive` :\
      \n**Kullanım ➥ ** botun durumu.\
      \n\n**📌Komut ➥ **`.ialive` :\
      \n**Kullanım ➥ ** Canlı Görünüm Alive\
      \n\n**📌Komut ➥ ** `.exelon`\
      \n**Kullanım ➥ **Rastgele exelon çıkartmaları"
                 })
