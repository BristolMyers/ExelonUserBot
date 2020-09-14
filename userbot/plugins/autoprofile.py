# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import asyncio
import time
from telethon.tl import functions
from telethon.errors import FloodWaitError
from userbot.utils import admin_cmd
from userbot import AUTONAME, CMD_HELP, DEFAULT_BIO
import random
import pybase64
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
import shutil

DEFAULTUSERBIO = str(DEFAULT_BIO) if DEFAULT_BIO else " Bekleme Süresi "
DEL_TIME_OUT = 60
DEFAULTUSER = str(AUTONAME) if AUTONAME else "exelon"

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"


@borg.on(admin_cmd(pattern="autopic$"))
async def autopic(event):
    await event.edit(f"`Auto Profil, Ustam tarafından başlatıldı`")
    downloaded_file_name = "userbot/original_pic.png"
    downloader = SmartDL(
        Var.DOWNLOAD_PFP_URL_CLOCK,
        downloaded_file_name,
        progress_bar=False)
    downloader.start(blocking=False)
    photo = "userbot/photo_pfp.png"
    while not downloader.isFinished():
        pass
    counter = -60
    while True:
        shutil.copy(downloaded_file_name, photo)
        im = Image.open(photo)
        file_test = im.rotate(counter, expand=False).save(photo, "PNG")
        current_time = datetime.now().strftime("  Time: %H:%M \n  Date: %d.%m.%y ")
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
        drawn_text.text((150, 250), current_time, font=fnt, fill=(124, 252, 0))
        img.save(photo)
        file = await bot.upload_file(photo)  # pylint:disable=E0602
        try:
            await bot(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
                file
            ))
            os.remove(photo)
            counter -= 60
            await asyncio.sleep(60)
        except BaseException:
            return


@borg.on(admin_cmd(pattern="digitalpfp$"))
async def main(event):
    await event.edit("`Dijital Profil Resminin başlatılması 5 saniyede sihir görür.`")
    poto = "userbot/poto_pfp.png"
    exelon = str(pybase64.b64decode(
        "aHR0cHM6Ly90ZWxlZ3JhLnBoL2ZpbGUvYWVhZWJlMzNiMWYzOTg4YTBiNjkwLmpwZw=="))[2:51]
    downloaded_file_name = "userbot/digital_pic.png"
    downloader = SmartDL(exelon, downloaded_file_name, progress_bar=True)
    downloader.start(blocking=False)
    await asyncio.sleep(5)
    while True:
        shutil.copy(downloaded_file_name, poto)
        Image.open(poto)
        current_time = datetime.now().strftime("%H:%M")
        img = Image.open(poto)
        drawn_text = ImageDraw.Draw(img)
        exelon = str(pybase64.b64decode(
            "dXNlcmJvdC9oZWxwZXJzL3N0eWxlcy9kaWdpdGFsLnR0Zg=="))[2:36]
        fnt = ImageFont.truetype(exelon, 200)
        drawn_text.text((350, 100), current_time, font=fnt, fill=(124, 252, 0))
        img.save(poto)
        file = await event.client.upload_file(poto)
        await event.client(functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1)))
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.remove(poto)
        await asyncio.sleep(60)


