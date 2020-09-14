# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
""" Powered by @Google
Available Commands:
.gs <query>
.grs """

import os
from re import findall
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from userbot.utils import admin_cmd
from re import findall
from search_engine_parser import GoogleSearch
from userbot.uniborgConfig import Config


def progress(current, total):
    logger.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current,
            total,
            (current / total) * 100))


BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
BOTLOG = True


@borg.on(admin_cmd(outgoing=True, pattern=r"gs (.*)"))
async def gsearch(q_event):
    """ .google komutu için bir Google araması yapın. """
    match = q_event.pattern_match.group(1)
    page = findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"👉[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await q_event.edit("**Arama Sorgusu:**\n`" + match + "`\n\n**Sonuçlar:**\n" +
                       msg,
                       link_preview=False)
    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            "Google Arama sorgusu `" + match + "` başarıyla yürütüldü",
        )


@borg.on(admin_cmd(pattern="grs"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    BASE_URL = "http://www.google.com"
    OUTPUT_STR = "Google Tersine Arama yapmak için bir görseli yanıtlayın"
    if event.reply_to_msg_id:
        await event.edit("Ön İşlem Ortamı")
        previous_message = await event.get_reply_message()
        previous_message_text = previous_message.message
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY
            )
            SEARCH_URL = "{}/searchbyimage/upload".format(BASE_URL)
            multipart = {
                "encoded_image": (
                    downloaded_file_name,
                    open(
                        downloaded_file_name,
                        "rb")),
                "image_content": ""}
            # https://stackoverflow.com/a/28792943/4723940
            google_rs_response = requests.post(
                SEARCH_URL, files=multipart, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
            os.remove(downloaded_file_name)
        else:
            previous_message_text = previous_message.message
            SEARCH_URL = "{}/searchbyimage?image_url={}"
            request_url = SEARCH_URL.format(BASE_URL, previous_message_text)
            google_rs_response = requests.get(
                request_url, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
        await event.edit("Google Sonucu Bulundu. Üzerine biraz çorba döküyorum!")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # document.getElementsByClassName("r5a77d"): PRS
        prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
        prs_anchor_element = prs_div.find("a")
        prs_url = BASE_URL + prs_anchor_element.get("href")
        prs_text = prs_anchor_element.text
        # document.getElementById("jHnbRc")
        img_size_div = soup.find(id="jHnbRc")
        img_size = img_size_div.find_all("div")
        end = datetime.now()
        ms = (end - start).seconds
        OUTPUT_STR = """{img_size}
**Muhtemel İlgili Arama**: <a href="{prs_url}">{prs_text}</a>
Daha Fazla Bilgi: Bunu aç <a href="{the_location}">Link</a> in {ms} saniye""".format(**locals())
    await event.edit(OUTPUT_STR, parse_mode="HTML", link_preview=False)
