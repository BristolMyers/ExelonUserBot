# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

"""Herhangi bir mesajda Görülen Sayacı etkinleştirin,
mesajınızı kaç kullanıcının gördüğünü bilmek için
Kullanım: Herhangi bir iletiye yanıt olarak .frwd"""
from userbot import CMD_HELP
from userbot.utils import admin_cmd
from userbot.uniborgConfig import Config


@borg.on(admin_cmd(pattern="frwd"))
async def _(event):
    if event.fwd_from:
        return
    if Config.PRIVATE_CHANNEL_BOT_API_ID is None:
        await event.edit("Bu eklentinin çalışması için lütfen gerekli ortam değişkenini `PRIVATE_CHANNEL_BOT_API_ID` ayarlayın")
        return
    try:
        e = await borg.get_entity(Config.PRIVATE_CHANNEL_BOT_API_ID)
    except Exception as e:
        await event.edit(str(e))
    else:
        re_message = await event.get_reply_message()
        # https://t.me/telethonofftopic/78166
        fwd_message = await borg.forward_messages(
            e,
            re_message,
            silent=True
        )
        await borg.forward_messages(
            event.chat_id,
            fwd_message
        )
        await fwd_message.delete()
        await event.delete()

CMD_HELP.update({"frwd": "**PLUGİN İSMİ:** `frwd`:\
      \n\n**📌Komut ➥ **`.frwd `\
      \n**Kullanım ➥ ** Herhangi bir mesajda Görülen Sayacı etkinleştirin, mesajınızı kaç kullanıcının gördüğünü bilmek için Herhangi bir iletiye yanıt olarak .frwd olarak yanıtlayın"
                 })
