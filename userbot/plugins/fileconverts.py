# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import os
import time
import asyncio
from io import BytesIO
from .. import CMD_HELP
from telethon import types
from datetime import datetime
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import SendMediaRequest
from ..utils import admin_cmd, sudo_cmd, progress, edit_or_reply


@borg.on(admin_cmd(pattern="stoi$"))
@borg.on(sudo_cmd(pattern="stoi$", allow_sudo=True))
async def _(exelon):
    if exelon.fwd_from:
        return
    reply_to_id = exelon.message.id
    if exelon.reply_to_msg_id:
        reply_to_id = exelon.reply_to_msg_id
    filename = "hi.jpg"
    event = await edit_or_reply(exelon, "Dönüştürülüyor.....")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await borg.download_media(reply_message, downloaded_file_name)
        if os.path.exists(downloaded_file_name):
            caat = await borg.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await event.edit("Dönüştürülemiyor")
    else:
        await event.edit("Kullanımı: `.to` bir Telegram normal çıkartmasını yanıtla")


@borg.on(admin_cmd(pattern="itos$"))
@borg.on(sudo_cmd(pattern="itos$", allow_sudo=True))
async def _(exelon):
    if exelon.fwd_from:
        return
    reply_to_id = exelon.message.id
    if exelon.reply_to_msg_id:
        reply_to_id = exelon.reply_to_msg_id
    filename = "hi.webp"
    event = await edit_or_reply(exelon, "Dönüştürülüyor......")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await borg.download_media(reply_message, downloaded_file_name)
        if os.path.exists(downloaded_file_name):
            caat = await borg.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await event.edit("Dönüştürülemiyor")
    else:
        await event.edit("Kullanımı: `.itos` bir Telegram normal çıkartmasını yanıtla")


@borg.on(admin_cmd(pattern="ttf ?(.*)"))
@borg.on(sudo_cmd(pattern="ttf ?(.*)", allow_sudo=True))
async def get(event):
    name = event.text[5:]
    if name is None:
        await edit_or_reply(event, "metin mesajını `.ttf` <dosya adı> olarak yanıtla>`")
        return
    m = await event.get_reply_message()
    if m.text:
        with open(name, "w") as f:
            f.write(m.message)
        await event.delete()
        await borg.send_file(event.chat_id, name, force_document=True)
        os.remove(name)
    else:
        await edit_or_reply(event, "metin mesajını `.ttf` <dosya adı> olarak yanıtla>`")


@borg.on(admin_cmd(pattern="ftoi$"))
@borg.on(sudo_cmd(pattern="ftoi$", allow_sudo=True))
async def on_file_to_photo(event):
    target = await event.get_reply_message()
    catt = await edit_or_reply(event, "Dönüştürülüyor.....")
    try:
        image = target.media.document
    except AttributeError:
        return
    if not image.mime_type.startswith('image/'):
        return  # This isn't an image
    if image.mime_type == 'image/webp':
        return  # Telegram doesn't let you directly send stickers as photos
    if image.size > 10 * 1024 * 1024:
        return  # We'd get PhotoSaveFileInvalidError otherwise
    file = await borg.download_media(target, file=BytesIO())
    file.seek(0)
    img = await borg.upload_file(file)
    img.name = 'image.png'
    try:
        await borg(SendMediaRequest(
            peer=await event.get_input_chat(),
            media=types.InputMediaUploadedPhoto(img),
            message=target.message,
            entities=target.entities,
            reply_to_msg_id=target.id
        ))
    except PhotoInvalidDimensionsError:
        return
    await catt.delete()


@borg.on(admin_cmd(pattern="nfc ?(.*)"))
@borg.on(sudo_cmd(pattern="nfc ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "```Herhangi bir medya dosyasını yanıtlayın.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "medya dosyasına yanıtla")
        return
    input_str = event.pattern_match.group(1)
    if input_str is None:
        await edit_or_reply(event, "try `.nfc voice` or`.nfc mp3`")
        return
    if input_str == "mp3":
        event = await edit_or_reply(event, "Dönüştürülüyor...")
    elif input_str == "voice":
        event = await edit_or_reply(event, "Dönüştürülüyor...")
    else:
        await edit_or_reply(event, "try `.nfc voice` or`.nfc mp3`")
        return
    try:
        start = datetime.now()
        c_time = time.time()
        downloaded_file_name = await borg.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download")
            )
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("{} Saniye içinde `{}` klasörüne indirildi.".format(downloaded_file_name, ms))
        new_required_file_name = ""
        new_required_file_caption = ""
        command_to_run = []
        force_document = False
        voice_note = False
        supports_streaming = False
        if input_str == "voice":
            new_required_file_caption = "voice_" + \
                str(round(time.time())) + ".opus"
            new_required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + \
                "/" + new_required_file_caption
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name
            ]
            voice_note = True
            supports_streaming = True
        elif input_str == "mp3":
            new_required_file_caption = "mp3_" + \
                str(round(time.time())) + ".mp3"
            new_required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + \
                "/" + new_required_file_caption
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name
            ]
            voice_note = False
            supports_streaming = True
        else:
            await event.edit("not supported")
            os.remove(downloaded_file_name)
            return
        logger.info(command_to_run)
        # TODO: re-write create_subprocess_exec 😉
        process = await asyncio.create_subprocess_exec(
            *command_to_run,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        os.remove(downloaded_file_name)
        if os.path.exists(new_required_file_name):
            end_two = datetime.now()
            await borg.send_file(
                entity=event.chat_id,
                file=new_required_file_name,
                allow_cache=False,
                silent=True,
                force_document=force_document,
                voice_note=voice_note,
                supports_streaming=supports_streaming,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "yüklemeye çalışıyor")
                )
            )
            (end_two - end).seconds
            os.remove(new_required_file_name)
            await event.delete()


CMD_HELP.update({"fileconverts": "**PLUGİN İSMİ:** `fileconverts`\
      \n\n**📌Komut ➥ **`.stoi` çıkartmaya cevap ver:\
      \n**Kullanım ➥ ** Çıkartmayı resme dönüştürür.\
      \n\n**📌Komut ➥ **`.itos` resme cevap ver:\
      \n**Kullanım ➥ ** Resmi çıkartmaya dönüştürür.\
      \n\n**📌Komut ➥ ** `.ftoi` görüntü dosyasına yanıt ver\
      \n**Kullanım ➥ ** Verilen görüntü dosyasını akışa uygun biçime dönüştürür.\
      \n\n**📌Komut ➥ **`.ttf` dosya adı metin mesajına yanıt :\
      \n**Kullanım ➥ ** Verilen kısa mesajı gerekli dosyaya dönüştürür (verilen dosya adı).\
      \n\n**📌Komut ➥ **`.nfc voice` veya `.nfc mp3` ses / mp3 ayıklamak için gerekli medyaya yanıt :\
      \n**Kullanım ➥ ** Gerekli medya dosyasını sese veya mp3 dosyasına dönüştürür."
                 })
