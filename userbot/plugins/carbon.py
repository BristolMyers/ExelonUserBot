# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

"""Exelon için Karbon Kazıyıcı Eklentisi. // yaratıcı bir şekilde metin.
kullanım: .kar1 // herhangi bir metin mesajına yanıt olarak
kullanım: .kar2 // herhangi bir metin mesajına cevap olarak
kullanım: .kar3 // herhangi bir metin mesajına yanıt olarak
kullanım: .kar4 // herhangi bir metin mesajına cevap olarak
kullanım: .rgbk2 // herhangi bir kısa mesaja yanıt olarak
kullanım: .kargb // herhangi bir kısa mesaja yanıt olarak
kullanım: .karpp // profil resminiz ayarlanacak
Vars  için @BristolMyers'e teşekkürler"""

import os
import random
import asyncio
from . import deEmojify
from selenium import webdriver
from urllib.parse import quote_plus
from selenium.webdriver.chrome.options import Options
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from .. import CMD_HELP, CHROME_DRIVER, GOOGLE_CHROME_BIN, ALIVE_NAME

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "exelon"

CARBONLANG = "auto"
LANG = "tr"


@borg.on(admin_cmd(outgoing=True, pattern="carbon(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="carbon(?: |$)(.*)", allow_sudo=True))
async def carbon_api(e):
    """ Carbon.now.sh için bir Wrapper """
    await e.edit("`İşleniyor.`")
    CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)  # Mesaj modüle aktarılıyor
    pcode = deEmojify(pcode)
    code = quote_plus(pcode)  # Urlencoded'e dönüştürme
    exelon = await edit_or_reply(e, "`Carbon Yapılıyor...\n25%`")
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
    await exelon.edit("`Sabırlı ol...\n50%`")
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_path}}
    driver.execute("send_command", params)
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
   # driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
   # driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
    await exelon.edit("`İşleniyor..\n75%`")
    # Waiting for downloading
    await asyncio.sleep(2)
    await exelon.edit("`Done Dana Done...\n100%`")
    file = './carbon.png'
    await exelon.edit("`Yükleniyor..`")
    await e.client.send_file(
        e.chat_id,
        file,
        caption="İşte karbonun, \n Exelon tarafından yapıldı",
        force_document=True,
        reply_to=e.message.reply_to_msg_id
    )
    os.remove('./carbon.png')
    driver.quit()
    # Yüklemeden sonra carbon.png kaldırılıyor
    await exelon.delete()  # Deleting msg


@borg.on(admin_cmd(pattern=f"kar1(?: |$)(.*)", outgoing=True))
async def carbon_api(e):
    """ Carbon.now.sh için bir Wrapper """
    await e.edit("🔲🔲🔲🔲🔲")
    CARBON = 'https://carbon.now.sh/?bg=rgba(249%2C237%2C212%2C0)&t=synthwave-84&wt=none&l=application%2Fjson&ds=true&dsyoff=20px&dsblur=0px&wc=true&wa=true&pv=56px&ph=0px&ln=false&fl=1&fm=IBM%20Plex%20Mono&fs=14.5px&lh=153%25&si=false&es=4x&wm=false&code={code}'
    CARBONLANG = "tr"
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[6:]:
        pcode = str(pcode[6:])
    elif textx:
        pcode = str(textx.message)  # Importing message to module
    code = quote_plus(pcode)  # Converting to urlencoded
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = Config.CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')
    prefs = {'download.default_directory': './'}
    chrome_options.add_experimental_option('prefs', prefs)
    await e.edit("🔳🔳🔲🔲🔲")

    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER,
        options=chrome_options)
    driver.get(url)
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_path}}
    driver.execute("send_command", params)

    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    await asyncio.sleep(2)
    await e.edit("🔳🔳🔳🔲🔲")
    await asyncio.sleep(2)
    await e.edit("🔳🔳🔳🔳🔳")
    file = './carbon.png'
    await e.edit("☣️Karbon 1 Tamamlandı, Yükleniyor Karbon☣️")
    await e.client.send_file(
        e.chat_id,
        file,
        caption=f"İşte Karbon1'iniz ",
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )
    os.remove('./carbon.png')
    # Removing carbon.png after uploading
    await e.delete()  # Deleting msg


