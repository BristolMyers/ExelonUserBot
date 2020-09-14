# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

"""
Bir grubu yönetmenize yardımcı olacak Userbot modülü
"""
import asyncio
from asyncio import sleep
from datetime import datetime

from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)

from userbot import CMD_HELP
from userbot.plugins.sql_helper.mute_sql import is_muted, mute, unmute
from userbot.uniborgConfig import Config
from userbot.utils import admin_cmd, errors_handler, sudo_cmd

if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
# =================== CONSTANT ===================
PP_TOO_SMOL = "`Görüntü çok küçük`"
PP_ERROR = "`Görüntü işleme sırasında hata oluştu`"
NO_ADMIN = "`Yönetici değilim!`"
NO_PERM = "`Yeterli iznim yok!`"
NO_SQL = "`SQL dışı modda çalışıyor!`"

CHAT_PP_CHANGED = "`Grup resmi değiştirildi`"
CHAT_PP_ERROR = "`Resmi güncellerken bazı sorunlar oluştu.`" \
                "`Belki de bir yönetici değilim`" \
                "`ya da yeterli haklara sahip değilim.`"
INVALID_MEDIA = "`Geçersiz uzantı`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@borg.on(admin_cmd("setgpic$"))
@errors_handler
async def set_group_photo(gpic):
    """ .setgpic komutu ile grubunuzun fotoğrafını değiştirebilirsiniz """
    if not gpic.is_group:
        await gpic.edit("`Bunun bir grup olduğunu sanmıyorum.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None
    if not admin and not creator:
        await gpic.edit(NO_ADMIN)
        return
    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)
    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await
                                 gpic.client.upload_file(photo)))
            await gpic.edit(CHAT_PP_CHANGED)
        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)
    if BOTLOG:
        await gpic.client.send_message(
            BOTLOG_CHATID, "#GROUPPIC\n"
            f"Group profile pic changed "
            f"CHAT: {gpic.chat.title}(`{gpic.chat_id}`)")


@borg.on(admin_cmd("promote(?: |$)(.*)"))
@errors_handler
async def promote(promt):
    """ .promote komutu ile belirlenen kişiyi yönetici yapar """
    # Hedef sohbeti almak
    chat = await promt.get_chat()
    # Yetkiyi sorgula
    admin = chat.admin_rights
    creator = chat.creator
    # Yönetici değilse geri dön
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return
    new_rights = ChatAdminRights(add_admins=False,
                                 invite_users=True,
                                 change_info=False,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True)
    await promt.edit("`Yetkilendiriliyor...`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "Yönetici"  # Just in case.
    if user:
        pass
    else:
        return
    # Geçerli kullanıcı yönetici veya sahip ise tanıtmaya çalışalım
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("`Başarıyla yetkilendirildi!`")
    # Telethon BadRequestError hatası verirse
    # yönetici yapma yetkimiz yoktur
    except BadRequestError:
        await promt.edit(NO_PERM)
        return
    # Yetkilendirme işi başarılı olursa günlüğe belirtelim
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID, "#YETKİ\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {promt.chat.title}(`{promt.chat_id}`)")


@borg.on(admin_cmd("demote(?: |$)(.*)"))
@errors_handler
async def demote(dmod):
    """ .demote komutu belirlenen kişiyi yöneticilikten çıkarır  """
    # Yetki kontrolü
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return
    # Eğer başarılı olursa, yetki düşürüleceğini beyan edelim
    await dmod.edit("`Yetki düşürülüyor...`")
    rank = "admeme"  # dummy rank, lol.
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return
    # Yetki düşürme sonrası yeni izinler
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
    # Yönetici iznini düzenle
    try:
        await dmod.client(
            EditAdminRequest(dmod.chat_id, user.id, newrights, rank))
    # Telethon BadRequestError hatası verirse
    # gerekli yetkimiz yoktur
    except BadRequestError:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit("`Yetki başarıyla düşürüldü!`")
    # Yetki düşürme işi başarılı olursa günlüğe belirtelim
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID, "#YETKIDUSURME\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)")


