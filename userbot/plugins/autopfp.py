# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import requests
import re
import random
import urllib
import os
from telethon.tl import functions
from userbot.utils import admin_cmd
import asyncio
from .. import CMD_HELP

COLLECTION_STRING1 = [
    "awesome-batman-wallpapers",
    "batman-arkham-knight-4k-wallpaper",
    "batman-hd-wallpapers-1080p",
    "the-joker-hd-wallpaper",
    "dark-knight-joker-wallpaper"
]
COLLECTION_STRING2 = [
    "thor-wallpapers",
    "thor-wallpaper",
    "thor-iphone-wallpaper",
    "thor-wallpaper-hd"
]


async def animeppbat():
    rnd = random.randint(0, len(COLLECTION_STRING1) - 1)
    pack = COLLECTION_STRING1[rnd]
    pc = requests.get("http://getwallpapers.com/collection/" + pack).text
    f = re.compile(r'/\w+/full.+.jpg')
    f = f.findall(pc)
    fy = "http://getwallpapers.com" + random.choice(f)
    if not os.path.exists("f.ttf"):
        urllib.request.urlretrieve(
            "https://github.com/rebel6969/mym/raw/master/Rebel-robot-Regular.ttf", "f.ttf")
    urllib.request.urlretrieve(fy, "donottouch.jpg")


async def animeppthor():
    rnd = random.randint(0, len(COLLECTION_STRING2) - 1)
    pack = COLLECTION_STRING2[rnd]
    pc = requests.get("http://getwallpapers.com/collection/" + pack).text
    f = re.compile(r'/\w+/full.+.jpg')
    f = f.findall(pc)
    fy = "http://getwallpapers.com" + random.choice(f)
    if not os.path.exists("f.ttf"):
        urllib.request.urlretrieve(
            "https://github.com/rebel6969/mym/raw/master/Rebel-robot-Regular.ttf", "f.ttf")
    urllib.request.urlretrieve(fy, "donottouch.jpg")


@borg.on(admin_cmd(pattern="batmanpfp$"))
async def main(event):
    # Owner @NihiNivi
    await event.edit("Batman Profil Resmi Otomatik Olarak Değişmeye Başlıyor.")
    while True:
        await animeppbat()
        file = await event.client.upload_file("donottouch.jpg")
        await event.client(functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1)))
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.system("rm -rf donottouch.jpg")
        await asyncio.sleep(120)  # Edit this to your required needs


@borg.on(admin_cmd(pattern="thorpfp$"))
async def main(event):
    # Owner @NihiNivi
    await event.edit("Thor Profil Resmi Otomatik Olarak Değişmeye Başlıyor.")
    while True:
        await animeppthor()
        file = await event.client.upload_file("donottouch.jpg")
        await event.client(functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1)))
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.system("rm -rf donottouch.jpg")
        await asyncio.sleep(120)  # Edit this to your required needs


CMD_HELP.update({"autopfp": "**PLUGİN İSMİ:** `autopfp`\
      \n\n**📌Komut ➥ **`.batmanpfp` :\
      \n**Kullanım ➥ ** Profil resminizi random bir şekilde batman profili yapar.\
      \n\n**📌Komut ➥ **`.thorpfp` :\
      \n**Kullanım ➥ ** Profil resminizi random bir şekilde thor profili yapar."
                 })
