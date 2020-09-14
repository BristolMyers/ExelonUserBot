# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
import asyncio
from userbot.utils import admin_cmd
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon import events
import logging
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING)


@borg.on(admin_cmd(pattern=("sg ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Herhangi bir kullanıcı mesajını yanıtlayın.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("```kısa mesajı yanıtla```")
        return
    chat = "@SangMataInfo_bot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("```Gerçek kullanıcıların mesajını yanıtlayın.```")
        return
    await event.edit("```İşleniyor```")
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=461843263))
            await borg.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Lütfen @sangmatainfo_bot engellemesini kaldırın ve tekrar deneyin```")
            return
        if response.text.startswith("Forward"):
            await event.edit("Kullanıcı gizlilik ayarlarını etkinleştirdi, ad geçmişini alamazsınız")
        else:
            await event.edit(f"{response.message.message}")


@borg.on(admin_cmd(pattern=("fakemail ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    chat = "@fakemailbot"
    await event.edit("```Fakemail Oluşturuluyor, bekleyin```")
    async with borg.conversation(chat) as conv:
        try:
            await event.client.send_message("@fakemailbot", "/generate")
            await asyncio.sleep(5)
            k = await event.client.get_messages(entity="@fakemailbot", limit=1, reverse=False)
            mail = k[0].text
            # print(k[0].text)
        except YouBlockedUserError:
            await event.reply("```Lütfen @fakemailbot engelini kaldırın ve tekrar deneyin```")
            return
        await event.edit(mail)


@borg.on(admin_cmd(pattern=("mailid ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    chat = "@fakemailbot"
    await event.edit("``Fakemail listesi alınıyor```")
    async with borg.conversation(chat) as conv:
        try:
            await event.client.send_message("@fakemailbot", "/id")
            await asyncio.sleep(5)
            k = await event.client.get_messages(entity="@fakemailbot", limit=1, reverse=False)
            mail = k[0].text
            # print(k[0].text)
        except YouBlockedUserError:
            await event.reply("```Lütfen @fakemailbot engelini kaldırın ve tekrar deneyin```")
            return
        await event.edit(mail)


@borg.on(admin_cmd(pattern=("ub ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Herhangi bir kullanıcı mesajını yanıtlayın.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("```kısa mesajı yanıtla```")
        return
    chat = "@uploadbot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("```Gerçek kullanıcıların mesajını yanıtlayın.```")
        return
    await event.edit("```İşleniyor```")
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=97342984))
            await borg.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Lütfen @uploadbot engelini kaldırın ve tekrar deneyin```")
            return
        if response.text.startswith("Selam!,"):
            await event.edit("```ileri gizlilik ayarlarınızı tamamen devre dışı bırakabilir misiniz?```")
        else:
            await event.edit(f"{response.message.message}")


@borg.on(admin_cmd(pattern=("gid ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Herhangi bir kullanıcı mesajını yanıtlayın.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("```kısa mesajı yanıtla```")
        return
    chat = "@getidsbot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("```Gerçek kullanıcıların mesajını yanıtlayın.```")
        return
    await event.edit("```İşleniyor```")
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=186675376))
            await borg.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```botu engelledin```")
            return
        if response.text.startswith("Selam,"):
            await event.edit("```ileri gizlilik ayarlarınızı tamamen devre dışı bırakabilir misiniz?```")
        else:
            await event.edit(f"{response.message.message}")