@borg.on(admin_cmd(pattern=f"kar2(?: |$)(.*)", outgoing=True))
async def carbon_api(e):
    """ A Wrapper for carbon.now.sh """
    await e.edit("📛📛📛📛📛")
    CARBON = 'https://carbon.now.sh/?bg=rgba(239%2C40%2C44%2C1)&t=one-light&wt=none&l=application%2Ftypescript&ds=true&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Hack&fs=14px&lh=143%25&si=false&es=2x&wm=false&code={code}'
    CARBONLANG = "tr"
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[6:]:
        pcode = str(pcode[6:])
    elif textx:
        pcode = str(textx.message)  # Importing message to module
    code = quote_plus(pcode)  # Converting to urlencoded
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = Config.CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')
    prefs = {'download.default_directory': './'}
    chrome_options.add_experimental_option('prefs', prefs)
    await e.edit("🔘🔘📛📛📛")
    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER,
        options=chrome_options)
    driver.get(url)
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_path}}
    driver.execute("send_command", params)
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    await asyncio.sleep(2)
    await e.edit("🔘🔘🔘📛📛")
    await asyncio.sleep(2)  # Waiting for downloading
    await e.edit("🔘🔘🔘🔘🔘")
    file = './carbon.png'
    await e.edit("☣️Karbon 2 Tamamlandı, Yükleniyor Karbon☣️")
    await e.client.send_file(
        e.chat_id,
        file,
        caption=f"İşte Karbon2'niz",
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )

    os.remove('./carbon.png')
    # Removing carbon.png after uploading
    await e.delete()  # Deleting msg


@borg.on(admin_cmd(pattern=f"kar3(?: |$)(.*)", outgoing=True))
async def carbon_api(e):
    """ A Wrapper for carbon.now.sh """
    await e.edit("🎛🎛🎛🎛🎛")
    CARBON = 'https://carbon.now.sh/?bg=rgba(74%2C144%2C226%2C1)&t=material&wt=none&l=auto&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Fira%20Code&fs=14px&lh=152%25&si=false&es=2x&wm=false&code={code}'
    CARBONLANG = "tr"
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[6:]:
        pcode = str(pcode[6:])
    elif textx:
        pcode = str(textx.message)  # Importing message to module
    code = quote_plus(pcode)  # Converting to urlencoded
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = Config.CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')
    prefs = {'download.default_directory': './'}
    chrome_options.add_experimental_option('prefs', prefs)
    await e.edit("🔵🔵🎛🎛🎛")

    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER,
        options=chrome_options)
    driver.get(url)
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_path}}
    driver.execute("send_command", params)

    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    await asyncio.sleep(2)
    await e.edit("🔵🔵🔵🎛🎛")
   # driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
    await asyncio.sleep(2)  # Waiting for downloading

    await e.edit("🔵🔵🔵🔵🔵")
    file = './carbon.png'
    await e.edit("☣️Karbon  Tamamlandı, Yükleniyor Karbon☣️")
    await e.client.send_file(
        e.chat_id,
        file,
        caption=f"İşte Karbon3'ünüz",
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )

    os.remove('./carbon.png')
    # Removing carbon.png after uploading
    await e.delete()  # Deleting msg


@borg.on(admin_cmd(pattern=f"kar4(?: |$)(.*)", outgoing=True))
async def carbon_api(e):
    """ A Wrapper for carbon.now.sh """
    await e.edit("🌚🌚🌚🌚🌚")
    CARBON = 'https://carbon.now.sh/?bg=rgba(29%2C40%2C104%2C1)&t=one-light&wt=none&l=application%2Ftypescript&ds=true&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Hack&fs=14px&lh=143%25&si=false&es=2x&wm=false&code={code}'
    CARBONLANG = "tr"
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[6:]:
        pcode = str(pcode[6:])
    elif textx:
        pcode = str(textx.message)  # Importing message to module
    code = quote_plus(pcode)  # Converting to urlencoded
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = Config.CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')
    prefs = {'download.default_directory': './'}
    chrome_options.add_experimental_option('prefs', prefs)
    await e.edit("🌝🌝🌚🌚🌚")

    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER,
        options=chrome_options)
    driver.get(url)
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_path}}
    driver.execute("send_command", params)

    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    await asyncio.sleep(2)
    await e.edit("🌝🌝🌝🌚🌚")
    # driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
    await asyncio.sleep(2)  # Waiting for downloading

    await e.edit("🌝🌝🌝🌝🌝")
    file = './carbon.png'
    await e.edit("✅Karbon 4 Tamamlandı, Karbon Yükleniyor✅")
    await e.client.send_file(
        e.chat_id,
        file,
        caption=f"İşte Karbon4'ün ",
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )

    os.remove('./carbon.png')
    # Removing carbon.png after uploading
    await e.delete()  # Deleting msg


