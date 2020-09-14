# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
import io
import traceback
from datetime import datetime
from selenium import webdriver
from userbot.utils import admin_cmd
from userbot import CMD_HELP
import requests
from validators.url import url


@borg.on(admin_cmd(pattern="ss (.*)"))
async def _(event):
    if event.fwd_from:
        return
    if Config.CHROME_BIN is None:
        await event.edit("Google Chrome'u yüklemeniz gerekiyor. Modül Durduruluyor.")
        return
    await event.edit("İşleniyor...")
    start = datetime.now()
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--headless")
        # https://stackoverflow.com/a/53073789/4723940
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.binary_location = Config.CHROME_BIN
        await event.edit("Starting Google Chrome BIN")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        input_str = event.pattern_match.group(1)
        exelonurl = url(input_str)
        if not exelonurl:
            await event.edit("url, `https: // www.google.com` biçiminde olmalıdır")
            return
        driver.get(input_str)
        await event.edit("Sayfa Boyutlarını Hesaplama")
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);")
        driver.set_window_size(width + 100, height + 100)
        # Add some pixels on top of the calculated dimensions
        # for good measure to make the scroll bars disappear
        im_png = driver.get_screenshot_as_png()
        # saves screenshot of entire page
        await event.edit("Chrome Bin'i Durdu")
        driver.close()
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        end = datetime.now()
        ms = (end - start).seconds
        hmm = f"**url : **{input_str} \n**Zaman:** `{ms} saniye`"
        await event.delete()
        with io.BytesIO(im_png) as out_file:
            out_file.name = input_str + ".PNG"
            await borg.send_file(
                event.chat_id,
                out_file,
                caption=hmm,
                force_document=True,
                reply_to=message_id,
                allow_cache=False,
                silent=True
            )
    except Exception:
        await event.edit(traceback.format_exc())


@borg.on(admin_cmd(pattern="scapture (.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if Config.SCREEN_SHOT_LAYER_ACCESS_KEY is None:
        await event.edit("https://screenshotlayer.com/product adresinden bir API anahtarı almanız gerekiyor \nModule stopping!")
        return
    await event.edit("İşleniyor...")
    sample_url = "https://api.screenshotlayer.com/api/capture?access_key={}&url={}&fullpage={}&viewport={}&format={}&force={}"
    input_str = event.pattern_match.group(1)
    exelonurl = url(input_str)
    if not exelonurl:
        await event.edit("url, `https://www.google.com` biçiminde olmalıdır")
        return
    response_api = requests.get(sample_url.format(
        Config.SCREEN_SHOT_LAYER_ACCESS_KEY,
        input_str,
        "1",
        "2560x1440",
        "PNG",
        "1"
    ))
    # https://stackoverflow.com/a/23718458/4723940
    contentType = response_api.headers['content-type']
    end = datetime.now()
    ms = (end - start).seconds
    hmm = f"**url : **{input_str} \n**Zaman:** `{ms} saniye`"
    if "image" in contentType:
        with io.BytesIO(response_api.content) as screenshot_image:
            screenshot_image.name = "screencapture.png"
            try:
                await borg.send_file(
                    event.chat_id,
                    screenshot_image,
                    caption=hmm,
                    force_document=True,
                    reply_to=event.message.reply_to_msg_id
                )
                await event.delete()
            except Exception as e:
                await event.edit(str(e))
    else:
        await event.edit(response_api.text)

CMD_HELP.update({
    "screenshot":
    "**📌Komut ➥ **.ss <url>\
    \n**Kullanım ➥ ** Bir web sitesinin ekran görüntüsünü alır ve ekran görüntüsünü gönderir.\
    \nGeçerli bir URL örneği➥  `https: // www.google.com`\
    \n\n**📌Komut ➥ **.scapture <url>\
    \n**Kullanım ➥ ** Bir web sitesinin ekran görüntüsünü alır ve bunun için yapılandırma değişkenini ayarlamak için ekran görüntüsünü gönderir.\
    \nGeçerli bir URL örneği➥  `https: // www.google.com`"
})
