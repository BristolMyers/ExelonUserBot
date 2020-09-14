# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from telethon.tl.types import InputMessagesFilterDocument
from userbot.utils import load_module
from var import Var
from pathlib import Path
import os
from ..utils import admin_cmd, sudo_cmd
from .. import CMD_HELP


@borg.on(admin_cmd(pattern="extdl$", outgoing=True))
@borg.on(sudo_cmd(pattern="extdl$", allow_sudo=True))
async def install(event):
    if event.fwd_from:
        return
    chat = Var.PLUGIN_CHANNEL
    documentss = await borg.get_messages(chat, None, filter=InputMessagesFilterDocument)
    total = int(documentss.total)
    total_doxx = range(0, total)
    await event.delete()
    for ixo in total_doxx:
        mxo = documentss[ixo].id
        downloaded_file_name = await event.client.download_media(await borg.get_messages(chat, ids=mxo), "userbot/plugins/")
        if "(" not in downloaded_file_name:
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            load_module(shortname.replace(".py", ""))
            await borg.send_message(event.chat_id, "Eklenti `{}` başarıyla yüklendi.".format(os.path.basename(downloaded_file_name)))
        else:
            await borg.send_message(event.chat_id, "Eklenti `{}` önceden yüklendi ve yüklenemez.".format(os.path.basename(downloaded_file_name)))


CMD_HELP.update({"externalplugins": "**PLUGİN İSMİ:** `externalplugins`\
      \n\n**📌Komut ➥ **`.extdl` :\
      \n**Kullanım ➥ ** Harici eklentileri kurmak için Özel bir kanal oluşturun ve tüm harici modüllerinizi oraya gönderin ve heroku'da `PLUGIN CHANNEL` ve kanal kimliğiyle değer olarak bir değişken belirleyin.\
      bu nedenle, her yeniden başlatma veya güncellemeden sonra, tüm harici modülleri yüklemek için `.extdl` yazın\
      "
                 })
