# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""IX.IO pastebin like site
Syntax: .paste
Syntax: .neko
Syntax: .paster
Syntax: .iffuci
"""

from userbot import CMD_HELP
from userbot.uniborgConfig import Config
from requests import exceptions, get
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.utils import admin_cmd
from telethon import events
import requests
from datetime import datetime
import os
import logging
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING)


def progress(current, total):
    logger.info(
        "{} / {} İndirildi\nTamamlandı {}".format(
            current,
            total,
            (current / total) * 100))


DOGBIN_URL = "https://del.dog/"

BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
BOTLOG = True


@borg.on(admin_cmd(pattern="paste ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.paste <eklenecek uzun metin>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.paste <eklenecek uzun meti>`"
    url = "https://del.dog/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    end = datetime.now()
    ms = (end - start).seconds
    if r["isUrl"]:
        nurl = f"https://del.dog/v/{r['key']}"
        await event.edit("Dogbin'e yapıştırıldı: [dog] ({}) {} saniye içinde. Orijinal URL'ye Git: [link] ({})".format(url, ms, nurl))
    else:
        await event.edit("Dogbin'e yapıştırıldı: [dog] ({}) {} saniye içinde".format(url, ms))


@borg.on(admin_cmd(outgoing=True, pattern="getpaste(?: |$)(.*)"))
async def get_dogbin_content(dog_url):
    """ .getpaste komutu için, bir dogbin URL'sinin içeriğini getirir. """
    textx = await dog_url.get_reply_message()
    message = dog_url.pattern_match.group(1)
    await dog_url.edit("`Dogbin içeriğini alınıyor...`")

    if textx:
        message = str(textx.message)

    format_normal = f'{DOGBIN_URL}'
    format_view = f'{DOGBIN_URL}v/'

    if message.startswith(format_view):
        message = message[len(format_view):]
    elif message.startswith(format_normal):
        message = message[len(format_normal):]
    elif message.startswith("del.dog/"):
        message = message[len("del.dog/"):]
    else:
        await dog_url.edit("`Bu bir dogbin url'si bile mi?`")
        return

    resp = get(f'{DOGBIN_URL}raw/{message}')

    try:
        resp.raise_for_status()
    except exceptions.HTTPError as HTTPErr:
        await dog_url.edit(
            "İstek, başarısız bir durum kodu döndürdü.\n\n" + str(HTTPErr))
        return
    except exceptions.Timeout as TimeoutErr:
        await dog_url.edit("İstek zaman aşımına uğradı." + str(TimeoutErr))
        return
    except exceptions.TooManyRedirects as RedirectsErr:
        await dog_url.edit(
            "İstek, yapılandırılan maksimum yeniden yönlendirme sayısını aştı." +
            str(RedirectsErr))
        return

    reply_text = "`Dogbin URL içeriği başarıyla alındı!`\n\n`İçerik:` " + resp.text

    await dog_url.edit(reply_text)
    if BOTLOG:
        await dog_url.client.send_message(
            BOTLOG_CHATID,
            "Dogbin içeriğini al sorgusu başarıyla yürütüldü",
        )


@borg.on(admin_cmd(pattern="neko ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.neko <eklenecek uzun meti>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                # message += m.decode("UTF-8") + "\r\n"
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.neko <eklenecek uzun meti>`"
    py_file = ""
    if downloaded_file_name.endswith(".py"):
        py_file += ".py"
        data = message
        key = requests.post(
            'https://nekobin.com/api/documents',
            json={
                "content": data}).json().get('result').get('key')
        url = f'https://nekobin.com/{key}{py_file}'
        reply_text = f'Pasted to Nekobin : [neko]({url})'
        await event.edit(reply_text)
    else:
        data = message
        key = requests.post(
            'https://nekobin.com/api/documents',
            json={
                "content": data}).json().get('result').get('key')
        url = f'https://nekobin.com/{key}'
        reply_text = f'Pasted to Nekobin : [neko]({url})'
        await event.edit(reply_text)


@borg.on(admin_cmd(pattern="iffuci ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.iffuci <eklenecek uzun meti>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.iffuci <eklenecek uzun meti>`"
    url = "https://www.iffuci.tk/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://iffuci.tk/{r['key']}"
    end = datetime.now()
    ms = (end - start).seconds
    if r["isUrl"]:
        nurl = f"https://iffuci.tk/v/{r['key']}"
        await event.edit("code is pasted to {} in {} seconds. GoTo Original URL: {}".format(url, ms, nurl))
    else:
        await event.edit("code is pasted to {} in {} seconds".format(url, ms))


@borg.on(admin_cmd(pattern="paster ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    datetime.now()
    reply_message = await event.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.paste <eklenecek uzun meti>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.paste <eklenecek uzun meti>`"
    url = "https://del.dog/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    chat = "@chotamreaderbot"
    if r["isUrl"]:
        nurl = f"https://del.dog/v/{r['key']}"
        await event.edit("{} Saniye içinde {} doğrulandı. GoTo Original URL: {}".format(url, ms, nurl))

    else:
        await event.edit("**Anlık görüntüleme yapılıyor...**")
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(
                        incoming=True,
                        from_users=272572121))
                await event.client.send_message(chat, url)
                response = await response
            except YouBlockedUserError:
                await event.reply("```Lütfen beni engellemeyi kaldır (@chotamreaderbot) u Nigga```")
                return
            await event.delete()
            await event.client.send_message(event.chat_id, response.message, reply_to=reply_message)

CMD_HELP.update({
    "pastebin":
    "**📌Komut ➥ **.paste <metin/yanıtla>\
\n**Kullanım ➥  ** Dogbin kullanarak bir yapıştırma veya kısaltılmış url oluşturun (https://del.dog/)\
\n\n**📌Komut ➥ **.getpaste\
\n**Kullanım ➥  ** Bir yapıştırma veya kısaltılmış url içeriğini dogbin'den alır (https://del.dog/)\
\n\n**📌Komut ➥ **.neko <metin>\
\n**Kullanım ➥  **Nekobin (https://nekobin.com) kullanarak bir yapıştırma veya kısaltılmış url oluşturun\
\n\n**📌Komut ➥ **.iffuci <metin/yanıtla>\
\n**Kullanım ➥  ** İffuci kullanarak bir yapıştırma veya kısaltılmış url oluşturun (https://www.iffuci.tk)\
\n\n**📌Komut ➥ **.paster <metin/yanıtla>\
\n**Kullanım ➥  **Anında bir görünüm oluşturun veya telgraf dosyasına yapıştırın\
  "
})
