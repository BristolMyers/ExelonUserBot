# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import os
import glob
import pybase64
from .. import CMD_HELP
from . import exelonmusic, exelonmusicvideo
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from telethon.tl.functions.messages import ImportChatInviteRequest as Get


@borg.on(admin_cmd(pattern="song( (.*)|$)"))
@borg.on(sudo_cmd(pattern="song( (.*)|$)", allow_sudo=True))
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.messag
    else:
        event = await edit_or_reply(event, "`Ne bulmam gerekiyor `")
        return
    event = await edit_or_reply(event, "`Exelon ..! Senin şarkını buluyor....`")
    try:
        exelon = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        exelon = Get(exelon)
        await event.client(exelon)
    except BaseException:
        pass
    await exelonmusic(str(query), "128k", event)
    l = glob.glob("./temp/*.mp3")
    if l:
        await event.edit("Evet..! bir şey buldum..🥰")
    else:
        await event.edit(f"Afedersiniz..! `{query}` ile hiçbir şey bulamıyorum")
        return
    thumbexelon = glob.glob("./temp/*.jpg") + glob.glob("./temp/*.webp")
    if thumbexelon:
        exelonthumb = thumbexelon[0]
    else:
        exelonthumb = None
    loa = l[0]
    await borg.send_file(
        event.chat_id,
        loa,
        force_document=False,
        allow_cache=False,
        caption=query,
        thumb=exelonthumb,
        supports_streaming=True,
        reply_to=reply_to_id
    )
    await event.delete()
    os.system("rm -rf ./temp/*.mp3")
    os.system("rm -rf ./temp/*.jpg")
    os.system("rm -rf ./temp/*.webp")


@borg.on(admin_cmd(pattern="song320( (.*)|$)"))
@borg.on(sudo_cmd(pattern="song320( (.*)|$)", allow_sudo=True))
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.message
    else:
        event = await edit_or_reply(event, "`Ne bulmam gerekiyor `")
        return
    event = await edit_or_reply(event, "`Exelon ..! Senin şarkını buluyor....`")
    try:
        exelon = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        exelon = Get(exelon)
        await event.client(exelon)
    except BaseException:
        pass
    await exelonmusic(str(query), "320k", event)
    l = glob.glob("./temp/*.mp3")
    if l:
        await event.edit("Evet..! bir şey buldum..🥰")
    else:
        await event.edit(f"Afedersiniz..! `{query}` ile hiçbir şey bulamıyorum")
        return
    thumbexelon = glob.glob("./temp/*.jpg") + glob.glob("./temp/*.webp")
    if thumbexelon:
        exelonthumb = thumbexelon[0]
    else:
        exelonthumb = None
    loa = l[0]
    await borg.send_file(
        event.chat_id,
        loa,
        force_document=False,
        allow_cache=False,
        caption=query,
        thumb=exelonthumb,
        supports_streaming=True,
        reply_to=reply_to_id
    )
    await event.delete()
    os.system("rm -rf ./temp/*.mp3")
    os.system("rm -rf ./temp/*.jpg")
    os.system("rm -rf ./temp/*.webp")


@borg.on(admin_cmd(pattern="vsong( (.*)|$)"))
@borg.on(sudo_cmd(pattern="vsong( (.*)|$)", allow_sudo=True))
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.messag
    else:
        event = await edit_or_reply(event, "Ne bulmam gerekiyor")
        return
    event = await edit_or_reply(event, "Exelon Video şarkını buluyor....")
    await exelonmusicvideo(query, event)
    try:
        exelon = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        exelon = Get(exelon)
        await event.client(exelon)
    except BaseException:
        pass
    l = glob.glob(("./temp/*.mp4"))
    if l:
        await event.edit("Evet..! bir şey buldum..🥰")
    else:
        await event.edit(f"Afedersiniz..! `{query}` ile hiçbir şey bulamıyorum")
        return
    thumbexelon = glob.glob("./temp/*.jpg") + glob.glob("./temp/*.webp")
    if thumbexelon:
        exelonthumb = thumbexelon[0]
    else:
        exelonthumb = None
    loa = l[0]
    await borg.send_file(
        event.chat_id,
        loa,
        thumb=exelonthumb,
        caption=query,
        supports_streaming=True,
        reply_to=reply_to_id
    )
    await event.delete()
    os.system("rm -rf ./temp/*.mp4")
    os.system("rm -rf ./temp/*.jpg")
    os.system("rm -rf ./temp/*.webp")

CMD_HELP.update({"getmusic": "**PLUGİN İSMİ:** `getmusic`\
      \n\n**📌Komut ➥ **`.song` query or `.song` şarkı adına cevap ver :\
      \n**Kullanım ➥ ** sorguya girdiğiniz şarkıyı bulur ve gönderir."
                 })
