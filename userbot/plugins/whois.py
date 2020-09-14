# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

""" Userbot module for getiing info about any user on Telegram(including you!). """

import os
import html
from telethon.utils import get_input_location
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from telethon.tl.types import MessageEntityMentionName
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from ..utils import admin_cmd, sudo_cmd, edit_or_reply


@borg.on(admin_cmd(pattern="userinfo(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="userinfo(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await edit_or_reply(event, str(error_i_a))
        return False
    replied_user_profile_photos = await borg(GetUserPhotosRequest(
        user_id=replied_user.user.id,
        offset=42,
        max_id=0,
        limit=80
    ))
    replied_user_profile_photos_count = "NaN"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their
        # names
        first_name = first_name.replace("\u2060", "")
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "Erişebilmem için bir profil fotoğrafına ihtiyacım var ;  **this**"
        str(e)
    caption = """Bulunan bilgiler:
🔖ID: <code>{}</code>
🤵İsim: <a href='tg://user?id={}'>{}</a>
✍️Bio: {}
🌏Veri Merkezi Numarası: {}
🖼Profil fotoğrafı sayısı: {}
🔏Kısıtlı mı: {}
🌐Telegram Tarafından Doğrulanmış mı: {}
🤖Bot mu: {}
👥Ortak gruplar: {}
List Of Telegram Data Centres:
DC1 : Miami FL, USA
DC2 : Amsterdam, NL
DC3 : Miami FL, USA
DC4 : Amsterdam, NL
DC5 : Singapore, SG
""".format(
        user_id,
        user_id,
        first_name,
        user_bio,
        dc_id,
        replied_user_profile_photos_count,
        replied_user.user.restricted,
        replied_user.user.verified,
        replied_user.user.bot,
        common_chats
    )
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
    await borg.send_message(
        event.chat_id,
        caption,
        reply_to=message_id_to_reply,
        parse_mode="HTML",
        file=replied_user.profile_photo,
        force_document=False,
        silent=True
    )
    await event.delete()


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
    if event.message.entities:
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


@borg.on(admin_cmd(pattern="whois(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="whois(?: |$)(.*)", allow_sudo=True))
async def who(event):
    exelon = await edit_or_reply(event,
                                 "`Mark Zuckerberg'dan bazı verileri çalarken sıkı durun!`")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    replied_user = await get_user(event)
    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        await edit_or_reply(event, "`Kullanıcının bilgileri alınamadı.`")
        return
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    try:
        await borg.send_file(event.chat_id,
                             photo,
                             caption=caption,
                             link_preview=False,
                             force_document=False,
                             reply_to=message_id_to_reply,
                             parse_mode="html")
        if not photo.startswith("http"):
            os.remove(photo)
        await exelon.delete()
    except TypeError:
        await exelon.edit(caption, parse_mode="html")


async def get_user(event):
    """ Kullanıcıyı argümandan veya cevaplanan mesajdan alın. """
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return replied_user


async def fetch_info(replied_user, event):
    """ Kullanıcı nesnesinden ayrıntıları alın. """
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(user_id=replied_user.user.id,
                             offset=42,
                             max_id=0,
                             limit=80))
    replied_user_profile_photos_count = "Kişinin profil resmi yükleme konusunda yardıma ihtiyacı var."
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "DC kimliği getirilemedi!"
        str(e)
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    photo = await event.client.download_profile_photo(user_id,
                                                      TEMP_DOWNLOAD_DIRECTORY +
                                                      str(user_id) + ".jpg",
                                                      download_big=True)
    first_name = first_name.replace("\u2060", "") if first_name else (
        "Bu kullanıcı bir isime sahip değil.")
    last_name = last_name.replace("\u2060", "") if last_name else (
        "Bu kullanıcı bir soyad'a sahip değil.")
    username = "@{}".format(username) if username else (
        "Bu Kullanıcının Kullanıcı Adı Yok")
    user_bio = "Bu Kullanıcının Hakkında yok" if not user_bio else user_bio
    caption = "<b>Druv veritabanından KULLANICI BİLGİSİ:</b>\n\n"
    caption += f"🤵Adı: {first_name}\n"
    caption += f"🤵Soyadı: {last_name}\n"
    caption += f"🤵Kullanıcı adı: {username}\n"
    caption += f"🌏Veri merkezi numarası: {dc_id}\n"
    caption += f"🖼Profil fotoğrafı sayısı: {replied_user_profile_photos_count}\n"
    caption += f"🤖Bot mu: {is_bot}\n"
    caption += f"🔏Kısıtlı mı: {restricted}\n"
    caption += f"🌐Telegram tarafından doğrulanmış mı:: {verified}\n"
    caption += f"🔖ID: <code>{user_id}</code>\n\n"
    caption += f"✍️Bio: \n<code>{user_bio}</code>\n\n"
    caption += f"👥Ortak gruplar: {common_chat}\n"
    caption += f"🔗Profilin kalıcı bağlantısı: "
    caption += f"<a href=\"tg://user?id={user_id}\">{first_name}</a>"
    return photo, caption


CMD_HELP.update({
    "whois":
    "**Plugin : **`whois`\
    \n\n**📌Komut ➥ **`.whois <kullanıcıadı>` veya birisine .whois ile yanıt verin\
    \n**Kullanım ➥ ** Bir kullanıcı hakkında bilgi alın.\
    \n\n**📌Komut ➥ **`.userinfo <username>` veya .userinfo ile birisinin metnini yanıtlayın\
    \n**Kullanım ➥ ** Bir kullanıcının bilgilerini alır."
})
