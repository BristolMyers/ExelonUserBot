# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
""" Çeşitli sıyırıcılar içeren Exelon modülü. """

import os
import random
from time import sleep
from selenium import webdriver
from urllib.parse import quote_plus
from selenium.webdriver.chrome.options import Options
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError
from googletrans import LANGUAGES, Translator
from gtts.lang import tts_langs
from emoji import get_emoji_regexp
from asyncio import sleep
from userbot import CHROME_DRIVER, GOOGLE_CHROME_BIN
from userbot.utils import admin_cmd
from userbot.uniborgConfig import Config

LANG = "tr"
CARBONLANG = "auto"
TTS_LANG = "tr"
TRT_LANG = "tr"
if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID


@borg.on(admin_cmd(outgoing=True, pattern="krb"))
async def carbon_api(e):
    await e.edit("İşleniyor..")
    CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
    global CARBONLANG
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[5:]:
        pcodee = str(pcode[5:])
        if "|" in pcodee:
            pcode, skeme = pcodee.split("|")
        else:
            pcode = pcodee
            skeme = None
    elif textx:
        pcode = str(textx.message)
        skeme = None  # Importing message to module
    pcode = deEmojify(pcode)
    code = quote_plus(pcode)  # Converting to urlencoded
    await e.edit("Carbon yapılıyor...\n25%")
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {'download.default_directory': './'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER,
        options=chrome_options)
    driver.get(url)
    await e.edit("Sabırlı ol...\n50%")
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_path}}
    driver.execute("send_command", params)
    driver.find_element_by_xpath(
        '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[1]/div/span[2]').click()
    if skeme is not None:
        k_skeme = driver.find_element_by_xpath(
            '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[1]/div/span[2]/input')
        k_skeme.send_keys(skeme)
        k_skeme.send_keys(Keys.DOWN)
        k_skeme.send_keys(Keys.ENTER)
    else:
        color_scheme = str(random.randint(1, 29))
        driver.find_element_by_id(("downshift-0-item-" + color_scheme)).click()
    driver.find_element_by_id("export-menu").click()
    driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
    driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
    await e.edit("İşleniyor..\n75%")
    # Waiting for downloading
    await sleep(2.5)
    color_name = driver.find_element_by_xpath(
        '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[1]/div/span[2]/input').get_attribute('value')
    await e.edit("Sonunda bitti...\n100%")
    file = './carbon.png'
    await e.edit("Uploading..")
    await e.client.send_file(
        e.chat_id,
        file,
        caption="`İşte karbonunuz!` \n**Renk şeması: **`{}`".format(color_name),
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )
    os.remove('./carbon.png')
    driver.quit()
    # Removing carbon.png after uploading
    await e.delete()  # Deleting msg


@borg.on(admin_cmd(outgoing=True, pattern=r"wiki (.*)"))
async def wiki(wiki_q):
    """ .wiki komutu için Wikipedia'dan içerik alın. """
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Netleştirilmemiş sayfa bulundu.\n\n{error}")
        return
    except PageError as pageerror:
        await wiki_q.edit(f"Sayfa bulunamadı.\n\n{pageerror}")
        return
    result = summary(match)
    if len(result) >= 4096:
        file = open("output.txt", "w+")
        file.write(result)
        file.close()
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "output.txt",
            reply_to=wiki_q.id,
            caption="`Çıktı çok büyük, dosya olarak gönderiliyor`",
        )
        if os.path.exists("output.txt"):
            os.remove("output.txt")
        return
    await wiki_q.edit("**Arama:**\n`" + match + "`\n\n**Sonucu:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"Wiki sorgusu `{match}` başarıyla yürütüldü")


@borg.on(admin_cmd(outgoing=True, pattern=r"trt(?: |$)([\s\S]*)"))
async def translateme(trans):
    """ .trt komutu için, verilen metni Google Translate kullanarak çevirin. """
    translator = Translator()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await trans.edit("`Çevirmek için bir mesaja bir metin veya cevap verin!`")
        return

    try:
        reply_text = translator.translate(deEmojify(message), dest=TRT_LANG)
    except ValueError:
        await trans.edit("Geçersiz hedef dil.")
        return

    source_lan = LANGUAGES[f'{reply_text.src.lower()}']
    transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
    reply_text = f"Nereden **{source_lan.title()}**\nİçin **{transl_lan.title()}:**\n\n{reply_text.text}"

    await trans.edit(reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"Bazı {source_lan.title ()} içeriği şimdi {transl_lan.title ()} diline çevrildi.",
        )


@borg.on(admin_cmd(pattern="lang (trt|tts) (.*)", outgoing=True))
async def lang(value):
    """ .lang komutu için, userbot kazıyıcılarının varsayılan dilini değiştirin. """
    util = value.pattern_match.group(1).lower()
    if util == "trt":
        scraper = "Çevirmen"
        global TRT_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in LANGUAGES:
            TRT_LANG = arg
            LANG = LANGUAGES[arg]
        else:
            await value.edit(
                f"`Geçersiz Dil kodu !!`\n`TRT için mevcut dil kodları`:\n\n`{LANGUAGES}`"
            )
            return
    elif util == "tts":
        scraper = "Konuşma metni"
        global TTS_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            await value.edit(
                f"`Geçersiz Dil kodu !!`\n`TTS için mevcut dil kodları`:\n\n`{tts_langs()}`"
            )
            return
    await value.edit(f"`{scraper} için dil {LANG.title ()} olarak değiştirildi.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID,
            f"`{scraper} için dil {LANG.title ()} olarak değiştirildi.`")


def deEmojify(inputString):
    """ Dizeden emojileri ve diğer güvenli olmayan karakterleri kaldırın """
    return get_emoji_regexp().sub(u'', inputString)
