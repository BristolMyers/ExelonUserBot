# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""Speech to Text
Syntax: .stt <Dil Kodu> bir konuşma mesajına yanıt olarak"""
import requests
import os
from datetime import datetime
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="stt (.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    await event.edit("Analiz için yerelime indiriyorum 🙇")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        required_file_name = await borg.download_media(
            previous_message,
            Config.TMP_DOWNLOAD_DIRECTORY
        )
        lan = input_str
        if Config.IBM_WATSON_CRED_URL is None or Config.IBM_WATSON_CRED_PASSWORD is None:
            await event.edit("Bu modül için gerekli ENV değişkenlerini ayarlamanız gerekir. \nModül durduruluyor")
        else:
            await event.edit("IBM WatSon Speech To Text kullanarak analize başlama")
            headers = {
                "Content-Type": previous_message.media.document.mime_type,
            }
            data = open(required_file_name, "rb").read()
            response = requests.post(
                Config.IBM_WATSON_CRED_URL + "/v1/recognize",
                headers=headers,
                data=data,
                auth=("apikey", Config.IBM_WATSON_CRED_PASSWORD)
            )
            r = response.json()
            if "results" in r:
                # process the json to appropriate string format
                results = r["results"]
                transcript_response = ""
                transcript_confidence = ""
                for alternative in results:
                    alternatives = alternative["alternatives"][0]
                    transcript_response += " " + \
                        str(alternatives["transcript"]) + " + "
                    transcript_confidence += " " + \
                        str(alternatives["confidence"]) + " + "
                end = datetime.now()
                ms = (end - start).seconds
                if transcript_response != "":
                    string_to_show = "Dil: `{}`\nTRANSCRIPT: `{}`\nGeçen süre: {} saniye\nGüven: `{}`".format(
                        lan, transcript_response, ms, transcript_confidence)
                else:
                    string_to_show = "Dil: `{}`\nGeçen süre: {} saniye\n**Sonuç bulunamadı**".format(
                        lan, ms)
                await event.edit(string_to_show)
            else:
                await event.edit(r["error"])
            # now, remove the temporary file
            os.remove(required_file_name)
    else:
        await event.edit("İlgili transkripti almak için bir sesli mesajı yanıtlayın.")
