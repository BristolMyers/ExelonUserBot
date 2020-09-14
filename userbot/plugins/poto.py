# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""
----------------------------------------------------------------
Tüm Thenks Emily'ye gider (Bu Eklentinin yaratıcısı)
\nand `SnapDragon for` Helping me.
----------------------------------------------------------------

Type `.poto` for get ** O Kullanıcının tüm profil resimleri**
\nOr type `.poto (number)` **bir Kullanıcının istenen sayıda fotoğrafını almak için** .
"""

import logging
from userbot.utils import admin_cmd
import asyncio
logger = logging.getLogger(__name__)

if 1 == 1:
    name = "Profile Photos"
    client = borg

    @borg.on(admin_cmd(pattern="poto ?(.*)"))
    async def potocmd(event):
        """Yanıtlanan kullanıcıların, kanalların veya sohbetlerin profil fotoğraflarını alır"""
        id = "".join(event.raw_text.split(maxsplit=2)[1:])
        user = await event.get_reply_message()
        chat = event.input_chat
        if user:
            photos = await event.client.get_profile_photos(user.sender)
            u = True
        else:
            photos = await event.client.get_profile_photos(chat)
            u = False
        if id.strip() == "":
            id = 1
            if int(id) <= (len(photos)):
                send_photos = await event.client.download_media(photos[id - 1])
                await event.client.send_file(event.chat_id, send_photos)
            else:
                await event.edit("Bu NIBBA / NIBBI için fotoğraf bulunamadı. Şimdi Geber!")
                await asyncio.sleep(2)
                return
        elif id.strip() == "all":
            if len(photos) > 0:
                await event.client.send_file(event.chat_id, photos)
            else:
                try:
                    if u is True:
                        photo = await event.client.download_profile_photo(user.sender)
                    else:
                        photo = await event.client.download_profile_photo(event.input_chat)
                    await event.client.send_file(event.chat_id, photo)
                except a:
                    await event.edit("**Bu kullanıcının hiç fotoğrafı yok!**")
                    return
        else:
            try:
                id = int(id)
                if id <= 0:
                    await event.edit("```numara Geçersiz!``` *Sen benimle dalgamı geçiyorsun ?**")
                    return
            except BaseException:
                await event.edit("Sen benimle dalgamı geçiyorsun ?")
                return
            if int(id) <= (len(photos)):
                send_photos = await event.client.download_media(photos[id - 1])
                await event.client.send_file(event.chat_id, send_photos)
            else:
                await event.edit("Bu NIBBA / NIBBI için fotoğraf bulunamadı. Şimdi Geber!")
                await asyncio.sleep(2)
                return
