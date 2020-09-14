# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
from userbot.utils import admin_cmd
import asyncio


@borg.on(admin_cmd(pattern="undlt"))
async def _(event):
    if event.fwd_from:
        return
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await borg.get_admin_log(event.chat_id, limit=5, search="", edit=False, delete=True)
        for i in a:
            await event.reply(i.original.action.message)
    else:
        await event.edit("Bu komutu yapmak için yönetici izinlerine ihtiyacınız var")
        await asyncio.sleep(3)
        await event.delete()
