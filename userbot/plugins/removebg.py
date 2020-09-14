# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
#
""
from datetime import datetime
import io
import os
import requests
from userbot.utils import admin_cmd
from userbot import CMD_HELP


@borg.on(admin_cmd(pattern="rmbg ?(.*)"))
async def _(event):
    HELP_STR = "Bir medyaya yanıt olarak `.rmbg `veya bu komuta argüman olarak bir bağlantı verin"
    if event.fwd_from:
        return
    if Config.REM_BG_API_KEY is None:
        await event.edit("Bu eklentiyi kullanmak için remove.bg'deki API belirtecine ihtiyacınız var.")
        return False
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        # check if media message
        await event.edit("Ooh Analysing dis pic...")
        try:
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await event.edit(str(e))
            return
        else:
            await event.edit("ReMove.BG'ye gönderme")
            output_file_name = ReTrieveFile(downloaded_file_name)
            os.remove(downloaded_file_name)
    elif input_str:
        await event.edit("ReMove.BG'ye gönderme")
        output_file_name = ReTrieveURL(input_str)
    else:
        await event.edit(HELP_STR)
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "BG_less.png"
            await borg.send_file(
                event.chat_id,
                remove_bg_image,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id
            )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Bu sinir bozucu Arka Planı {} saniye içinde kaldırın".format(ms))
    else:
        await event.edit("ReMove.BG API Hata döndürdü. Lütfen @ExelonSupport'a bildirin\n`{}".format(output_file_name.content.decode("UTF-8")))


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True
    )
    return r


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    data = {
        "image_url": input_url
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True
    )
    return r


CMD_HELP.update({
    "removebg":
    "**📌Komut ➥ **.rmbg <Resme Bağlantı> veya herhangi bir resmi yanıtlayın (Uyarı: çıkartmalarda çalışmaz.)\
\n**Kullanım ➥ ** Remove.bg API'sini kullanarak görüntülerin arka planını kaldırır"
})
