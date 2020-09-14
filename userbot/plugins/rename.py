# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import asyncio
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import os
import subprocess
from telethon.tl.types import DocumentAttributeVideo
import time
from userbot import ALIVE_NAME
from userbot.utils import admin_cmd, sudo_cmd
from userbot.utils import humanbytes, progress
import math
from pySmartDL import SmartDL

thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "thumb_image.jpg"


def get_video_thumb(file, output=None, width=90):
    metadata = extractMetadata(createParser(file))
    p = subprocess.Popen([
        'ffmpeg', '-i', file,
        '-ss', str(int((0, metadata.get('duration').seconds)[metadata.has('duration')] / 2)),
        '-filter:v', 'scale={}:-1'.format(width),
        '-vframes', '1',
        output,
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if not p.returncode and os.path.lexists(file):
        return output


DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "exelon"


@borg.on(admin_cmd(pattern="rename (.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("İşlem sırasında yeniden adlandırma  🙄🙇‍♂️🙇‍♂️🙇‍♀️ Dosya boyutu büyükse biraz zaman alabilir")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        c_time = time.time()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await borg.download_media(
            reply_message,
            downloaded_file_name,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "indirmeye çalışıyor")
            )
        )
        end = datetime.now()
        ms = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            await event.edit(f"__**➥ {ms} saniye içinde indirildi.**__\n__**➥ İndirildi :- **__ `{downloaded_file_name}`\n__**➥ İndiren:-**__ {DEFAULTUSER}")
        else:
            await event.edit("Hata oluştu\n {}".format(input_str))
    else:
        await event.edit("Syntax // bir Telegram medyasına yanıt olarak `.rename file.name`")


@borg.on(admin_cmd(pattern="rnup (.*)"))
async def _(event):
    if event.fwd_from:
        return
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    await event.edit("Yeniden Adlandırma ve Yükleme işlemi devam ediyor 🙄🙇‍♂️🙇‍♂️🙇‍♀️ Dosya boyutu büyükse biraz zaman alabilir")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        c_time = time.time()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await borg.download_media(
            reply_message,
            downloaded_file_name,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "indirmeye çalışıyor")
            )
        )
        end = datetime.now()
        ms_one = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            c_time = time.time()
            caat = await borg.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                supports_streaming=False,
                allow_cache=False,
                reply_to=event.message.id,
                thumb=thumb,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "indirmeye çalışıyor")
                )

            )
            end_two = datetime.now()
            os.remove(downloaded_file_name)
            ms_two = (end_two - end).seconds
            await event.delete()
            await caat.edit(f"__**➥ {ms_one} saniye içinde indirildi.**__\n__**➥ {ms_two} saniye içinde yüklendi.**__\n__**➥İndiren :-**__ {DEFAULTUSER}")
        else:
            await event.edit("Dosya bulunamadı {}".format(input_str))
    else:
        await event.edit("Syntax // Telegram medyasına yanıt olarak .rnupload file.name")


@borg.on(sudo_cmd(pattern="rnup (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    await event.edit("Yeniden Adlandırma ve Yükleme işlemi devam ediyor 🙄🙇‍♂️🙇‍♂️🙇‍♀️ Dosya boyutu büyükse biraz zaman alabilir")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        c_time = time.time()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await borg.download_media(
            reply_message,
            downloaded_file_name,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "indirmeye çalışıyor")
            )
        )
        end = datetime.now()
        ms_one = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            c_time = time.time()
            caat = await borg.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                supports_streaming=False,
                allow_cache=False,
                reply_to=event.message.id,
                thumb=thumb,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "indirmeye çalışıyor")
                )

            )
            end_two = datetime.now()
            os.remove(downloaded_file_name)
            ms_two = (end_two - end).seconds
            await event.delete()
            await caat.reply(f"__**➥ {ms_one} saniye içinde indirildi.**__\n__**➥ {ms_two} saniye içinde yüklendi.**__\n__**➥ İndiren :-**__ {DEFAULTUSER}")
        else:
            await event.reply("Dosya bulunamadı {}".format(input_str))
    else:
        await event.reply("Syntax // .rnupload file.name as reply to a Telegram media")


