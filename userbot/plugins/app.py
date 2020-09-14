# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import bs4
import requests
from .. import CMD_HELP, ALIVE_NAME
from ..utils import admin_cmd, sudo_cmd, edit_or_reply

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "exelon"


@borg.on(admin_cmd(pattern="app (.*)"))
@borg.on(sudo_cmd(pattern="app (.*)", allow_sudo=True))
async def apk(event):
    app_name = event.pattern_match.group(1)
    event = await edit_or_reply(event, "Aranıyor!")
    try:
        remove_space = app_name.split(' ')
        final_name = '+'.join(remove_space)
        page = requests.get(
            "https://play.google.com/store/search?q=" +
            final_name +
            "&c=apps")
        str(page.status_code)
        soup = bs4.BeautifulSoup(page.content, 'lxml', from_encoding='utf-8')
        results = soup.findAll("div", "ZmHEEd")
        app_name = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'WsMG1c nnK0zc').text
        app_dev = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'KoLSrc').text
        app_dev_link = "https://play.google.com" + \
            results[0].findNext('div', 'Vpfmgd').findNext('a', 'mnKHRc')['href']
        app_rating = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'pf5lIe').find('div')['aria-label']
        app_link = "https://play.google.com" + \
            results[0].findNext('div', 'Vpfmgd').findNext('div', 'vU6FJ p63iDd').a['href']
        app_icon = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'uzcko').img['data-src']
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += "\n\n<code>Kurucu :</code> <a href='" + \
            app_dev_link + "'>" + app_dev + "</a>"
        app_details += "\n<code>değerlendirme:</code> " + app_rating.replace(
            "Rated ", "⭐ ").replace(
            " out of ", "/").replace(
            " stars", "", 1).replace(
                " stars", "⭐ ").replace(
                    "five", "5")
        app_details += "\n<code>Özellikleri :</code> <a href='" + \
            app_link + "'>View in Play Store</a>"
        app_details += f"\n\n===> {DEFAULTUSER} <==="
        await event.edit(app_details, link_preview=True, parse_mode='HTML')
    except IndexError:
        await event.edit("Aramada sonuç bulunamadı. Lütfen Geçerli **uygulama** adını girin")
    except Exception as err:
        await event.edit("Exception Occured:- " + str(err))


@borg.on(admin_cmd(pattern="appr (.*)"))
@borg.on(sudo_cmd(pattern="appr (.*)", allow_sudo=True))
async def apkr(event):
    app_name = event.pattern_match.group(1)
    event = await edit_or_reply(event, "Aranıyor!")
    try:
        remove_space = app_name.split(' ')
        final_name = '+'.join(remove_space)
        page = requests.get(
            "https://play.google.com/store/search?q=" +
            final_name +
            "&c=apps")
        str(page.status_code)
        soup = bs4.BeautifulSoup(page.content, 'lxml', from_encoding='utf-8')
        results = soup.findAll("div", "ZmHEEd")
        app_name = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'WsMG1c nnK0zc').text
        app_dev = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'KoLSrc').text
        app_dev_link = "https://play.google.com" + \
            results[0].findNext('div', 'Vpfmgd').findNext('a', 'mnKHRc')['href']
        app_rating = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'pf5lIe').find('div')['aria-label']
        app_link = "https://play.google.com" + \
            results[0].findNext('div', 'Vpfmgd').findNext('div', 'vU6FJ p63iDd').a['href']
        app_icon = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'uzcko').img['data-src']
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += "\n\n<code>Kurucu :</code> <a href='" + \
            app_dev_link + "'>" + app_dev + "</a>"
        app_details += "\n<code>değerlendirme:</code> " + app_rating.replace(
            "Rated ", "⭐ ").replace(
            " out of ", "/").replace(
            " stars", "", 1).replace(
                " stars", "⭐ ").replace(
                    "five", "5")
        app_details += "\n<code>Özellikleri :</code> <a href='" + \
            app_link + "'>View in Play Store</a>"
        app_details += "\n\n<b>Download : </b> <a href='https://t.me/joinchat/ExelonSupport'>Request_Here</a>"
        app_details += "\n\n===> @BrsitolMyers <==="
        await event.edit(app_details, link_preview=True, parse_mode='HTML')
    except IndexError:
        await event.edit("Aramada sonuç bulunamadı. Lütfen Geçerli **uygulama** adını girin**")
    except Exception as err:
        await event.edit("Exception Occured:- " + str(err))


CMD_HELP.update({"app": "**PLUGİN İSMİ:** `app`\
      \n\n**📌Komut ➥ **`.app [Uygulama adı]` :\
      \n**Kullanım ➥ ** Play Store'da uygulamayı arar ve Play Store'da uygulamanın bağlantısını sağlar ve uygulama ayrıntılarını getirir.\
      \n\n**📌Komut ➥ **`.appr [Uygulama adı]` :\
      \n**Kullanım ➥ ** Play Store'da uygulamayı arar ve Play Store'daki uygulamaya bağlantı sağlar ve Exelon istek bağlantısıyla uygulama ayrıntılarını getirir."
                 })