@borg.on(admin_cmd("ban(?: |$)(.*)"))
@errors_handler
async def ban(bon):
    """ .ban komutu belirlenen kişiyi gruptan yasaklar """
    # Yetki kontrolü
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # Well
    if not admin and not creator:
        await bon.edit(NO_ADMIN)
        return
    user, reason = await get_user_from_event(bon)
    if user:
        pass
    else:
        return
    # Announce that we're going to whack the pest
    await bon.edit("`Başarıyla Yasaklandı!`")
    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id,
                                           BANNED_RIGHTS))
    except BadRequestError:
        await bon.edit(NO_PERM)
        return
    # Grubun spam gönderenlere daha kolay katılmasını yasaklamaya yardımcı olur
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await bon.edit(
            "`Mesaj atma hakkım yok! Ama yine de kullanıcı yasaklandı!`")
        return
    # Mesajı silin ve ardından komutun
    # incelikle yapıldığını söyleyin
    # Kimliğe seslenin ki fedadmins daha sonra fban edebilsin
    if reason:
        await bon.edit(f"`{str(user.id)}` yasaklandı !!\nNedeni: {reason}")
    else:
        await bon.edit(f"`{str(user.id)}` yasaklandı !!")
    # Yasaklama işlemini günlüğe belirtelim
    # başarıyla!
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID, "#BAN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {bon.chat.title}(`{bon.chat_id}`)")


@borg.on(admin_cmd("unban(?: |$)(.*)"))
@errors_handler
async def nothanos(unbon):
    """ .unban komutu belirlenen kişinin yasağını kaldırır """
    # Yetki kontrolü
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # Well
    if not admin and not creator:
        await unbon.edit(NO_ADMIN)
        return
    # Her şey yolunda giderse...
    await unbon.edit("`Yasak kaldırılıyor...`")
    user = await get_user_from_event(unbon)
    user = user[0]
    if user:
        pass
    else:
        return
    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit("```Yasaklama başarıyla kaldırıldı.```")
        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID, "#UNBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {unbon.chat.title}(`{unbon.chat_id}`)")
    except UserIdInvalidError:
        await unbon.edit("`Sanırım bu kişi yasaklama mantığım ile uyuşmuyor!`")


