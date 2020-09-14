# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

""" Belirtilen cihaz hakkında bilgi topalayan UserBot modülü. """

import re
import json
from .. import CMD_HELP
from requests import get
from bs4 import BeautifulSoup
from ..utils import admin_cmd, sudo_cmd, edit_or_reply

GITHUB = 'https://github.com'
DEVICES_DATA = 'https://raw.githubusercontent.com/androidtrackers/' \
               'certified-android-devices/master/devices.json'


@borg.on(admin_cmd(pattern=r"magisk$"))
@borg.on(sudo_cmd(pattern=r"magisk$", allow_sudo=True))
async def kakashi(magisk):
    """ magisk latest releases """
    releases = (
        "__**Latest Magisk Releases:**__\n\n"
        f"**Stable : **[ZIP v20.4](https://github.com/topjohnwu/Magisk/releases/download/v20.4/Magisk-v20.4.zip) | [ZIP v20.3](https://bit.ly/3hXLF3L) | [Uninstaller](https://github.com/topjohnwu/Magisk/releases/download/v20.4/Magisk-uninstaller-20200323.zip)\n"
        f"**Magisk Manager : **[APK v7.5.0](https://bit.ly/31U1C5F)\n"
        f"**Canary : **[ZIP vcd6eca1d](https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/magisk-release.zip) | [Uninstaller](https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/magisk-uninstaller.zip)\n"
        f"**Canary Build : **[APK v87de0e7a](https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/app-release.apk)")
    await edit_or_reply(magisk, releases)


@borg.on(admin_cmd(outgoing=True, pattern=r"device(?: |$)(\S*)"))
@borg.on(sudo_cmd(pattern=r"device(?: |$)(\S*)", allow_sudo=True))
async def device_info(request):
    """ kod adından android cihaz temel bilgilerini alın """
    textx = await request.get_reply_message()
    codename = request.pattern_match.group(1)
    if codename:
        pass
    elif textx:
        codename = textx.text
    else:
        await edit_or_reply(request, "`Kullanımı: .device <codename> / <model>`")
        return
    data = json.loads(
        get("https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_device.json").text)
    results = data.get(codename)
    if results:
        reply = f"**için arama sonuçları{codename}**:\n\n"
        for item in results:
            reply += f"**Marka**: {item['brand']}\n" \
                     f"**İsim**: {item['name']}\n" \
                     f"**Model**: {item['model']}\n\n"
    else:
        reply = f"`Hakkında hiç bir bilgi toplayamadım :  {codename}!`\n"
    await edit_or_reply(request, reply)


@borg.on(admin_cmd(outgoing=True,
                   pattern=r"codename(?: |)([\S]*)(?: |)([\s\S]*)"))
@borg.on(
    sudo_cmd(
        pattern=r"codename(?: |)([\S]*)(?: |)([\s\S]*)",
        allow_sudo=True))
async def codename_info(request):
    """ android kod'u bulucu """
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()

    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(' ')[0]
        device = ' '.join(textx.text.split(' ')[1:])
    else:
        await edit_or_reply(request, "`Kullanım : <cihazKodu> <marka> <cihaz>`")
        return

    data = json.loads(
        get("https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_brand.json").text)
    devices_lower = {k.lower(): v
                     for k, v in data.items()}  # Lower brand names in JSON
    devices = devices_lower.get(brand)
    results = [
        i for i in devices if i["name"].lower() == device.lower()
        or i["model"].lower() == device.lower()
    ]
    if results:
        reply = f"**için arama sonuçları {brand} {device}**:\n\n"
        if len(results) > 8:
            results = results[:8]
        for item in results:
            reply += f"**Marka**: {item['device']}\n" \
                     f"**İsim**: {item['name']}\n" \
                     f"**Model**: {item['model']}\n\n"
    else:
        reply = f"`Hata, {device} 'i bulamadım!`\n"
    await edit_or_reply(request, reply)


@borg.on(admin_cmd(outgoing=True,
                   pattern=r"specs(?: |)([\S]*)(?: |)([\s\S]*)"))
