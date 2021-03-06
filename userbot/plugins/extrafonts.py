# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from .. import CMD_HELP, fonts
from ..utils import admin_cmd, sudo_cmd, edit_or_reply


@borg.on(admin_cmd(pattern="fmusical(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="fmusical(?: |$)(.*)", allow_sudo=True))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "Neyi değiştirmem gerekiyor, metin ver")
        return
    string = '  '.join(args).lower()
    for normalfontcharacter in string:
        if normalfontcharacter in fonts.normalfont:
            musicalcharacter = fonts.musicalfont[fonts.normalfont.index(
                normalfontcharacter)]
            string = string.replace(normalfontcharacter, musicalcharacter)
    await edit_or_reply(event, string)


@borg.on(admin_cmd(pattern="ancient(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="ancient(?: |$)(.*)", allow_sudo=True))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "Neyi değiştirmem gerekiyor, metin ver")
        return
    string = '  '.join(args).lower()
    for normalfontcharacter in string:
        if normalfontcharacter in fonts.normalfont:
            ancientcharacter = fonts.ancientfont[fonts.normalfont.index(
                normalfontcharacter)]
            string = string.replace(normalfontcharacter, ancientcharacter)
    await edit_or_reply(event, string)


CMD_HELP.update({"extrafonts": "**PLUGİN İSMİ:** `extrafonts`\
      \n\n**📌Komut ➥ **`.fmusical - .ancient ` :\
      \n**Kullanım ➥ ** Bazı farklı yazı tipi stilleri.\
      "
                 })