@command(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        await event.delete()


@borg.on(admin_cmd(r"mute ?(\d+)?"))
async def startmute(event):
    private = False
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("Beklenmeyen sorunlar veya çirkin hatalar meydana gelebilir!")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await event.edit("Lütfen bir kullanıcıyı yanıtlayın veya sesini kapatmak için komuta kullanıcı kimliğini ekleyin.")
    chat_id = event.chat_id
    replied_user = await event.client(GetFullUserRequest(userid))
    chat = await event.get_chat()
    if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
        if chat.admin_rights.delete_messages is True:
            pass
        else:
            return await event.edit("`Mesajları silme izniniz yoksa bir kişinin sesini kapatamazsınız. ಥ﹏ಥ`")
    elif "creator" in vars(chat):
        pass
    elif private:
        pass
    else:
        return await event.edit("`Yönetici hakları olmadan bir kişiyi sessize alamazsınız niqq.` ಥ﹏ಥ  ")
    if is_muted(userid, chat_id):
        return await event.edit("Bu kullanıcı bu sohbette zaten sessize alındı ​​~~ lmfao sed rip~~")
    try:
        mute(userid, chat_id)
    except Exception as e:
        await event.edit("Hata oluştu!\nHata " + str(e))
    else:
        await event.edit("Bu kişinin sesi başarıyla kapatıldı.\n**｀-´)⊃━☆ﾟ.*･｡ﾟ **")
    # Günlük grubuna duyur
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#MUTE\n"
            f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")


@borg.on(admin_cmd(r"unmute ?(\d+)?"))
async def endmute(event):
    private = False
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("Beklenmeyen sorunlar veya çirkin hatalar meydana gelebilir!")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await event.edit("Lütfen bir kullanıcıyı yanıtlayın veya sesini açmak için komuta kullanıcı kimliğini ekleyin.")
    replied_user = await event.client(GetFullUserRequest(userid))
    chat_id = event.chat_id
    if not is_muted(userid, chat_id):
        return await event.edit("__Bu kullanıcı bu sohbette yok sayılmamış__\n（ ^_^）o自自o（^_^ ）")
    try:
        unmute(userid, chat_id)
    except Exception as e:
        await event.edit("Hata Oluştu!\nHata " + str(e))
    else:
        await event.edit("Bu kişinin sesini başarıyla açtı\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍")
    # Günlük grubuna duyur
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#UNMUTE\n"
            f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")


@borg.on(admin_cmd("pin($| (.*))"))
@errors_handler
async def pin(msg):
    """ .pin komutu verildiği grupta ki yazıyı & medyayı sabitler """
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return
    to_pin = msg.reply_to_msg_id
    if not to_pin:
        await msg.edit("`Sabitlemek için herhangi bir mesaja yanıt verin.`")
        return
    options = msg.pattern_match.group(1)
    is_silent = True
    if options.lower() == "loud":
        is_silent = False
    try:
        await msg.client(
            UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await msg.edit(NO_PERM)
        return
    await msg.edit("`Başarıyla sabitlendi!`")
    user = await get_user_from_id(msg.from_id, msg)
    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID, "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}")


@borg.on(admin_cmd("kick(?: |$)(.*)"))
@errors_handler
async def kick(usr):
    """ .kick komutu belirlenen kişiyi gruptan çıkartır """
    # Yetki kontrolü
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # Yönetici değil ise geri dön
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return
    user, reason = await get_user_from_event(usr)
    if not user:
        await usr.edit("`Kullanıcı bulunamadı.`")
        return
    await usr.edit("`Çıkartılıyor...`")
    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(.5)
    except Exception as e:
        await usr.edit(NO_PERM + f"\n{str(e)}")
        return
    if reason:
        await usr.edit(f"[{user.first_name}](tg://user?id={user.id}) `gruptan atıldı !`\nNedeni: {reason}")
    else:
        await usr.edit(f"[{user.first_name}](tg://user?id={user.id}) `gruptan atıldı !`")
    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID, "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n")


@borg.on(admin_cmd("iundlt$"))
async def _(event):
    if event.fwd_from:
        return
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await borg.get_admin_log(event.chat_id, limit=5, edit=False, delete=True)
        # print(a[0].old.message)
        deleted_msg = "**Bu gruptaki silinen son 5 mesaj:**"
        for i in a:
            deleted_msg += "\n👉`{}`".format(i.old.message)
        await event.edit(deleted_msg)
    else:
        await event.edit("`Bu komutu yapmak için yönetici izinlerine ihtiyacınız var`")
        await asyncio.sleep(3)
        await event.delete()


