# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.utils import admin_cmd, sudo_cmd
from userbot import CMD_HELP


@borg.on(admin_cmd(pattern="recognize ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("Herhangi bir kullanıcının medya mesajını yanıtlayın.")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("medya dosyasına cevap ver")
        return
    chat = "@Rekognition_Bot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("Gerçek kullanıcıların mesajını yanıtlayın.")
        return
    exelon = await event.edit("bu medyayı tanıyor")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=461083923))
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("@Rekognition_Bot engelini kaldırın ve tekrar deneyin")
            await exelon.delete()
            return
        if response.text.startswith("Sonraki mesaja bakın."):
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=461083923))
            response = await response
            exelon = response.message.message
            await event.edit(exelon)

        else:
            await event.edit("sorry, I couldnt find it")


@borg.on(sudo_cmd(pattern="recognize ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("Herhangi bir kullanıcının medya mesajını yanıtlayın.")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.reply("medya dosyasına cevap ver")
        return
    chat = "@Rekognition_Bot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.reply("Gerçek kullanıcıların mesajını yanıtlayın.")
        return
    exelon = await event.reply("bu medyayı tanıyor")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=461083923))
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("@Rekognition_Bot engelini kaldırın ve tekrar deneyin")
            await exelon.delete()
            return
        if response.text.startswith("Sonraki mesaja bakın."):
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=461083923))
            response = await response
            exelon = response.message.message
            await event.reply(exelon)
            await exelon.delete()
        else:
            await event.reply("üzgünüm bulamadım")
            await exelon.delete()

CMD_HELP.update({
    "recognize":
    "`**📌Komut ➥ **.recognize` bunu herhangi bir medya dosyasına cevapla\
    \n**Kullanım ➥ ** AWS Rekognition kullanarak bir görüntü hakkında bilgi alın.\
    \n➥ Algılanan etiketler, yüzler dahil olmak üzere bilgileri bulun. metin ve denetleme etiketleri."
})
