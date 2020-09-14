# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
import os
from userbot import CMD_HELP
from telethon.tl import functions
from userbot.utils import admin_cmd
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.types import Channel, Chat, InputPhoto, User
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.errors.rpcerrorlist import UsernameOccupiedError


# ====================== CONSTANT ===============================
INVALID_MEDIA = "```Medya varlığının uzantısı geçersiz.```"
PP_CHANGED = "```Profil resmi başarıyla değiştirildi.```"
PP_TOO_SMOL = "```Bu resim çok küçük, daha büyük bir resim kullanın.```"
PP_ERROR = "```Görüntü işlenirken hata oluştu.```"
BIO_SUCCESS = "```Bio başarıyla düzenlendi.```"
NAME_OK = "```Adınız başarıyla değiştirildi.```"
USERNAME_SUCCESS = "```Kullanıcı adınız başarıyla değiştirildi.```"
USERNAME_TAKEN = "```Bu kullanıcı adı zaten alınmış.```"
# ===============================================================


@borg.on(admin_cmd(pattern="pbio (.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    bio = event.pattern_match.group(1)
    try:
        await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            about=bio
        ))
        await event.edit("Profil biyografimi başarıyla değiştirdim")
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))


@borg.on(admin_cmd(pattern="pname ((.|\n)*)"))  # pylint:disable=E0602,W0703
async def _(event):
    if event.fwd_from:
        return
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if "|" in names:
        first_name, last_name = names.split("|", 1)
    try:
        await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            first_name=first_name,
            last_name=last_name
        ))
        await event.edit("İsmim başarıyla değiştirildi")
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))


@borg.on(admin_cmd(pattern="ppic"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    await event.edit("Profil Resmini yerelime indiriyorum...")
    if not os.path.isdir(
            Config.TMP_DOWNLOAD_DIRECTORY):  # pylint:disable=E0602
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)  # pylint:disable=E0602
    photo = None
    try:
        photo = await borg.download_media(  # pylint:disable=E0602
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY  # pylint:disable=E0602
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
    else:
        if photo:
            await event.edit("Şimdi, Telegram'a yüklüyorum...")
            if photo.endswith((".mp4", ".MP4")):
                # https://t.me/tgbetachat/324694
                size = os.stat(photo).st_size
                if size > 2097152:
                    await event.edit("boyut 2 mb'den küçük olmalıdır")
                    os.remove(photo)
                    return
                exelonpic = None
                exelonvideo = await borg.upload_file(photo)
            else:
                exelonpic = await borg.upload_file(photo)  # pylint:disable=E0602
                exelonvideo = None
            try:
                await borg(functions.photos.UploadProfilePhotoRequest(
                    file=exelonpic,
                    video=exelonvideo,
                    video_start_ts=0.01))
            except Exception as e:  # pylint:disable=C0103,W0703
                await event.edit(str(e))
            else:
                await event.edit("Profil resmim başarıyla değiştirildi")
    try:
        os.remove(photo)
    except Exception as e:  # pylint:disable=C0103,W0703
        logger.warn(str(e))  # pylint:


@borg.on(admin_cmd(outgoing=True, pattern="username (.*)"))
async def update_username(username):
    """ .username komutu için Telegram'da yeni bir kullanıcı adı belirleyin. """
    newusername = username.pattern_match.group(1)
    try:
        await username.client(UpdateUsernameRequest(newusername))
        await username.edit(USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await username.edit(USERNAME_TAKEN)


@borg.on(admin_cmd(outgoing=True, pattern="count$"))
async def count(event):
    """ .Count komutu için profil istatistiklerini alın. """
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    await event.edit("`İşleniyor..`")
    dialogs = await bot.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity, User):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity, Chat):
            g += 1
        elif isinstance(currrent_entity, Channel):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1
        else:
            print(d)

    result += f"`Kullanıcılar:`\t**{u}**\n"
    result += f"`Gruplar:`\t**{g}**\n"
    result += f"`Super Gruplar:`\t**{c}**\n"
    result += f"`Kanallar:`\t**{bc}**\n"
    result += f"`Botlar:`\t**{b}**"

    await event.edit(result)


@borg.on(admin_cmd(outgoing=True, pattern=r"delpfp"))
async def remove_profilepic(delpfp):
    """ .delpfp komutu için Telegram'daki mevcut profil resminizi silin. """
    group = delpfp.text[8:]
    if group == 'all':
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.from_id,
                             offset=0,
                             max_id=0,
                             limit=lim))
    input_photos = []
    for sep in pfplist.photos:
        input_photos.append(
            InputPhoto(id=sep.id,
                       access_hash=sep.access_hash,
                       file_reference=sep.file_reference))
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await delpfp.edit(
        f"`{Len (input_photos)} profil resmi başarıyla silindi.`")


@borg.on(admin_cmd(pattern="myusernames$"))
async def _(event):
    if event.fwd_from:
        return
    result = await bot(GetAdminedPublicChannelsRequest())
    output_str = ""
    for channel_obj in result.chats:
        output_str += f"- {channel_obj.title} @{channel_obj.username} \n"
    await event.edit(output_str)

CMD_HELP.update({
    "profile":
    "**📌Komut ➥ **.username <new_username>\
\n**Kullanım ➥ ** Telegram kullanıcı adınızı değiştirir.\
\n\n**📌Komut ➥ **.pname <firstname> veya .pname <firstname> <lastname>\
\n**Kullanım ➥ ** Telegram adınızı değiştirir. (Adı ve soyadı ilk boşluğa göre bölünecektir)\
\n\n**📌Komut ➥ **.setpfp or .ppic\
\n**Kullanım ➥ ** Telegram profil resminizi değiştirmek için bir resme .setpfp veya .ppic ile yanıt verin.\
\n\n**📌Komut ➥ **.pbio <new_bio>\
\n**Kullanım ➥ ** Telegram biyografinizi değiştirir.\
\n\n**📌Komut ➥ **.delpfp or .delpfp <number>/<all>\
\n**Kullanım ➥ ** Telegram profil resimlerinizi siler.\
\n\n**📌Komut ➥ **.myusernames\
\n**Kullanım ➥ ** Sizin tarafınızdan ayrılmış, kanallarınız veya gruplarınız tarafından oluşturulan kullanıcı adlarını gösterir.\
\n\n**📌Komut ➥ **.count\
\n**Kullanım ➥ ** Gruplarınızı, sohbetlerinizi, botlarınızı vb. Sayar..."
})