@borg.on(admin_cmd(pattern=f"rgbk2(?: |$)(.*)", outgoing=True))
async def carbon_api(e):
    RED = random.randint(0, 256)
    GREEN = random.randint(0, 256)
    BLUE = random.randint(0, 256)
    OPC = random.random()
    await e.edit("⬜⬜⬜⬜⬜")
    CARBON = 'https://carbon.now.sh/?bg=rgba({R}%2C{G}%2C{B}%2C{O})&t=material&wt=none&l=auto&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Fira%20Code&fs=14px&lh=152%25&si=false&es=2x&wm=false&code={code}'
    CARBONLANG = "tr"
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[7:]:
        pcode = str(pcode[7:])
    elif textx:
        pcode = str(textx.message)  # Importing message to module
    code = quote_plus(pcode)  # Converting to urlencoded
    url = CARBON.format(
        code=code,
        R=RED,
        G=GREEN,
        B=BLUE,
        O=OPC,
        lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = Config.CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')
    prefs = {'download.default_directory': './'}
    chrome_options.add_experimental_option('prefs', prefs)
    await e.edit("⬛⬛⬜⬜⬜")

    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER,
        options=chrome_options)
    driver.get(url)
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_path}}
    driver.execute("send_command", params)

    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    await asyncio.sleep(2)  # this might take a bit.
   # driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
    # await asyncio.sleep(5)
    await e.edit("⬛⬛⬛⬜⬜")
    # driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
    await asyncio.sleep(2)  # Waiting for downloading

    await e.edit("⬛⬛⬛⬛⬛")
    file = './carbon.png'
    await e.edit("✅RGB Karbon 2.0 Tamamlandı, Yükleniyor Karbon✅")
    await e.client.send_file(
        e.chat_id,
        file,
        caption=f"İşte karbonrgb'niz",
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )
    os.remove('./carbon.png')
    # Removing carbon.png after uploading
    await e.delete()  # Deleting msg


@borg.on(admin_cmd(pattern=f"kargb(?: |$)(.*)", outgoing=True))
async def carbon_api(e):
    RED = random.randint(0, 256)
    GREEN = random.randint(0, 256)
    BLUE = random.randint(0, 256)
    THEME = ["3024-night",
             "a11y-dark",
             "blackboard",
             "base16-dark",
             "base16-light",
             "cobalt",
             "dracula",
             "duotone-dark",
             "hopscotch",
             "lucario",
             "material",
             "monokai",
             "night-owl",
             "nord",
             "oceanic-next",
             "one-light",
             "one-dark",
             "panda-syntax",
             "paraiso-dark",
             "seti",
             "shades-of-purple",
             "solarized",
             "solarized%20light",
             "synthwave-84",
             "twilight",
             "verminal",
             "vscode",
             "yeti",
             "zenburn",
             ]
    CUNTHE = random.randint(0, len(THEME) - 1)
    The = THEME[CUNTHE]
    await e.edit("⬜⬜⬜⬜⬜")
    CARBON = 'https://carbon.now.sh/?bg=rgba({R}%2C{G}%2C{B}%2C1)&t={T}&wt=none&l=auto&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Fira%20Code&fs=14px&lh=152%25&si=false&es=2x&wm=false&code={code}'
    CARBONLANG = "tr"
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[7:]:
        pcode = str(pcode[7:])
    elif textx:
        pcode = str(textx.message)  # Importing message to module
    code = quote_plus(pcode)  # Converting to urlencoded
    url = CARBON.format(
        code=code,
        R=RED,
        G=GREEN,
        B=BLUE,
        T=The,
        lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = Config.CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')
    prefs = {'download.default_directory': './'}
    chrome_options.add_experimental_option('prefs', prefs)
    await e.edit("⬛⬛⬜⬜⬜")

    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER,
        options=chrome_options)
    driver.get(url)
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_path}}
    driver.execute("send_command", params)
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    await asyncio.sleep(2)  # this might take a bit.
  #  driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
   # await asyncio.sleep(5)
    await e.edit("⬛⬛⬛⬜⬜")
    # driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
    await asyncio.sleep(2)  # Waiting for downloading
    await e.edit("⬛⬛⬛⬛⬛")
    file = './carbon.png'
    await e.edit("✅RGB Karbon Tamamlandı, Karbon Yükleniyor✅")
    await e.client.send_file(
        e.chat_id,
        file,
        caption=f"İşte karbonrgb'niz",
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )
    os.remove('./carbon.png')
    await e.delete()  # Deleting msg


CMD_HELP.update({"carbon": "**PLUGİN İSMİ:** `carbon`\
      \n\n**📌Komut ➥ **`.carbon` <koda cevap ver> :\
      \n**Kullanım ➥ ** Kodunuzu farklı bir tarzda gösterir.\
      \n**Benzer farklı stilleri deneyin**\
      \n`.kar1` <koda cevap ver>\
      \n`.kar2` <koda cevap ver>\
      \n`.kar3` <koda cevap ver>\
      \n`.kar4` <koda cevap ver>\
      \n`.rgbk2` <koda cevap ver>\
      \n`.kargb` <koda cevap ver>\
      "
                 })