@borg.on(sudo_cmd(pattern="(ban|unban)($| (.*))", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "ban":
        rights = BANNED_RIGHTS
    elif input_cmd == "unban":
        rights = UNBAN_RIGHTS
    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
    else:
        return False
    try:
        await borg(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await event.reply(str(exc))
    else:
        await event.reply(f"{input_cmd}ned Successfully!")


@borg.on(sudo_cmd(pattern="pgs($| (.*))", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        i = 1
        msgs = []
        from_user = None
        input_str = event.pattern_match.group(1)
        if input_str:
            from_user = await borg.get_entity(input_str)
        async for message in borg.iter_messages(
            event.chat_id,
            min_id=event.reply_to_msg_id,
            from_user=from_user
        ):
            i = i + 1
            msgs.append(message)
            if len(msgs) == 100:
                await borg.delete_messages(event.chat_id, msgs, revoke=True)
                msgs = []
        if len(msgs) <= 100:
            await borg.delete_messages(event.chat_id, msgs, revoke=True)
            msgs = []
            await event.delete()
        else:
            await event.reply("**PURGE** Failed!")


@borg.on(sudo_cmd(pattern=r"mute(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def spider(spdr):
    # Admin or creator check
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await spdr.reply(NO_ADMIN)
        return
    user, reason = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return
    self_user = await spdr.client.get_me()
    if user.id == self_user.id:
        await spdr.reply(f"Maalesef kendimi sessize alamıyorum")
        return
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.reply(f"Hata! Kullanıcının sesini muhtemelen zaten kapattı.")
    try:
        await spdr.client(EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))
        # Announce that the function is done
        if reason:
            await spdr.reply(f"{user.first_name} içinde sessize alında {spdr.chat.title}\n"f"`Nedeni:`{reason}")
        else:
            await spdr.reply(f"{user.first_name} içinde sessize alında {spdr.chat.title}")
        # Announce to logging group
        if BOTLOG:
            await spdr.client.send_message(
                BOTLOG_CHATID, "#MUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {spdr.chat.title}(`{spdr.chat_id}`)")
    except UserIdInvalidError:
        return await spdr.reply("`Sanırım bu kişi sessize alma mantığım ile uyuşmuyor!`")


@borg.on(sudo_cmd(pattern=r"unmute(?: |$)(.*)", allow_sudo=True))
async def unmoot(unmot):
    """ .unmute komutu belirlenin kişinin sesini açar (yani grupta tekrardan konuşabilir)Sessizden çıkarılıyor... """
    # Admin or creator check
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await unmot.reply(NO_ADMIN)
        return
    # If admin or creator, inform the user and start unmuting
    await unmot.edit('```Sessizden çıkarılıyor...```')
    user = await get_user_from_event(unmot)
    user = user[0]
    if user:
        pass
    else:
        return
    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.reply("Hata! Kullanıcı zaten sessizden çıkarıldı.`")
    try:
        await unmot.client(EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
        await unmot.reply("Kullanıcı tekrardan konuşabilir!")
    except UserIdInvalidError:
        await unmot.reply("`Sanırım bu kişi sessizden çıkarma mantığım ile uyuşmuyor`")
        return
    if BOTLOG:
        await unmot.client.send_message(
            BOTLOG_CHATID, "#UNMUTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {unmot.chat.title}(`{unmot.chat_id}`)")


async def get_user_from_event(event):
    """ Sessize alınan kullanıcıların mesajlarını silmek için kullanılır """
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Kullanıcının kullanıcı adını, kimliğini veya yanıtını iletin!`")
            return
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            await event.edit("Bu kullanıcının bilgileri alınamadı.")
            return None
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj

CMD_HELP.update({"admin": "**PLUGİN İSMİ:** `admin`\
      \n\n**📌Komut ➥ **`.setgpic <yanıtlanan resim>` :\
      \n**Kullanım ➥ ** Grubun resmini değiştirir.\
      \n\n**📌Komut ➥ **`.promote` :\
      \n**Kullanım ➥ ** Sohbetteki kişiye yönetici hakları sağlar.\
      \n\n**📌Komut ➥ ** `.demote`\
      \n**Kullanım ➥ ** Sohbetteki kişinin yönetici izinlerini iptal eder.\
      \n\n**📌Komut ➥ **`.ban` :\
      \n**Kullanım ➥ ** Sohbetteki kişiyi gruptan yasaklar.\
      \n\n**📌Komut ➥ **`.unban` :\
      \n**Kullanım ➥ ** Sohbetteki kişinin yasağını kaldırır.\
      \n\n**📌Komut ➥ ** `.mute`\
      \n**Kullanım ➥ ** Sohbetteki kişiyi susturur, yöneticilerde de çalışır\
      \n\n**📌Komut ➥ **`.unmute` :\
      \n**Kullanım ➥ ** Kişiyi sessize alınanlar listesinden kaldırır.\
      \n\n**📌Komut ➥ ** `.pin <yanıtlanan mesaj medya>`\
      \n**Kullanım ➥ ** Grupta yanıtlanan mesajı sabitler.\
      \n\n**📌Komut ➥ **`.kick` :\
      \n**Kullanım ➥ ** komutu belirlenen kişiyi gruptan çıkartır.\
      \n\n**📌Komut ➥ **`.iundlt` :\
      \n**Kullanım ➥ ** gruptaki son 5 silinmiş mesajı görüntüler."
                 })