@borg.on(admin_cmd(pattern="bloom$"))
async def autopic(event):
    await event.edit("`Bloom renk profili resmi ustam tarafından etkinleştirildi`")
    downloaded_file_name = "userbot/original_pic.png"
    downloader = SmartDL(
        Var.DOWNLOAD_PFP_URL_CLOCK,
        downloaded_file_name,
        progress_bar=True)
    downloader.start(blocking=False)
    photo = "userbot/photo_pfp.png"
    while not downloader.isFinished():
        pass
    while True:
        # RIP Tehlike bölgesi Burada düzenleme yok plox
        R = random.randint(0, 256)
        B = random.randint(0, 256)
        G = random.randint(0, 256)
        FR = (256 - R)
        FB = (256 - B)
        FG = (256 - G)
        shutil.copy(downloaded_file_name, photo)
        image = Image.open(photo)
        image.paste((R, G, B), [0, 0, image.size[0], image.size[1]])
        image.save(photo)
        current_time = datetime.now().strftime("\n Time: %H:%M:%S \n \n Date: %d/%m/%y")
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 60)
        ofnt = ImageFont.truetype(FONT_FILE_TO_USE, 250)
        drawn_text.text((95, 250), current_time, font=fnt, fill=(FR, FG, FB))
        drawn_text.text((95, 250), "      😈", font=ofnt, fill=(FR, FG, FB))
        img.save(photo)
        file = await event.client.upload_file(photo)  # pylint:disable=E0602
        try:
            await event.client(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
                file
            ))
            os.remove(photo)
            await asyncio.sleep(30)
        except BaseException:
            return


@borg.on(admin_cmd(pattern="autoname$"))  # pylint:disable=E0602
async def _(event):
    await event.edit(f"Otomatik Ad, Ustam tarafından başlatıldı ")
    while True:
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%H:%M")
        name = f"⌚️ {HM}||›  {DEFAULTUSER} ‹||📅 {DM}"
        logger.info(name)
        try:
            await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                first_name=name
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)

        # else:
            # logger.info(r.stringify())
            # await borg.send_message(  # pylint:disable=E0602
            #     Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
            #     "Successfully Changed Profile Name"
            # )
        await asyncio.sleep(DEL_TIME_OUT)


@borg.on(admin_cmd(pattern="autobio$"))  # pylint:disable=E0602
async def _(event):
    await event.edit(f"`Oto biyografim Ustam tarafından başlatıldı`")
    while True:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio = f"📅 {DMY} | {DEFAULTUSERBIO} | ⌚️ {HM}"
        logger.info(bio)
        try:
            await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                about=bio
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        # else:
            # logger.info(r.stringify())
            # await borg.send_message(  # pylint:disable=E0602
            #     Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
            #     "Changed Profile Picture"
            # )
        await asyncio.sleep(DEL_TIME_OUT)

BIO_STRINGS = [
    "👉⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️🔲",
    "⬜️👉⬛️⬛️⬛️⬛️⬛️⬛️⬛️🔲",
    "⬜️⬜️👉⬛️⬛️⬛️⬛️⬛️⬛️🔲",
    "⬜️⬜️⬜️👉⬛️⬛️⬛️⬛️⬛️🔲",
    "⬜️⬜️⬜️⬜️👉⬛️⬛️⬛️⬛️🔲",
    "⬜️⬜️⬜️⬜️⬜️👉⬛️⬛️⬛️🔲",
    "⬜️⬜️⬜️⬜️⬜️⬜️👉⬛️⬛️🔲",
    "⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉⬛️🔲",
    "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉🔲",
    "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉🔳",
    "⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉⬜️🔳",
    "⬜️⬜️⬜️⬜️⬜️⬜️👉⬜️⬜️🔳",
    "⬜️⬜️⬜️⬜️⬜️👉⬜️⬜️⬜️🔳",
    "⬜️⬜️⬜️⬜️👉⬜️⬜️⬜️⬜️🔳",
    "⬜️⬜️⬜️👉⬜️⬜️⬜️⬜️⬜️🔳",
    "⬜️⬜️👉⬜️⬜️⬜️⬜️⬜️⬜️🔳",
    "⬜️👉⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳",
    "👉⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳",
    "🐵",
    "🙈",
    "🙉",
    "🙊",
    "🐵",
    "🐵",
    "🙈",
    "🙉",
    "🙊",
    "🐵",
    "👉⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️🔲",
    "⬜️👉⬛️⬛️⬛️⬛️⬛️⬛️⬛️🔲",
    "⬜️⬜️👉⬛️⬛️⬛️⬛️⬛️⬛️🔲",
    "⬜️⬜️⬜️👉⬛️⬛️⬛️⬛️⬛️🔲",
    "⬜️⬜️⬜️⬜️👉⬛️⬛️⬛️⬛️🔲",
    "⬜️⬜️⬜️⬜️⬜️👉⬛️⬛️⬛️🔲",
    "⬜️⬜️⬜️⬜️⬜️⬜️👉⬛️⬛️🔲",
    "⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉⬛️🔲",
    "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉🔲",
    "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉🔳",
    "⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉⬜️🔳",
    "⬜️⬜️⬜️⬜️⬜️⬜️👉⬜️⬜️🔳",
    "⬜️⬜️⬜️⬜️⬜️👉⬜️⬜️⬜️🔳",
    "⬜️⬜️⬜️⬜️👉⬜️⬜️⬜️⬜️🔳",
    "⬜️⬜️⬜️👉⬜️⬜️⬜️⬜️⬜️🔳",
    "⬜️⬜️👉⬜️⬜️⬜️⬜️⬜️⬜️🔳",
    "⬜️👉⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳",
    "👉⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳",
    "🐵",
    "🙈",
    "🙉",
    "🙊",
    "🐵",
    "🐵",
    "🙈",
    "🙉",
    "🙊",
    "🐵",
]


