# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import asyncio
import os
import time
import time as t
from datetime import datetime
from userbot.utils import admin_cmd
import zipfile


extracted = Config.TMP_DOWNLOAD_DIRECTORY + "extracted/"
thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


@borg.on(admin_cmd("zip"))
async def _(event):
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.edit("`Bir dosyayı sıkıştırmak için yanıtlayın.`")
        return
    mone = await event.edit("Işleniyor...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
            directory_name = downloaded_file_name
            await event.edit(downloaded_file_name)
        except Exception as e:  # pylint: devre dışı bırak = C0103, W0703
            await mone.edit(str(e))
    zipfile.ZipFile(
        directory_name + '.zip',
        'w',
        zipfile.ZIP_DEFLATED).write(directory_name)
    await borg.send_file(
        event.chat_id,
        directory_name + ".zip",
        caption="**Sıkıştırılmış!**",
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id,
    )
    await asyncio.sleep(7)
    await event.delete()


def zipdir(path, ziph):
    # ziph, zip dosyası tanıtıcısıdır
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))


@command(pattern="^.unzip")
async def _(event):
    if event.fwd_from:
        return
    mone = await event.edit("İşleme...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            t.time()
            downloaded_file_name = await bot.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
        except Exception as e:  # pylint: devre dışı bırak = C0103, W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit("`Zip dosyasını {} saniye içinde {} konumuna depoladı.`".format(downloaded_file_name, ms))

        with zipfile.ZipFile(downloaded_file_name, 'r') as zip_ref:
            zip_ref.extractall(extracted)
        filename = sorted(get_lst_of_files(extracted, []))
        # dosyaadı = dosya adı + "/"
        await event.edit("Unzipping now")
        #r = kök, d = dizinler, f = dosyalar
        for single_file in filename:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                force_document = True
                supports_streaming = False
                document_attributes = []
                try:
                    await bot.send_file(
                        event.chat_id,
                        single_file,
                        caption=f"**Unzipped** `{caption_rts}`",
                        force_document=force_document,
                        supports_streaming=supports_streaming,
                        allow_cache=False,
                        reply_to=event.message.id,
                        attributes=document_attributes,
                        # progress_callback = lambda d, t: asyncio.get_event_loop (). create_task (
                        #     ilerleme (d, t, olay, c_time, "yüklemeye çalışılıyor")
                        # )
                    )
                except Exception as e:
                    await bot.send_message(
                        event.chat_id,
                        "{} neden oldu `{}`".format(caption_rts, str(e)),
                        reply_to=event.message.id
                    )
                    # bazı medyanın bazı sorunları vardı
                    continue
                os.remove(single_file)
        os.remove(downloaded_file_name)


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst
