# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
import os
import requests
from userbot import bot, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.utils import admin_cmd

OCR_SPACE_API_KEY = Config.OCR_SPACE_API_KEY


async def ocr_space_file(filename,
                         overlay=False,
                         api_key=OCR_SPACE_API_KEY,
                         language='tr'):
    """ Yerel dosya ile OCR.space API isteği.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    with open(filename, 'rb') as f:
        r = requests.post(
            'https://api.ocr.space/parse/image',
            files={filename: f},
            data=payload,
        )
    return r.json()


@borg.on(admin_cmd(pattern="ocr(?: |$)(.*)", outgoing=True))
async def ocr(event):
    await event.edit("`Okunuyor...`")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await bot.download_media(
        await event.get_reply_message(), TEMP_DOWNLOAD_DIRECTORY)
    test_file = await ocr_space_file(filename=downloaded_file_name,
                                     language=lang_code)
    try:
        ParsedText = test_file["Ayrıştırılmış Sonuçlar"][0]["ParsedText"]
    except BaseException:
        await event.edit("`Okuyamadım.`\n`Sanırım yeni gözlüğe ihtiyacım var.`")
    else:
        await event.edit(f"`İşte ondan okuyabileceklerim:`\n\n{ParsedText}"
                         )
    os.remove(downloaded_file_name)


CMD_HELP.update({
    'ocr':
    ".ocr <language>\nUsage: Metni çıkarmak için bir görüntü veya çıkartmayı yanıtlayın.\n\nDil kodlarını [buradan] alın (https://ocr.space/ocrapi)"
})
