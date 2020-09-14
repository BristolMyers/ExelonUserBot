# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from .. import CMD_HELP
from ..utils import admin_cmd, sudo_cmd
from telethon.tl.functions.messages import SaveDraftRequest


@borg.on(admin_cmd(pattern="chain$"))
@borg.on(sudo_cmd(pattern="chain$", allow_sudo=True))
async def _(event):
    await event.edit("Sayma...")
    count = -1
    message = event.message
    while message:
        reply = await message.get_reply_message()
        if reply is None:
            await borg(SaveDraftRequest(
                await event.get_input_chat(),
                "",
                reply_to_msg_id=message.id
            ))
        message = reply
        count += 1
    await event.edit(f"Zincir uzunluğu: {count}")


CMD_HELP.update({"chain": "**PLUGİN İSMİ:** `chain`\
      \n\n**📌Komut ➥ **`.chain` :\
      \n**Kullanım ➥ ** Dönüşümün uzunluğunu bulmak istediğiniz herhangi bir dönüşüm için bu komutu yanıtlayın (Yalnızca etiketli zincir sayılacaktır..\
      "
                 })
