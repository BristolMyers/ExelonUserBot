# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import os
from PIL import Image
from .. import LOGS, CMD_HELP
from telethon import functions, types
from glitch_this import ImageGlitcher
from . import take_screen_shot, runcmd
from ..utils import admin_cmd, sudo_cmd, edit_or_reply


@borg.on(admin_cmd(outgoing=True, pattern="(glitch|glitchs)(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="(glitch|glitchs)(?: |$)(.*)", allow_sudo=True))
async def glitch(exelon):
    cmd = exelon.pattern_match.group(1)
    exeloninput = exelon.pattern_match.group(2)
    reply = await exelon.get_reply_message()
    exelonid = exelon.reply_to_msg_id
    exelon = await edit_or_reply(exelon, "```Glitching... 😁```")
    if not (reply and (reply.media)):
        await exelon.edit("`medya bulunamadı...`")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    exelonsticker = await reply.download_media(file="./temp/")
    if not exelonsticker.endswith(('.mp4', '.webp', '.tgs', '.png', '.jpg')):
        os.remove(exelonsticker)
        await exelon.edit("`Media not found...`")
        return
    os.path.join("./temp/", "glitch.png")
    if exeloninput:
        if not exeloninput.isdigit():
            await exelon.edit("`Girdiğiniz geçersiz, yardıma bakın`")
            return
        exeloninput = int(exeloninput)
        if not 0 < exeloninput < 9:
            await exelon.edit("`Geçersiz Aralık...`")
            return
    else:
        exeloninput = 2
    if exelonsticker.endswith(".tgs"):
        exelonfile = os.path.join("./temp/", "glitch.png")
        exeloncmd = f"lottie_convert.py --frame 0 -if lottie -of png {exelonsticker} {exelonfile}"
        stdout, stderr = (await runcmd(exeloncmd))[:2]
        if not os.path.lexists(exelonfile):
            await exelon.edit("`exelonsticker bulunamadı...`")
            LOGS.info(stdout + stderr)
        glitch_file = exelonfile
    elif exelonsticker.endswith(".webp"):
        exelonfile = os.path.join("./temp/", "glitch.png")
        os.rename(exelonsticker, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("`exelonsticker bulunamadı... `")
            return
        glitch_file = exelonfile
    elif exelonsticker.endswith(".mp4"):
        exelonfile = os.path.join("./temp/", "glitch.png")
        await take_screen_shot(exelonsticker, 0, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("```exelonsticker bulunamadı...```")
            return
        glitch_file = exelonfile
    else:
        glitch_file = exelonsticker
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file)
    if cmd == "glitchs":
        glitched = "./temp/" + "glitched.webp"
        glitch_img = glitcher.glitch_image(img, exeloninput, color_offset=True)
        glitch_img.save(glitched)
        await borg.send_file(
            exelon.chat_id,
            glitched,
            reply_to=exelonid)
        os.remove(glitched)
        await exelon.delete()
    elif cmd == "glitch":
        Glitched = "./temp/" + "glitch.gif"
        glitch_img = glitcher.glitch_image(
            img, exeloninput, color_offset=True, gif=True)
        DURATION = 200
        LOOP = 0
        glitch_img[0].save(
            Glitched,
            format='GIF',
            append_images=glitch_img[1:],
            save_all=True,
            duration=DURATION,
            loop=LOOP)
        sandy = await borg.send_file(
            exelon.chat_id,
            Glitched,
            reply_to=exelonid)
        await borg(functions.messages.SaveGifRequest(
            id=types.InputDocument(
                id=sandy.media.document.id,
                access_hash=sandy.media.document.access_hash,
                file_reference=sandy.media.document.file_reference
            ),
            unsave=True
        ))
        os.remove(Glitched)
        await exelon.delete()
    for files in (exelonsticker, glitch_file):
        if files and os.path.exists(files):
            os.remove(files)

CMD_HELP.update({
    "glitch":
    "**Plugin : **`glitch`\
    \n\n**Syntax : **`.glitch` medya dosyasına yanıtla\
    \n**Usage :** Verilen ortam dosyasını (gif, çıkartmalar, resim, videolar) bir gif'e çevirir ve hata aralığı 1'den 8'e kadardır.\
    Hiçbir şeyden bahsedilmezse, varsayılan olarak 2'dir \
    \n\n**Syntax : **`.glitchs` medya dosyasına yanıtla\
    \n**Usage :** Verilen ortam dosyasını (gif, çıkartmalar, görüntü, videolar) bir çıkartmaya ve hata aralığı 1'den 8'e kadar arızalar.\
    Hiçbir şeyden bahsedilmezse, varsayılan olarak 2'dir\
    "
})
