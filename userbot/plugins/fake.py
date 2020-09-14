# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from telethon.tl.functions.channels import EditAdminRequest
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from telethon.tl.types import ChatAdminRights
from .. import CMD_HELP, ALIVE_NAME
from datetime import datetime
import logging
import asyncio


logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING)

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "exelon"


@borg.on(admin_cmd(pattern="scam ?(.*)"))
@borg.on(sudo_cmd(pattern="scam ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    action = "yazıyor"
    if input_str:
        action = input_str
    try:
        await event.delete()
    except BaseException:
        pass
    async with borg.action(event.chat_id, action):
        await asyncio.sleep(86400)  # type for 10 seconds


@borg.on(admin_cmd(pattern="prankpromote ?(.*)"))
@borg.on(sudo_cmd(pattern="prankpromote ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    datetime.now()
    to_promote_id = None
    rights = ChatAdminRights(
        post_messages=True
    )
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.message.id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_promote_id = r_mesg.sender_id
    elif input_str:
        to_promote_id = input_str
    try:
        await borg(EditAdminRequest(event.chat_id, to_promote_id, rights, ""))
    except (Exception) as exc:
        await edit_or_reply(event, str(exc))
    else:
        await edit_or_reply(event, "Başarıyla Tanıtıldı")


@borg.on(admin_cmd(pattern=f"padmin$", outgoing=True))
@borg.on(sudo_cmd(pattern="padmin$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 20)
    event = await edit_or_reply(event, "promoting.......")
    animation_chars = [
        "**Promoting User As Admin...**",
        "**Enabling All Permissions To User...**",
        "**(1) Send Messages: ☑️**",
        "**(1) Send Messages: ✅**",
        "**(2) Send Media: ☑️**",
        "**(2) Send Media: ✅**",
        "**(3) Send Stickers & GIFs: ☑️**",
        "**(3) Send Stickers & GIFs: ✅**",
        "**(4) Send Polls: ☑️**",
        "**(4) Send Polls: ✅**",
        "**(5) Embed Links: ☑️**",
        "**(5) Embed Links: ✅**",
        "**(6) Add Users: ☑️**",
        "**(6) Add Users: ✅**",
        "**(7) Pin Messages: ☑️**",
        "**(7) Pin Messages: ✅**",
        "**(8) Change Chat Info: ☑️**",
        "**(8) Change Chat Info: ✅**",
        "**Permission Granted Successfully**",
        f"**pRoMooTeD SuCcEsSfUlLy bY: {DEFAULTUSER}**"
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 20])


CMD_HELP.update({"fake": "**PLUGİN İSMİ:** `fake`\
      \n\n**📌Komut ➥ **`.scam <eylem adı>` :\
      \n**Kullanım ➥ ** .scam (eylem adı) yazın bu, eylemlerin yazdığı, kişi, oyun, konum, ses, tur, video, fotoğraf, belge, iptal gibi gruptaki sahte eylemi gösterir.\
      \n\n**📌Komut ➥ **`.prankpromote` şaka yapmak istediğiniz kullanıcıya cevap verin` :\
      \n**Kullanım➥** onu yönetici konumuna yükseltir, ancak herhangi bir işlem yapma izni olmayacak, yani önerme işlemlerini görebilecek ancak herhangi bir yönetici işlemi yapamayacaktır.\
      \n\n**📌Komut➥** `.padmin`\
      \n**Kullanım ➥ ** Yönetici olduğu için ona tüm izinleri etkinleştirdiğini gösteren bir animasyon (sahte tanıtım).\ "
                 })