@borg.on(admin_cmd(pattern="rnstreamup (.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("İşlem devam ederken Yayınlanabilir olarak yeniden adlandırın ve yükleyin 🙄🙇‍♂️🙇‍♂️🙇‍♀️ Dosya boyutu büyükse biraz zaman alabilir")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        c_time = time.time()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await borg.download_media(
            reply_message,
            downloaded_file_name,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "indirmeye çalışıyor")
            )
        )
        end_one = datetime.now()
        ms_one = (end_one - start).seconds
        if os.path.exists(downloaded_file_name):
            thumb = None
            if not downloaded_file_name.endswith(
                    (".mkv", ".mp4", ".mp3", ".flac")):
                await event.edit("Afedersiniz. Ancak, {} akışına uygun bir dosya olduğunu sanmıyorum. Lütfen tekrar deneyin.\n**Desteklenen Formatlar**: MKV, MP4, MP3, FLAC".format(downloaded_file_name))
                return False
            if os.path.exists(thumb_image_path):
                thumb = thumb_image_path
            else:
                thumb = get_video_thumb(downloaded_file_name, thumb_image_path)
            start = datetime.now()
            metadata = extractMetadata(createParser(downloaded_file_name))
            duration = 0
            width = 0
            height = 0
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if os.path.exists(thumb_image_path):
                metadata = extractMetadata(createParser(thumb_image_path))
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")
            # Telegram only works with MP4 files
            # this is good, since with MKV files sent as streamable Telegram responds,
            # Bad Request: VIDEO_CONTENT_TYPE_INVALID
           # c_time = time.time()
            try:
                caat = await borg.send_file(
                    event.chat_id,
                    downloaded_file_name,
                    thumb=thumb,
                    caption="Exelon tarafından yeniden yüklendi",
                    force_document=False,
                    allow_cache=False,
                    reply_to=event.message.id,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True
                        )
                    ]
                )
            except Exception as e:
                await event.edit(str(e))
            else:
                end = datetime.now()
                os.remove(downloaded_file_name)
                ms_two = (end - end_one).seconds
                await event.delete()
                await caat.edit(f"__**➥ {ms_one} saniye içinde indirildi.**__\n__**➥ {ms_two} saniye içinde yüklendi.**__\n__**➥ İndiren :-**__ {DEFAULTUSER}")
        else:
            await event.edit("Dosya bulunamadı {}".format(input_str))
    else:
        await event.edit("Syntax // Telegram MEDYASINA yanıt olarak .rnstreamupload file.name")


@borg.on(admin_cmd(pattern="rndlup (.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    url = input_str
    file_name = os.path.basename(url)
    to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
    if "|" in input_str:
        url, file_name = input_str.split("|")
    url = url.strip()
    file_name = file_name.strip()
    downloaded_file_name = os.path.join(to_download_directory, file_name)
    downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False)
    display_message = ""
    c_time = time.time()
    while not downloader.isFinished():
        total_length = downloader.filesize if downloader.filesize else None
        downloaded = downloader.get_dl_size()
        now = time.time()
        diff = now - c_time
        percentage = downloader.get_progress() * 100
        downloader.get_speed()
        round(diff) * 1000
        progress_str = "[{0}{1}]\nileniyor: {2}%".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))
        estimated_total_time = downloader.get_eta(human=True)
        try:
            current_message = f"indirmeye çalışıyor\n"
            current_message += f"URL: {url}\n"
            current_message += f"Dosya Aı: {file_name}\n"
            current_message += f"{progress_str}\n"
            current_message += f"{humanbytes(downloaded)} of {humanbytes(total_length)}\n"
            current_message += f"ETA: {estimated_total_time}"
            if round(diff % 10.00) == 0 and current_message != display_message:
                await event.edit(current_message)
                display_message = current_message
        except Exception as e:
            logger.info(str(e))
    end = datetime.now()
    ms_dl = (end - start).seconds
    if downloader.isSuccessful():
        await event.edit("{} Saniye içinde `{}` konumuna indirildi".format(downloaded_file_name, ms_dl))
        if os.path.exists(downloaded_file_name):
            c_time = time.time()
            caat = await borg.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=event.message.id,
                thumb=thumb,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "İndirmeye çalışıyor")
                )
            )
            end_two = datetime.now()
            os.remove(downloaded_file_name)
            ms_two = (end_two - end).seconds
            await event.delete()
            await caat.edit(f"__**➥ {ms_dl} saniye içinde indirildi.**__\n__**➥ {ms_two} saniye içinde yüklendi.**__\n__**➥ İndiren :-**__ {DEFAULTUSER}")
        else:
            await event.edit("Dosya bulunamadı {}".format(input_str))
    else:
        await event.edit("Incorrect URL\n {}".format(input_str))
