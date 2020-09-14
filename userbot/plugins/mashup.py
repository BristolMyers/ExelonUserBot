# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""
video meme mashup:
Syntax: .mash <text>
"""
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.utils import admin_cmd, sudo_cmd
from userbot import CMD_HELP


@borg.on(admin_cmd(pattern="mash ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    chat = "@vixtbot"
    await event.edit("```Kontrol etme...```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=285336877))
            await event.client.send_message(chat, "{}".format(input_str))
            response = await response
        except YouBlockedUserError:
            await event.reply("@Vixtbot üzerindeki engellemeyi kaldır")
            return
        if response.text.startswith("Onu bulamıyorum"):
            await event.edit("üzgünüm bulamıyorum")
        else:
            await event.delete()
            await borg.send_file(event.chat_id, response.message, reply_to=reply_to_id)


@borg.on(sudo_cmd(pattern="mash ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    chat = "@vixtbot"
    await event.delete()
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=285336877))
            await event.client.send_message(chat, "{}".format(input_str))
            response = await response
        except YouBlockedUserError:
            await event.reply("@Vixtbot üzerindeki engellemeyi kaldır")
            return
        if response.text.startswith("Onu bulamıyorum"):
            await event.reply("üzgünüm bulamıyorum")
        else:
            await event.delete()
            await borg.send_file(event.chat_id, response.message, reply_to=reply_to_id)


CMD_HELP.update({"mashup": "**PLUGİN İSMİ:** `mashup`\
      \n\n**📌Komut ➥ **`.mash` <metin> :\
      \n**Kullanım ➥ ** Size verilen metnin ilgili video mesajını gönderir."
                 })
