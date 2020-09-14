# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import html
from ..utils import admin_cmd
from telethon.tl import functions
from telethon.tl.types import MessageEntityMentionName
from telethon.tl.functions.users import GetFullUserRequest
from .. import CMD_HELP, AUTONAME, DEFAULT_BIO, ALIVE_NAME

DEFAULTUSER = str(AUTONAME) if AUTONAME else str(ALIVE_NAME)
DEFAULTUSERBIO = str(
    DEFAULT_BIO) if DEFAULT_BIO else "sıɥʇ ǝpoɔǝp uǝɥʇ llıʇu∩ ˙ ǝɔɐds ǝʇɐʌıɹd ǝɯos ǝɯ ǝʌı⅁˙"
if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID


@borg.on(admin_cmd(pattern="clone ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    user_id = replied_user.user.id
    profile_pic = await event.client.download_profile_photo(user_id, Config.TMP_DOWNLOAD_DIRECTORY)
    # bazı kişilerin adlarında tuhaf HTML var
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # bazı Silinmiş Hesapların ilk_adı yoktur
    if first_name is not None:
        # bazı garip insanların (benim gibi) 4096'dan fazla karakteri vardır.
        # names
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    # last_name is not Manadatory in @Telegram
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await borg(functions.account.UpdateProfileRequest(
        first_name=first_name
    ))
    await borg(functions.account.UpdateProfileRequest(
        last_name=last_name
    ))
    await borg(functions.account.UpdateProfileRequest(
        about=user_bio
    ))
    pfile = await borg.upload_file(profile_pic)  # pylint:disable=E060
    await borg(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
        pfile
    ))
    await event.delete()
    await borg.send_message(
        event.chat_id,
        "**HA HA HA SENİ KLONLADIM**",
        reply_to=reply_message
    )
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, f"#CLONED\nSuccesfulley cloned [{first_name}](tg://user?id={user_id })")


@borg.on(admin_cmd(pattern="revert$"))
async def _(event):
    if event.fwd_from:
        return
    name = f"{DEFAULTUSER}"
    bio = f"{DEFAULTUSERBIO}"
    n = 1
    await borg(functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit=n)))
    await borg(functions.account.UpdateProfileRequest(about=bio))
    await borg(functions.account.UpdateProfileRequest(first_name=name))
    await event.edit("başarıyla hesabınıza geri döndürüldü")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, f"#REVERT\nProfilinize başarıyla geri döndü")


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        replied_user = await event.client(
            GetFullUserRequest(
                previous_message.from_id
            )
        )
        return replied_user, None
    input_str = None
    try:
        input_str = event.pattern_match.group(1)
    except IndexError as e:
        return None, e
    if event.message.entities is not None:
        mention_entity = event.message.entities
        probable_user_mention_entity = mention_entity[0]
        if isinstance(probable_user_mention_entity, MessageEntityMentionName):
            user_id = probable_user_mention_entity.user_id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        try:
            user_object = await event.client.get_entity(input_str)
            user_id = user_object.id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        except Exception as e:
            return None, e
    if event.is_private:
        try:
            user_id = event.chat_id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        except Exception as e:
            return None, e
    try:
        user_object = await event.client.get_entity(int(input_str))
        user_id = user_object.id
        replied_user = await event.client(GetFullUserRequest(user_id))
        return replied_user, None
    except Exception as e:
        return None, e


CMD_HELP.update({"clone": "**PLUGİN İSMİ:** `clone`\
      \n\n**📌Komut ➥ **`.clone` <klonlamak istediğiniz kullanıcıyı yanıtlayın> :\
      \n**Kullanım ➥ **Karşıdaki kullanıcının hesabını klonlar.\
      \n\n**📌Komut ➥ **`.revert` :\
      \n**Kullanım ➥ ** AUTONAME, DEFAULT_BIO için heroku'da ayarladığınız profilinize geri döner."
                 })