@borg.on(admin_cmd(pattern="monkeybio$"))  # pylint:disable=E0602
async def _(event):
    await event.edit(f"`maymun Ustam tarafından başlatıldı`")
    while True:
        bro = random.randint(0, len(BIO_STRINGS) - 1)
        #input_str = event.pattern_match.group(1)
        Bio = BIO_STRINGS[bro]
        time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        #bio = f"📅 {DMY} | ᗯᗩᏆᎢᏆᑎᏀ ᏞᏆᏦᗴ ᎢᏆᗰᗴ | ⌚️ {HM}"
        logger.info(Bio)
        try:
            await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                about=Bio
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        # else:
            # logger.info(r.stringify())
            # await borg.send_message(  # pylint:disable=E0602
            #     Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
            #     "Successfully Changed Profile Bio"
            # )
        await asyncio.sleep(DEL_TIME_OUT)


CMD_HELP.update({"autoprofile": "**PLUGİN İSMİ:** autoprofile\
      \n\n**📌Komut ➥ **`.autopic`\
      \n**Kullanım ➥  Görüntü üzerinde zamanla birlikte döndürülüyor.\
      \nBunu çalışmak için önce heroku değişkeninde `DOWNLOAD_PFP_URL_CLOCK` ayarını gerekli görüntünün telgraf bağlantısı ile ayarlamalısınız!!\
      \n\n**📌Komut ➥**  `.digitalpfp`\
      \nKullanım ➥  Profil resminiz digitaltime profil resmine dönüşür!\
      \n\n**📌Komut ➥** `.bloom`\
      \n**Kullanım ➥**  Rastgele renkli profil resimleri, zamanla birlikte ayarlanacaktır.\
      \nBunu çalışmak için önce heroku değişkeninde \"DOWNLOAD_PFP_URL_CLOCK\" ayarını gerekli görüntünün telgraf bağlantısı ile ayarlamalısınız!!\
      \n\n**📌Komut ➥** `.autoname`\
      \n**Kullanım ➥**  Adın yanı sıra bunun çalışabilmesi için önce heroku değişkeninde `AUTONAME` ayarlamalısınız!!\
      \n\n**📌Komut ➥** `.autobio`\
      \n**Kullanım ➥**  Biyografinizle birlikte bunun çalışması için önce heroku değişkeninde `DEFAULT_BIO` ayarlamalısınız!!\
      n\n**📌Komut ➥** `.monkeybio`\
      \n**Kullanım ➥**  Komik maymun biyo kümesi.\
      \n\n bu aby komutunu durdurmak için .restart yapmanız ve bunları manuel olarak değiştirmeniz gerekir!!"
                 })