@borg.on(
    sudo_cmd(
        pattern=r"specs(?: |)([\S]*)(?: |)([\s\S]*)",
        allow_sudo=True))
async def devices_specifications(request):
    """ Cihaz Özellikleri """
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(' ')[0]
        device = ' '.join(textx.text.split(' ')[1:])
    else:
        await edit_or_reply(request, "`Kullanım: .specs <marka> <cihaz>`")
        return
    all_brands = BeautifulSoup(
        get('https://www.devicespecifications.com/en/brand-more').content,
        'lxml').find('div', {
            'class': 'brand-listing-container-news'
        }).findAll('a')
    brand_page_url = None
    try:
        brand_page_url = [
            i['href'] for i in all_brands if brand == i.text.strip().lower()
        ][0]
    except IndexError:
        await edit_or_reply(request, f'`{brand}  bilinmeyen marka!`')
        return
    devices = BeautifulSoup(get(brand_page_url).content, 'lxml') \
        .findAll('div', {'class': 'model-listing-container-80'})
    device_page_url = None
    try:
        device_page_url = [
            i.a['href']
            for i in BeautifulSoup(str(devices), 'lxml').findAll('h3')
            if device in i.text.strip().lower()
        ]
    except IndexError:
        await edit_or_reply(request, f"`Bulamadım : {device}!`")
        return
    if len(device_page_url) > 2:
        device_page_url = device_page_url[:2]
    reply = ''
    for url in device_page_url:
        info = BeautifulSoup(get(url).content, 'lxml')
        reply = '\n' + info.title.text.split('-')[0].strip() + '\n'
        info = info.find('div', {'id': 'model-brief-specifications'})
        specifications = re.findall(r'<b>.*?<br/>', str(info))
        for item in specifications:
            title = re.findall(r'<b>(.*?)</b>', item)[0].strip()
            data = re.findall(r'</b>: (.*?)<br/>', item)[0] \
                .replace('<b>', '').replace('</b>', '').strip()
            reply += f'**{title}**: {data}\n'
    await edit_or_reply(request, reply)


@borg.on(admin_cmd(outgoing=True, pattern=r"twrp(?: |$)(\S*)"))
@borg.on(sudo_cmd(pattern=r"twrp(?: |$)(\S*)", allow_sudo=True))
async def twrp(request):
    """ android cihaz twrp alın """
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(' ')[0]
    else:
        await edit_or_reply(request, "`Kullanımı: .twrp <kodadı>`")
        return
    url = get(f'https://dl.twrp.me/{device}/')
    if url.status_code == 404:
        reply = f"`İçin twrp indirmeleri bulunamadı {device}!`\n"
        await edit_or_reply(request, reply)
        return
    page = BeautifulSoup(url.content, 'lxml')
    download = page.find('table').find('tr').find('a')
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = f'**İçin en son TWRP {device}:**\n' \
        f'[{dl_file}]({dl_link}) - __{size}__\n' \
        f'**Güncellenmiş:** __{date}__\n'
    await edit_or_reply(request, reply)

CMD_HELP.update({"android": "**PLUGİN İSMİ:** `android`\
      \n\n**📌Komut ➥ **`.magisk` :\
      \n**Kullanım ➥ ** En son Magisk sürümlerini alın.\
      \n\n**📌Komut ➥ **`.device <codename>` :\
      \n**Kullanım ➥ ** Android cihaz kod adı veya modeli hakkında bilgi alın.\
      \n\n**📌Komut ➥ ** `.codename <marka> <cihaz>`\
      \n**Kullanım ➥ ** Android cihaz kod adını ara.\
      \n\n**📌Komut ➥ **`.specs <marka> <cihaz>` :\
      \n**Kullanım ➥ ** Cihaz teknik özellikleri bilgilerini alın.\
      \n\n**📌Komut ➥ **`.twrp <codename>` :\
      \n**Kullanım ➥ ** Android cihaz için en son twrp indirmesini edinin."
                 })
