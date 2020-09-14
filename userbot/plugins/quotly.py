# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from ..utils import admin_cmd, sudo_cmd
import os
from .. import process


@borg.on(admin_cmd(pattern="q(?: |$)(.*)"))
async def stickerchat(exelonquotes):
    if exelonquotes.fwd_from:
        return
    reply = await exelonquotes.get_reply_message()
    if not reply:
        await exelonquotes.edit("Mesajdan alıntı yapamıyorum. bir mesajı cevapla")
        return
    fetchmsg = reply.message
    repliedreply = await reply.get_reply_message()
    if reply.media:
        if reply.media.document.mime_type in ('mp4'):
            await exelonquotes.edit("animasyonlu çıkartmalar ve mp4 formatları desteklenmez")
            return
    await exelonquotes.delete()
    user = (await borg.get_entity(reply.forward.sender) if reply.fwd_from
            else reply.sender)
    res, exelonmsg = await process(fetchmsg, user, borg, reply, repliedreply)
    if not res:
        return
    exelonmsg.save('./temp/sticker.webp')
    await borg.send_file(exelonquotes.chat_id, "./temp/sticker.webp", reply_to=reply)
    os.remove('./temp/sticker.webp')


@borg.on(admin_cmd(pattern="qbot(?: |$)(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Herhangi bir kullanıcı mesajını yanıtlayın.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("```Kısa mesajı yanıtla```")
        return
    chat = "@QuotLyBot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("```Gerçek kullanıcıların mesajını yanıtlayın.```")
        return
    await event.edit("```Alıntı Yapmak```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=1031952739))
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Lütfen beni engellemeyi kaldır (@QuotLyBot) u Nigga```")
            return
        await borg.send_read_acknowledge(conv.chat_id)
        if response.text.startswith("Selam!"):
            await event.edit("```İleri gizlilik ayarlarınızı tamamen devre dışı bırakabilir misiniz?```")
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)


@borg.on(sudo_cmd(pattern="qbot(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("```Herhangi bir kullanıcı mesajını yanıtlayın.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.reply("```Kısa mesajı yanıtla```")
        return
    chat = "@QuotLyBot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.reply("```Gerçek kullanıcıların mesajını yanıtlayın.```")
        return
    exelon = await event.reply("```Alıntı Yapmak```")
    await borg.send_read_acknowledge(conv.chat_id)
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=1031952739))
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Lütfen beni engellemeyi kaldır (@QuotLyBot) u Nigga```")
            return
        if response.text.startswith("Hi!"):
            await event.reply("```İleri gizlilik ayarlarınızı tamamen devre dışı bırakabilir misiniz?```")
        else:
            await exelon.delete()
            await event.client.send_message(event.chat_id, response.message)
