# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from userbot.utils import admin_cmd
from telethon.tl.types import ChannelParticipantsAdmins


@borg.on(admin_cmd(pattern="tagall$"))
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    mentions = "@all"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await reply_to_id.reply(mentions)
    await event.delete()


@borg.on(admin_cmd(pattern="all (.*)"))
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.edit("Nasıl Yapmalısınız. `.all Buraya Gelin`.")

    mentions = input_str
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await reply_to_id.reply(mentions)
    await event.delete()


@borg.on(admin_cmd(pattern="admins$"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "@admin: **Spam Tespit Edildi**"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f"[\u2063](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


@borg.on(admin_cmd(pattern="men (.*)"))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        input_str = event.pattern_match.group(1)
        reply_msg = await event.get_reply_message()
        caption = """<a href='tg://user?id={}'>{}</a>""".format(
            reply_msg.from_id, input_str)
        await event.delete()
        await borg.send_message(event.chat_id, caption, parse_mode="HTML")
    else:
        await event.edit("Kullanıcıdan bahsetmek için `.mention <istediğin mesaj>`")
