# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import re
from .. import CMD_HELP
from telethon import events
import userbot.plugins.sql_helper.blacklist_sql as sql
from ..utils import admin_cmd, sudo_cmd, edit_or_reply


@borg.on(events.NewMessage(incoming=True))
async def on_new_message(event):
    # TODO: Yöneticileri kilitlerden muaf tutma
    name = event.raw_text
    snips = sql.get_chat_blacklist(event.chat_id)
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
            except Exception:
                await event.reply("Bu sohbette SİLME iznim yok")
                sql.rm_from_blacklist(event.chat_id, snip.lower())
            break


@borg.on(admin_cmd(pattern="addblacklist ((.|\n)*)"))
@borg.on(sudo_cmd(pattern="addblacklist ((.|\n)*)", allow_sudo=True))
async def on_add_black_list(event):
    text = event.pattern_match.group(1)
    to_blacklist = list(set(trigger.strip()
                            for trigger in text.split("\n") if trigger.strip()))
    for trigger in to_blacklist:
        sql.add_to_blacklist(event.chat_id, trigger.lower())
    await edit_or_reply(event, "`Mevcut sohbette kara listeye {} kelime eklendi`".format(len(to_blacklist)))


@borg.on(admin_cmd(pattern="rmblacklist ((.|\n)*)"))
@borg.on(sudo_cmd(pattern="rmblacklist ((.|\n)*)", allow_sudo=True))
async def on_delete_blacklist(event):
    text = event.pattern_match.group(1)
    to_unblacklist = list(set(trigger.strip()
                              for trigger in text.split("\n") if trigger.strip()))
    successful = 0
    for trigger in to_unblacklist:
        if sql.rm_from_blacklist(event.chat_id, trigger.lower()):
            successful += 1
    await edit_or_reply(event, f"{successful} / {len (to_unblacklist)} `Kelime kara listeden kaldırıldı`")


@borg.on(admin_cmd(pattern="listblacklist$"))
@borg.on(sudo_cmd(pattern="listblacklist$", allow_sudo=True))
async def on_view_blacklist(event):
    all_blacklisted = sql.get_chat_blacklist(event.chat_id)
    OUT_STR = "`Mevcut Sohbetteki Kara Listeye Alınmış Kelimeler`:\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"👉 {trigger} \n"
    else:
        OUT_STR = "Kara Liste Yok. `.addblacklist` kullanarak Kaydetmeye başlayın"
    if len(OUT_STR) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "blacklist.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Mevcut Sohbetteki Kara Listeler",
                reply_to=event
            )
            await event.delete()
    else:
        await edit_or_reply(event, OUT_STR)


CMD_HELP.update({"blacklist": "**PLUGİN İSMİ:** `blacklist`\
      \n\n**📌Komut ➥ **`.addblacklist` <kelime/kelimeler> :\
      \n**Kullanım ➥ ** Verilen kelime veya kelimeler söz konusu sohbette kara listeye eklenecektir, eğer herhangi bir kullanıcı gönderirse mesaj silinir.\
      \n\n**📌Komut ➥ **`rmblacklist` <kelime/kelimeler> :\
      \n**Kullanım ➥ ** Söz konusu sohbette verilen kelime veya kelimeler kara listeden kaldırılacaktır.\
      \n\n**📌Komut ➥ ** `.listblacklist`\
      \n**Kullanım ➥ ** Belirli bir sohbette size kara liste kelimelerinin listesini gösterir.\
      \n\n**Not: ** bununla aynı anda birden fazla kelime ekliyorsanız, yeni satırda [merhaba merhaba] olmayan yeni kelimenin verilmesi gerektiğini unutmayın. şu şekilde olmalı\
      \n[merhaba \n merhaba]"
                 })
