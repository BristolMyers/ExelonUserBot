# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="ctg ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Bir Bağlantıya Cevap Verin.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("```Bir Bağlantıya Cevap Verin.```")
        return
    chat = "@chotamreaderbot"
    reply_message.sender
    await event.edit("```İşleniyor```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=272572121))
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("`RIP Kara Liste Patronunuzu Kontrol Edin`")
            return
        if response.text.startswith(""):
            await event.edit("Aptal mıyım yoksa aptal mıyım?")
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)
