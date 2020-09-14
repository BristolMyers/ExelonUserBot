# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""
Let me Google / YouTube / DuckDuckGo / altnews / Xvideo / Pornhub / var / log / dyno that for you!
Syntax:
 .lmg <arama sorgusu>
 .lmy <arama sorgusu>
 .ddg <arama sorgusu>
 .lmalt <haber ara>
 .lmx <porno ara>
 .lmx2 <porno ara>
 .lmp <porno ara>
 .lmvar <heroku app name>
 .lmlog <heroku app name>
 .dyno <type billing>
 .lmkp <indiankanoon.com'daki gibi yerin adını yazın>
 .lmki <İndiankanoon.com'daki gibi öğenin adını yazın>
 .gem <Gem.gov.in'deki gibi öğenin adını yazın>
 .archive <Wayback makinesi hakkında bilgi almak istediğiniz web sitesinin adını yazın>
"""


import requests
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="lmg (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=http://google.com/search?q={}".format(
        input_str.replace(" ", "+"))
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("İzin ver** Googal** senin için arama yapsın:\n👉 [{}]({})\n`Sonra teşekkür et😉` ".format(input_str, response_api.rstrip()))
    else:
        await event.edit("Bir şeyler yanlış gitti. Lütfen daha sonra tekrar deneyiniz.")


@borg.on(admin_cmd(pattern="lmy (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://www.youtube.com/results?search_query={}".format(
        input_str.replace(" ", "+"))
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("İzin ver ** UThoob **senin için arama yapsın:\n👉 [{}]({})\n`Sonra teşekkür et😉` ".format(input_str, response_api.rstrip()))
    else:
        await event.edit("Bir şeyler yanlış gitti. Lütfen daha sonra tekrar deneyiniz.")


@borg.on(admin_cmd(pattern="ddg (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://duckduckgo.com/?q={}&t=h_&ia=about".format(
        input_str.replace(" ", "+"))
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("İzin ver **duckduckgo** senin için arama yapsın:\n👉 [{}]({})\n`Sonra teşekkür et 😉` ".format(input_str, response_api.rstrip()))
    else:
        await event.edit("Bir şeyler yanlış gitti. Lütfen daha sonra tekrar deneyiniz.")


@borg.on(admin_cmd(pattern="lmalt (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://www.altnews.in/?s={}".format(
        input_str.replace(" ", "+"))
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("İzin ver **altnews** senin için arama yapsın:\n👉 [{}]({})\n`Sonra teşekkür et 😉` ".format(input_str, response_api.rstrip()))
    else:
        await event.edit("Bir şeyler yanlış gitti. Lütfen daha sonra tekrar deneyiniz.")


@borg.on(admin_cmd(pattern="lmvar (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://dashboard.heroku.com/apps/{}/settings".format(
        input_str.replace(" ", "+"))
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("İzin ver **var** senin için arama yapsın:\n👉 [{}]({})\n`Sonra teşekkür et 😉` ".format(input_str, response_api.rstrip()))
    else:
        await event.edit("Bir şeyler yanlış gitti. Lütfen daha sonra tekrar deneyiniz.")


@borg.on(admin_cmd(pattern="lmlog (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://dashboard.heroku.com/apps/{}/logs".format(
        input_str.replace(" ", "+"))
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("İzin ver **log** senin için arama yapsın:\n👉 [{}]({})\n`Sonra teşekkür et 😉` ".format(input_str, response_api.rstrip()))
    else:
        await event.edit("Bir şeyler yanlış gitti. Lütfen daha sonra tekrar deneyiniz.")


@borg.on(admin_cmd(pattern="dyno(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://dashboard.heroku.com/account/{}".format(
        input_str.replace(" ", "+"))
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("İzin ver **dyno** senin için arama yapsın:\n👉 [{}]({})\n`Sonra teşekkür et 😉` ".format(input_str, response_api.rstrip()))
    else:
        await event.edit("Bir şeyler yanlış gitti. Lütfen daha sonra tekrar deneyiniz.")


@borg.on(admin_cmd(pattern="lmkp (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://indiankanoon.org/search/?formInput={}+sortby%3Amostrecent".format(
        input_str.replace(" ", "+"))
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("İzin ver **Indiankanoon.com : Place**senin için arama yapsın\n👉 [{}]({})\n`Sonra teşekkür et 😉` ".format(input_str, response_api.rstrip()))
    else:
        await event.edit("Bir şeyler yanlış gitti. Lütfen daha sonra tekrar deneyiniz.")


@borg.on(admin_cmd(pattern="gem (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://mkp.gem.gov.in/search?q={}&sort_type=created_at_desc&_xhr=1".format(
        input_str.replace(" ", "+"))
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("İzin ver **gem.gov.in** senin için arama yapsın:\n👉 [{}]({})\n`Sonra teşekkür et 😉` ".format(input_str, response_api.rstrip()))
    else:
        await event.edit("Bir şeyler yanlış gitti. Lütfen daha sonra tekrar deneyiniz.")


@borg.on(admin_cmd(pattern="archive (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://web.archive.org/web/*/{}".format(
        input_str.replace(" ", "+"))
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("İzin ver run your link on wayback machine that for you:\n👉 [{}]({})\n`Sonra teşekkür et 😉` ".format(input_str, response_api.rstrip()))
    else:
        await event.edit("Bir şeyler yanlış gitti. Lütfen daha sonra tekrar deneyiniz.")
