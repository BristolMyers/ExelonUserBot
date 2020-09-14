# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

"""Kentsel Sözlük / Kelime Bulma Modülü."""

import asyncurban
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="ud (.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("İşleniyor...")
    word = event.pattern_match.group(1)
    urban = asyncurban.UrbanDictionary()
    try:
        mean = await urban.get_word(word)
        await event.edit("Metin: **{}**\n\nAnlamı: **{}**\n\nÖrnek: __{}__".format(mean.word, mean.definition, mean.example))
    except asyncurban.WordNotFoundError:
        await event.edit("Şu kelime hakkında bir bilgi toplayamadım! : **" + word + "**")
