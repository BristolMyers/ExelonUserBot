# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
""" Google'da etiketleri ve resimleri tersine aramak için Userbot modülü"""

import io
import os
import urllib
import requests
from bs4 import BeautifulSoup
import re
from PIL import Image
from userbot import bot, CMD_HELP
from userbot.utils import admin_cmd, errors_handler

opener = urllib.request.build_opener()
useragent = 'Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36'
opener.addheaders = [('User-agent', useragent)]


@borg.on(admin_cmd(outgoing=True, pattern=r"reverse(?: |$)(\d*)"))
@errors_handler
async def okgoogle(img):
    """ .Reverse komutu için, Google resimleri ve çıkartmaları arayın. """
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")
    message = await img.get_reply_message()
    if message and message.media:
        photo = io.BytesIO()
        await bot.download_media(message, photo)
    else:
        await img.edit("`Fotoğrafı veya çıkartma zencisini yanıtlayın.`")
        return
    if photo:
        await img.edit("`İşleniyor...`")
        try:
            image = Image.open(photo)
        except OSError:
            await img.edit('`Büyük olasılıkla desteklenmiyor.`')
            return
        name = "okgoogle.png"
        image.save(name, "PNG")
        image.close()
        # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
        searchUrl = 'https://www.google.com/searchbyimage/upload'
        multipart = {
            'encoded_image': (name, open(name, 'rb')),
            'image_content': ''
        }
        response = requests.post(searchUrl,
                                 files=multipart,
                                 allow_redirects=False)
        fetchUrl = response.headers['Location']
        if response != 400:
            await img.edit("`Resim Google'a başarıyla yüklendi. Olabilir.`"
                           "\n`Kaynak şimdi ayrıştırılıyor. Olabilir.`")
        else:
            await img.edit("`Google bana defolup gitmemi söyledi.`")
            return
        os.remove(name)
        match = await ParseSauce(fetchUrl +
                                 "&preferences?hl=en&fg=1#languages")
        guess = match['best_guess']
        imgspage = match['similar_images']
        if guess and imgspage:
            await img.edit(f"[{guess}]({fetchUrl})\n\n`Bu görüntü aranıyor...`")
        else:
            await img.edit("`Bu pisliği bulamıyorum.`")
            return

        if img.pattern_match.group(1):
            lim = img.pattern_match.group(1)
        else:
            lim = 3
        images = await scam(match, lim)
        yeet = []
        for i in images:
            k = requests.get(i)
            yeet.append(k.content)
        try:
            await img.client.send_file(entity=await
                                       img.client.get_input_entity(img.chat_id
                                                                   ),
                                       file=yeet,
                                       reply_to=img)
        except TypeError:
            pass
        await img.edit(
            f"[{guess}]({fetchUrl})\n\n[Görsel olarak benzer resimler]({imgspage})")


async def ParseSauce(googleurl):
    """İstediğimiz bilgi için HTML kodunu ayrıştırın / kazıyın."""
    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, 'html.parser')
    results = {'similar_images': '', 'best_guess': ''}
    try:
        for similar_image in soup.findAll('input', {'class': 'gLFyf'}):
            url = 'https://www.google.com/search?tbm=isch&q=' + \
                urllib.parse.quote_plus(similar_image.get('value'))
            results['similar_images'] = url
    except BaseException:
        pass
    for best_guess in soup.findAll('div', attrs={'class': 'r5a77d'}):
        results['best_guess'] = best_guess.get_text()
    return results


async def scam(results, lim):
    single = opener.open(results['similar_images']).read()
    decoded = single.decode('utf-8')
    imglinks = []
    counter = 0
    pattern = r'^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$'
    oboi = re.findall(pattern, decoded, re.I | re.M)
    for imglink in oboi:
        counter += 2
        if counter <= int(lim):
            imglinks.append(imglink)
        else:
            break
    return imglinks

CMD_HELP.update({
    'reverse':
    '**📌Komut ➥ **.reverse\
     \n**Kullanım ➥ **Google Görsellerde tersten aramak için bir resme / çıkartmaya yanıt verin!'
})
