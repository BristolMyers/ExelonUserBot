# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import asyncio
from .. import CMD_HELP
from telethon.tl.types import ChatBannedRights
import userbot.plugins.sql_helper.antiflood_sql as sql
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from telethon.tl.functions.channels import EditBannedRequest

CHAT_FLOOD = sql.__load_flood_settings()
# sel önleme için uyarı modu
ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=True
)


@borg.on(admin_cmd(incoming=True))
async def _(event):
    if not CHAT_FLOOD:
        return
    if not (str(event.chat_id) in CHAT_FLOOD):
        return
    should_ban = sql.update_flood(event.chat_id, event.message.from_id)
    if not should_ban:
        return
    try:
        await event.client(EditBannedRequest(
            event.chat_id,
            event.message.from_id,
            ANTI_FLOOD_WARN_MODE
        ))
    except Exception as e:  # pylint:disable=C0103,W0703
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message="""**Otomatik AntiFlooder**
@admin [User](tg://user?id={}) bu sohbeti floodluyor.
`{}`""".format(event.message.from_id, str(e)),
            reply_to=event.message.id
        )
        await asyncio.sleep(10)
        await no_admin_privilege_message.edit(
            "Bu işe yaramaz SPAM dostum. kes şunu sohbet et dostum ",
            link_preview=False
        )
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message="""**Otomatik AntiFlooder**
[User](tg://user?id={}) otomatik olarak kısıtlandı
çünkü tanımlanan flood sınırına ulaştı.""".format(event.message.from_id),
            reply_to=event.message.id
        )


@borg.on(admin_cmd(pattern="setflood(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="setflood(?: |$)(.*)", allow_sudo=True))
async def _(event):
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event, "flood ayarlarını güncelleme!")
    try:
        sql.set_flood(event.chat_id, input_str)
        sql.__load_flood_settings()
        await event.edit("Antiflood, mevcut sohbette {} olarak güncellendi".format(input_str))
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))


CMD_HELP.update({"antiflood": "**PLUGİN İSMİ:** `antiflood`\
      \n\n**📌Komut ➥ **`.setflood [number]` :\
      \n**Kullanım ➥ ** Eğer yönetici iseniz sohbeti spam yaparsa kullanıcıyı uyarır, o grupta onu sessize alır."
                 })
