# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import asyncio
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChannelParticipantsAdmins
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="gbun"))
async def gbun(event):
    if event.fwd_from:
        return
    gbunVar = event.text
    gbunVar = gbunVar[6:]
    mentions = "`Uyarı! Kullanıcı Yönetici Tarafından 𝙂𝘽𝘼𝙉 Yedi...\n`"
    no_reason = "__Neden: Yönetici Öyle İstedi. __"
    await event.edit("**@ExelonUserBot ❗️⚜️☠️**")
    await asyncio.sleep(3.5)
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(reply_message.from_id))
        firstname = replied_user.user.first_name
        usname = replied_user.user.username
        idd = reply_message.from_id
        # make meself invulnerable cuz why not xD
        if idd == 1035034432:
            await reply_message.reply("`Bekle bir saniye, bu benim ustam!`\n**Usta zencimi yasaklamakla nasıl tehdit edersin!**\n\n__Hesabınız saldırıya uğradı! hesabınızı serbest bırakmak için Ustama[BristolMyers](tg://user?id=1012994299) 69 $ öde__😏")
        else:
            jnl = ("`Uyarı!! `"
                   "[{}](tg://user?id={})"
                   "` 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 Admin tarafından...\n\n`"
                   "**Kullanıcı Adı: ** __{}__\n"
                   "**ID : ** `{}`\n"
                   ).format(firstname, idd, firstname, idd)
            if usname is None:
                jnl += "**Kurban Nigga'nın kullanıcı adı: ** `Kullanıcı adı yok!`\n"
            else:
                jnl += "**Kurban Nigga'nın kullanıcı adı** : @{}\n".format(
                    usname)
            if len(gbunVar) > 0:
                gbunm = "`{}`".format(gbunVar)
                gbunr = "**Nedeni: **" + gbunm
                jnl += gbunr
            else:
                jnl += no_reason
            await reply_message.reply(jnl)
    else:
        mention = "`Uyarı!! Kullanıcı 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 Yönetici Tarafından...\nNedeni: Admin öyle istedi. `"
        await event.reply(mention)
    await event.delete()
