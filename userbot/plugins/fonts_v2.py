# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from userbot import CMD_HELP, fonts
from userbot.utils import admin_cmd
import random


@borg.on(admin_cmd(pattern="egyptf(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await event.edit("Neyi değiştirmem gerekiyor, metin ver")
        return
    string = '  '.join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            egyptfontcharacter = fonts.egyptfontfont[fonts.normaltext.index(
                normaltextcharacter)]
            string = string.replace(normaltextcharacter, egyptfontcharacter)
    await event.edit(string)


@borg.on(admin_cmd(pattern="maref(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await event.edit("Neyi değiştirmem gerekiyor, metin ver")
        return
    string = '  '.join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            nightmarecharacter = fonts.nightmarefont[fonts.normaltext.index(
                normaltextcharacter)]
            string = string.replace(normaltextcharacter, nightmarecharacter)
    await event.edit(string)


@borg.on(admin_cmd(pattern="handcf(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await event.edit("Neyi değiştirmem gerekiyor, metin ver")
        return
    string = '  '.join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            hwcapitalcharacter = fonts.hwcapitalfont[fonts.normaltext.index(
                normaltextcharacter)]
            string = string.replace(normaltextcharacter, hwcapitalcharacter)
    await event.edit(string)


@borg.on(admin_cmd(pattern="doublef(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await event.edit("Neyi değiştirmem gerekiyor, metin ver")
        return
    string = '  '.join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            doubletextcharacter = fonts.doubletextfont[fonts.normaltext.index(
                normaltextcharacter)]
            string = string.replace(normaltextcharacter, doubletextcharacter)
    await event.edit(string)


@borg.on(admin_cmd(pattern="mock(?: |$)(.*)"))
async def spongemocktext(mock):
    """ Do it and find the real fun. """
    if not mock.text[0].isalpha() and mock.text[0] not in ("/", "#", "@", "!"):
        reply_text = list()
        textx = await mock.get_reply_message()
        message = mock.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await mock.edit("`gIvE sOMEtHInG tO MoCk!`")
            return

        for charac in message:
            if charac.isalpha() and random.randint(0, 1):
                to_app = charac.upper() if charac.islower() else charac.lower()
                reply_text.append(to_app)
            else:
                reply_text.append(charac)

        await mock.edit("".join(reply_text))


@borg.on(admin_cmd(pattern="ghostf(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await event.edit("Neyi değiştirmem gerekiyor, metin ver")
        return
    string = '  '.join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            ghostfontcharacter = fonts.ghostfontfont[fonts.normaltext.index(
                normaltextcharacter)]
            string = string.replace(normaltextcharacter, ghostfontcharacter)
    await event.edit(string)


@borg.on(admin_cmd(pattern="handsf(?: |$)(.*)"))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await event.edit("Neyi değiştirmem gerekiyor, metin ver")
        return
    string = '  '.join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            hwslcharacter = fonts.hwslfont[fonts.normaltext.index(
                normaltextcharacter)]
            string = string.replace(normaltextcharacter, hwslcharacter)
    await event.edit(string)


CMD_HELP.update({"fonts_v2": "**PLUGİN İSMİ:** `fonts_v2`:\
      \n\n**📌Komut ➥ **`.mock (metin) veya .mock mesaja yanıt`\
      \n**Kullanım ➥ ** verilen metinde rastgele büyük ve küçük harfler.\
      \n**📌EXTRA YAZI TİPİ KOMUTLARI:** `.handsf .ghostf .doublef .handcf .egyptf .maref`"
                 })
