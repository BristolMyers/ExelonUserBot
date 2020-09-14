# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import requests
from userbot import CMD_HELP
from ..utils import admin_cmd, sudo_cmd, edit_or_reply


@borg.on(admin_cmd(pattern="dns (.*)"))
@borg.on(sudo_cmd(pattern="dns (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/dns/{}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(event, "{} DNS kayıtları \n{}".format(input_str, response_api))
    else:
        await edit_or_reply(event, "İnternette {} bulamıyorum".format(input_str))


@borg.on(admin_cmd(pattern="url (.*)"))
@borg.on(sudo_cmd(pattern="url (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url={}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(event, "{} İçin {} oluşturuldu.".format(response_api, input_str))
    else:
        await edit_or_reply(event, "bir şey yanlış. lütfen daha sonra tekrar deneyiniz.")


@borg.on(admin_cmd(pattern="unshort (.*)"))
@borg.on(sudo_cmd(pattern="unshort (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith('3'):
        await edit_or_reply(event, "Giriş URL'si: {} \n Yeniden Yönlendirilen URL: {}".format(input_str, r.headers["Location"]))
    else:
        await edit_or_reply(event, "Giriş URL'si {} döndürüldü status_code {}".format(input_str, r.status_code))


CMD_HELP.update({"dagd": "**PLUGİN İSMİ:** `dagd`\
      \n\n**📌Komut ➥ **`.dns link` :\
      \n**Kullanım ➥ ** Size verilen bağlantının Alan Adı Sistemini (dns) gösterir. örnek .dns google.com veya .dns github.com.\
      \n\n**📌Komut ➥ **`.url link` :\
      \n**Kullanım ➥ ** verilen bağlantıyı kısaltır.\
      \n\n**📌Komut ➥ ** `.unshort link`\
      \n**Kullanım ➥ ** verilen kısa bağlantıyı kaldırır."
                 })
