# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

""" Kızartma malzemeleri için Userbot modülü. @BristolMyers tarafından """

import io
from .. import CMD_HELP
from telethon import events
from random import randint, uniform
from PIL import Image, ImageEnhance, ImageOps
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from telethon.tl.types import DocumentAttributeFilename
from telethon.errors.rpcerrorlist import YouBlockedUserError


@borg.on(admin_cmd(pattern="frybot$"))
@borg.on(sudo_cmd(pattern="frybot$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        event = await edit_or_reply(event, "Herhangi bir kullanıcı mesajını yanıtlayın.")
        return
    reply_message = await event.get_reply_message()
    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await check_media(reply_message)
        if isinstance(data, bool):
            event = await edit_or_reply(event, "`Bunu derin kızartamam!`")
            return
    if not event.is_reply:
        event = await edit_or_reply(event, "`Derin kızartmak için bir görüntüyü veya çıkartmayı yanıtlayın!`")
        return
    chat = "@image_deepfrybot"
    reply_message.sender
    if reply_message.sender.bot:
        event = await edit_or_reply(event, "Gerçek kullanıcıların mesajını yanıtlayın.")
        return
    event = await edit_or_reply(event, "```İşleniyor```")
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=432858024))
            await borg.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("@image_deepfrybot engelini kaldırın ve tekrar deneyin")
            return
        await bot.send_read_acknowledge(conv.chat_id)
        if response.text.startswith("İleri"):
            await event.edit("```ileri gizlilik ayarlarınızı tamamen devre dışı bırakabilir misiniz?```")
        else:
            await borg.send_file(event.chat_id, response.message.media)
        await event.delete()


@borg.on(admin_cmd(pattern="deepfry(?: |$)(.*)", outgoing=True))
@borg.on(sudo_cmd(pattern="deepfry(?: |$)(.*)", allow_sudo=True))
async def deepfryer(event):
    try:
        frycount = int(event.pattern_match.group(1))
        if frycount < 1:
            raise ValueError
    except ValueError:
        frycount = 1
    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await check_media(reply_message)
        if isinstance(data, bool):
            event = await edit_or_reply(event, "`Bunu derin kızartamam!`")
            return
    if not event.is_reply:
        event = await edit_or_reply(event, "`Derin kızartmak için bir görüntüyü veya çıkartmayı yanıtlayın!`")
        return
    # download last photo (highres) as byte array
    image = io.BytesIO()
    await event.client.download_media(data, image)
    image = Image.open(image)
    # fry the image
    hmm = await edit_or_reply(event, "`Derin kızartma ortamı…`")
    for _ in range(frycount):
        image = await deepfry(image)
    fried_io = io.BytesIO()
    fried_io.name = "image.jpeg"
    image.save(fried_io, "JPEG")
    fried_io.seek(0)
    await event.reply(file=fried_io)
    await hmm.delete()


async def deepfry(img: Image) -> Image:
    colours = (
        (randint(50, 200), randint(40, 170), randint(40, 190)),
        (randint(190, 255), randint(170, 240), randint(180, 250))
    )
    img = img.copy().convert("RGB")
    # Crush image to hell and back
    img = img.convert("RGB")
    width, height = img.width, img.height
    img = img.resize((int(width ** uniform(0.8, 0.9)),
                      int(height ** uniform(0.8, 0.9))), resample=Image.LANCZOS)
    img = img.resize((int(width ** uniform(0.85, 0.95)),
                      int(height ** uniform(0.85, 0.95))), resample=Image.BILINEAR)
    img = img.resize((int(width ** uniform(0.89, 0.98)),
                      int(height ** uniform(0.89, 0.98))), resample=Image.BICUBIC)
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, randint(3, 7))
    # Generate colour overlay
    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageEnhance.Brightness(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageOps.colorize(overlay, colours[0], colours[1])
    # Overlay red and yellow onto main image and sharpen the hell out of it
    img = Image.blend(img, overlay, uniform(0.1, 0.4))
    img = ImageEnhance.Sharpness(img).enhance(randint(5, 300))
    return img


async def check_media(reply_message):
    if reply_message and reply_message.media:
        if reply_message.photo:
            data = reply_message.photo
        elif reply_message.document:
            if DocumentAttributeFilename(
                    file_name='AnimatedSticker.tgs') in reply_message.media.document.attributes:
                return False
            if reply_message.gif or reply_message.video or reply_message.audio or reply_message.voice:
                return False
            data = reply_message.media.document
        else:
            return False
    if not data or data is None:
        return False
    return data


CMD_HELP.update({"fryer": "**PLUGİN İSMİ:** `fryer`:\
      \n\n**📌Komut ➥ **`.frybot` resme veya çıkartmaya yanıt ver\
      \n**Kullanım ➥ ** Verilen metni buharlaştırın.\
      \n\n**📌Komut ➥ ** `.deepfry` <1 ile 9> `resme veya çıkartmaya yanıt\
      \n**Kullanım ➥ ** Verilen çıkartmayı veya resmi seviyeye göre kızartır, eğer hiçbir şey vermezseniz varsayılan olarak 1'dir."
                 })
