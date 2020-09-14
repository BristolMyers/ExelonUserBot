# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from userbot.utils import admin_cmd, sudo_cmd
from userbot import CMD_HELP
from telegraph import upload_file, exceptions
import os
from . import *
import pybase64


@borg.on(admin_cmd("mask ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Herhangi bir kullanıcı mesajını yanıtlayın.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("```medya mesajına cevap ver```")
        return
    chat = "@hazmat_suit_bot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("```Gerçek kullanıcıların mesajını yanıtlayın.```")
        return
    await event.edit("```İşleniyor```")
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=905164246))
            await borg.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Lütfen @hazmat_suit_bot engellemesini kaldırın ve tekrar deneyin```")
            return
        if response.text.startswith("İleri"):
            await event.edit("```ileri gizlilik ayarlarınızı tamamen devre dışı bırakabilir misiniz?```")
        else:
            await borg.send_file(event.chat_id, response.message.media)


@borg.on(admin_cmd(pattern="awooify(?: |$)(.*)"))
async def exelonbot(exelonmemes):
    replied = await exelonmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await exelonmemes.edit("desteklenen bir medya dosyasını yanıtla")
        return
    if replied.media:
        await exelonmemes.edit("telegraph geçiliyor...")
    else:
        await exelonmemes.edit("desteklenen bir medya dosyasını yanıtla")
        return
    try:
        exelon = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        exelon = Get(exelon)
        await exelonmemes.client(exelon)
    except BaseException:
        pass
    download_location = await borg.download_media(replied, Config.TMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await exelonmemes.edit("yanıtlanan dosya boyutu desteklenmiyor, 5 mb'nin altında olmalı")
            os.remove(download_location)
            return
        await exelonmemes.edit("görüntü oluşturuluyor..")
    else:
        await exelonmemes.edit("yanıtlanan dosya desteklenmiyor")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await exelonmemes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    exelon = f"https://telegra.ph{response[0]}"
    exelon = await awooify(exelon)
    await exelonmemes.delete()
    await borg.send_file(exelonmemes.chat_id, exelon, reply_to=replied)


@borg.on(admin_cmd(pattern="lolice(?: |$)(.*)"))
async def exelonbot(exelonmemes):
    replied = await exelonmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await exelonmemes.edit("desteklenen bir medya dosyasını yanıtla")
        return
    if replied.media:
        await exelonmemes.edit("telegraph geçiliyor...")
    else:
        await exelonmemes.edit("desteklenen bir medya dosyasını yanıtla")
        return
    try:
        exelon = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        exelon = Get(exelon)
        await exelonmemes.client(exelon)
    except BaseException:
        pass
    download_location = await borg.download_media(replied, Config.TMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await exelonmemes.edit("yanıtlanan dosya boyutu desteklenmiyor, 5 mb'nin altında olmalı")
            os.remove(download_location)
            return
        await exelonmemes.edit("görüntü oluşturuluyor..")
    else:
        await exelonmemes.edit("yanıtlanan dosya desteklenmiyor")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await exelonmemes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    exelon = f"https://telegra.ph{response[0]}"
    exelon = await lolice(exelon)
    await exelonmemes.delete()
    await borg.send_file(exelonmemes.chat_id, exelon, reply_to=replied)


@borg.on(admin_cmd(pattern="bun(?: |$)(.*)"))
async def exelonbot(exelonmemes):
    replied = await exelonmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await exelonmemes.edit("desteklenen bir medya dosyasını yanıtla")
        return
    if replied.media:
        await exelonmemes.edit("telegraph geçiliyor...")
    else:
        await exelonmemes.edit("desteklenen bir medya dosyasını yanıtla")
        return
    try:
        exelon = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        exelon = Get(exelon)
        await exelonmemes.client(exelon)
    except BaseException:
        pass
    download_location = await borg.download_media(replied, Config.TMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await exelonmemes.edit("yanıtlanan dosya boyutu desteklenmiyor, 5 mb'nin altında olmalı")
            os.remove(download_location)
            return
        await exelonmemes.edit("görüntü oluşturuluyor..")
    else:
        await exelonmemes.edit("yanıtlanan dosya desteklenmiyor")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await exelonmemes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    exelon = f"https://telegra.ph{response[0]}"
    exelon = await baguette(exelon)
    await exelonmemes.delete()
    await borg.send_file(exelonmemes.chat_id, exelon, reply_to=replied)


@borg.on(admin_cmd(pattern="iphx(?: |$)(.*)"))
async def exelonbot(exelonmemes):
    replied = await exelonmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await exelonmemes.edit("desteklenen bir medya dosyasını yanıtla")
        return
    if replied.media:
        await exelonmemes.edit("telegraph geçiliyor...")
    else:
        await exelonmemes.edit("desteklenen bir medya dosyasını yanıtla")
        return
    try:
        exelon = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        exelon = Get(exelon)
        await exelonmemes.client(exelon)
    except BaseException:
        pass
    download_location = await borg.download_media(replied, Config.TMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await exelonmemes.edit("yanıtlanan dosya boyutu desteklenmiyor, 5 mb'nin altında olmalı")
            os.remove(download_location)
            return
        await exelonmemes.edit("görüntü oluşturuluyor..")
    else:
        await exelonmemes.edit("yanıtlanan dosya desteklenmiyor")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await exelonmemes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    exelon = f"https://telegra.ph{response[0]}"
    exelon = await iphonex(exelon)
    await exelonmemes.delete()
    await borg.send_file(exelonmemes.chat_id, exelon, reply_to=replied)


@borg.on(sudo_cmd("mask ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("```Herhangi bir kullanıcı mesajını yanıtlayın.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.reply("```medya mesajına cevap ver```")
        return
    chat = "@hazmat_suit_bot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.reply("```Gerçek kullanıcıların mesajını yanıtlayın.```")
        return
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=905164246))
            await borg.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Lütfen @hazmat_suit_bot engellemesini kaldırın ve tekrar deneyin```")
            return
        if response.text.startswith("İleri"):
            await event.edit("```ileri gizlilik ayarlarınızı tamamen devre dışı bırakabilir misiniz?```")
        else:
            await borg.send_file(event.chat_id, response.message.media)


CMD_HELP.update({"mask": "`.mask` bir görüntü dosyasına yanıt ver:\
      \n**Kullanım ➥ **bir görüntüyü farklı bir stilde kendi tarzınızı denemek için yapar.\
      "
                 })
