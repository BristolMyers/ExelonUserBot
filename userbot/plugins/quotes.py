# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
import random
import requests
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="quote ?(.*)"))
async def quote_search(event):
    if event.fwd_from:
        return
    await event.edit("İşleniyor...")
    search_string = event.pattern_match.group(1)
    input_url = "https://bots.shrimadhavuk.me/Telegram/GoodReadsQuotesBot/?q={}".format(
        search_string)
    headers = {"USER-AGENT": "UniBorg"}
    try:
        response = requests.get(input_url, headers=headers).json()
    except BaseException:
        response = None
    if response is not None:
        result = random.choice(response).get(
            "input_message_content").get("message_text")
    else:
        result = None
    if result:
        await event.edit(result.replace("<code>", "`").replace("</code>", "`"))
    else:
        await event.edit("Sıfır sonuç bulundu")
