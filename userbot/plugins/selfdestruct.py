# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""Self Destruct Eklentisi
.sd <saniye cinsinden zaman> <metin>
"""


import time
from userbot import CMD_HELP
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="sdm", outgoing=True))
async def selfdestruct(destroy):
    if not destroy.text[0].isalpha() and destroy.text[0] not in (
            "/", "#", "@", "!"):
        message = destroy.text
        counter = int(message[5:7])
        text = str(destroy.text[7:])
        text = (
            text
        )
        await destroy.delete()
        smsg = await destroy.client.send_message(destroy.chat_id, text)
        time.sleep(counter)
        await smsg.delete()


@borg.on(admin_cmd(pattern="selfd", outgoing=True))
async def selfdestruct(destroy):
    if not destroy.text[0].isalpha() and destroy.text[0] not in (
            "/", "#", "@", "!"):
        message = destroy.text
        counter = int(message[7:9])
        text = str(destroy.text[9:])
        text = (
            text
            + "\n\n`Bu mesaj içinde kendi kendine imha edilecek "
            + str(counter)
            + " saniye`"
        )
        await destroy.delete()
        smsg = await destroy.client.send_message(destroy.chat_id, text)
        time.sleep(counter)
        await smsg.delete()


CMD_HELP.update({
    "selfdestruct":
    "**📌Komut ➥ ** .sdm numara [metin]\
\n**Kullanım ➥ **bu mesajı birkaç saniye içinde kendi kendine yok et \
\n\n**📌Komut ➥ ** .selfd numara [metin]\
\n**Kullanım ➥ ** yok edeceğini göstererek bu mesajı birkaç saniye içinde kendi kendini imha edin. \
"
})
