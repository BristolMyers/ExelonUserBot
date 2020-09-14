# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import re
import asyncio
from .. import CMD_HELP
from telethon.tl import types
from telethon import utils
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from userbot.plugins.sql_helper.filter_sql import add_filter, get_all_filters, remove_all_filters, remove_filter

DELETE_TIMEOUT = 0
TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2

global last_triggered_filters
last_triggered_filters = {}  # pylint:disable=E0602


@command(incoming=True)
async def on_snip(event):
    global last_triggered_filters
    name = event.raw_text
    if event.chat_id in last_triggered_filters:
        if name in last_triggered_filters[event.chat_id]:
            # avoid userbot spam
            # "I demand rights for us bots, we are equal to you humans." -Henri Koivuneva (t.me/UserbotTesting/2698)
            return False
    snips = get_all_filters(event.chat_id)
    if snips:
        for snip in snips:
            pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"
            if re.search(pattern, name, flags=re.IGNORECASE):
                if snip.snip_type == TYPE_PHOTO:
                    media = types.InputPhoto(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference
                    )
                elif snip.snip_type == TYPE_DOCUMENT:
                    media = types.InputDocument(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference
                    )
                else:
                    media = None
                event.message.id
                if event.reply_to_msg_id:
                    event.reply_to_msg_id
                await event.reply(
                    snip.reply,
                    file=media
                )
                if event.chat_id not in last_triggered_filters:
                    last_triggered_filters[event.chat_id] = []
                last_triggered_filters[event.chat_id].append(name)
                await asyncio.sleep(DELETE_TIMEOUT)
                last_triggered_filters[event.chat_id].remove(name)


@borg.on(admin_cmd(pattern="filter (.*)"))
@borg.on(sudo_cmd(pattern="filter (.*)", allow_sudo=True))
async def on_snip_save(event):
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if msg:
        snip = {'type': TYPE_TEXT, 'text': msg.message or ''}
        if msg.media:
            media = None
            if isinstance(msg.media, types.MessageMediaPhoto):
                media = utils.get_input_photo(msg.media.photo)
                snip['type'] = TYPE_PHOTO
            elif isinstance(msg.media, types.MessageMediaDocument):
                media = utils.get_input_document(msg.media.document)
                snip['type'] = TYPE_DOCUMENT
            if media:
                snip['id'] = media.id
                snip['hash'] = media.access_hash
                snip['fr'] = media.file_reference
        add_filter(
            event.chat_id,
            name,
            snip['text'],
            snip['type'],
            snip.get('id'),
            snip.get('hash'),
            snip.get('fr'))
        await edit_or_reply(event, f"filtre {name} başarıyla kaydedildi. {Name} ile alın")
    else:
        await edit_or_reply(event, "Filtreyi kaydetmek için 'kaydedici filtre anahtar kelimesi` ile bir mesajı yanıtlayın")


@borg.on(admin_cmd(pattern="filters$"))
@borg.on(sudo_cmd(pattern="filters$", allow_sudo=True))
async def on_snip_list(event):
    all_snips = get_all_filters(event.chat_id)
    OUT_STR = "Mevcut Sohbette Kullanılabilir Filtreler:\n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f"👉 {a_snip.keyword} \n"
    else:
        OUT_STR = "Filtre yok `.Savefilter` kullanarak Kaydetmeye başlayın"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "filters.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Mevcut Sohbette Kullanılabilir Filtreler",
                reply_to=event
            )
            await event.delete()
    else:
        await edit_or_reply(event, OUT_STR)


@borg.on(admin_cmd(pattern="stop (.*)"))
@borg.on(sudo_cmd(pattern="stop (.*)", allow_sudo=True))
async def on_snip_delete(event):
    name = event.pattern_match.group(1)
    remove_filter(event.chat_id, name)
    await edit_or_reply(event, f"filtre {name} başarıyla silindi")


@borg.on(admin_cmd(pattern="rmfilters$"))
@borg.on(sudo_cmd(pattern="rmfilters$", allow_sudo=True))
async def on_all_snip_delete(event):
    remove_all_filters(event.chat_id)
    await edit_or_reply(event, f"filtreler ** mevcut sohbette ** başarıyla silindi")


CMD_HELP.update({"filter": "**PLUGİN İSMİ:** `filter`\
      \n\n**📌Komut ➥ **`.filters` :\
      \n**Kullanım ➥ ** Bir sohbetteki tüm userbot filtrelerini listeler.\
      \n\n**📌Komut ➥ **.filter <filtrelenecek kelime> <cevaplanacak metin> ya da bir mesajı .filter <filtrelenecek kelime>\
      \n**Kullanım ➥ ** 'filtrelenecek kelime' olarak istenilen şeyi kaydeder.\
      \nDosyalardan çıkartmalara her türlü şeyle çalışır.\
      \n\n**📌Komut ➥ **`.stop <filtre>` :\
      \n**Kullanım ➥ ** Seçilen filtreyi durdurur.\
      \n\n**📌Komut ➥ **`.rmfilters` :\
      \n**Kullanım ➥ ** Grup yönetimi botlarındaki tüm filtreleri temizler."
                 })
