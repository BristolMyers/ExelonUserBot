# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from .. import CMD_HELP
from telethon.tl import functions
from ..utils import admin_cmd, sudo_cmd, edit_or_reply


@borg.on(admin_cmd(pattern="create (b|g|c) (.*)"))  # pylint:disable=E0602
@borg.on(sudo_cmd(pattern="create (b|g|c) (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    type_of_group = event.pattern_match.group(1)
    group_name = event.pattern_match.group(2)
    event = await edit_or_reply(event, "Oluşturuluyor......")
    if type_of_group == "b":
        try:
            result = await borg(functions.messages.CreateChatRequest(  # pylint:disable=E0602
                users=["@sarah_robot"],
                # Not enough users (to create a chat, for example)
                # Telegram, no longer allows creating a chat with ourselves
                title=group_name
            ))
            created_chat_id = result.chats[0].id
            await borg(functions.messages.DeleteChatUserRequest(
                chat_id=created_chat_id,
                user_id="@sarah_robot"
            ))
            result = await borg(functions.messages.ExportChatInviteRequest(
                peer=created_chat_id,
            ))
            await event.edit("`{}` `Grubu başarıyla oluşturuldu. Katılmak için` {}".format(group_name, result.link))
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
    elif type_of_group == "g" or type_of_group == "c":
        try:
            r = await borg(functions.channels.CreateChannelRequest(  # pylint:disable=E0602
                title=group_name,
                about="Bu @BristolMyers tarafından yapılan bir Testtir",
                megagroup=False if type_of_group == "c" else True
            ))
            created_chat_id = r.chats[0].id
            result = await borg(functions.messages.ExportChatInviteRequest(
                peer=created_chat_id,
            ))
            await event.edit("`{}` `Grubu başarıyla oluşturuldu. Katılmak için` {}".format(group_name, result.link))
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
    else:
        await event.edit("Beni nasıl kullanacağımı öğrenmek için .info create i okuyun")


CMD_HELP.update({"create": "**PLUGİN İSMİ:** `create`\
      \n\n**📌Komut ➥ **`.create b (grupadı)` :\
      \n**Kullanım ➥ ** Bir süper grup oluşturur ve size bağlantı gönderir.\
      \n\n**📌Komut ➥ **`.create g(grupadı)` :\
      \n**Kullanım ➥ ** Özel bir grup oluşturur ve size bağlantı gönderir.\
      \n\n**📌Komut ➥ ** `.create c(grupadı)`\
      \n**Kullanım ➥ ** Bir Kanal oluşturur ve size bağlantı gönderir.\
      \n\nburada bot hesabı sahibi"
                 })
