# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""Telegram 5.0.1'de Varsayılan İzin
Kullanılabilir Komutlar: .lock <option>, .unlock <option>, .locks
API Seçenekleri: msg, media, sticker, gif, gamee, ainline, gpoll, adduser, cpin, changeinfo
DB Seçenekleri: botlar, komutlar, e-posta, yönlendirme, url"""

from telethon import events, functions, types
from userbot.plugins.sql_helper.locks_sql import update_lock, is_locked, get_locks
from userbot.utils import admin_cmd
from userbot import CMD_HELP


@borg.on(admin_cmd(pattern=r"lock( (?P<target>\S+)|$)"))
async def _(event):
    # Düzenli ifadede boşluk tuhaflığı gereklidir çünkü bağımsız değişken isteğe bağlıdır ve diğer
    # komut ".lock" ile başlar
    if event.fwd_from:
        return
    input_str = event.pattern_match.group("hedef")
    peer_id = event.chat_id
    if input_str in (("bots", "commands", "email", "forward", "url")):
        update_lock(peer_id, input_str, True)
        await event.edit(
            "Kilitli {}".format(input_str)
        )
    else:
        msg = None
        media = None
        sticker = None
        gif = None
        gamee = None
        ainline = None
        gpoll = None
        adduser = None
        cpin = None
        changeinfo = None
        if input_str:
            if "msg" in input_str:
                msg = True
            if "media" in input_str:
                media = True
            if "sticker" in input_str:
                sticker = True
            if "gif" in input_str:
                gif = True
            if "gamee" in input_str:
                gamee = True
            if "ainline" in input_str:
                ainline = True
            if "gpoll" in input_str:
                gpoll = True
            if "adduser" in input_str:
                adduser = True
            if "cpin" in input_str:
                cpin = True
            if "changeinfo" in input_str:
                changeinfo = True
        banned_rights = types.ChatBannedRights(
            until_date=None,
            # view_messages=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            send_polls=gpoll,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            result = await borg(  # pylint:disable=E0602
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=peer_id,
                    banned_rights=banned_rights
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
        else:
            await event.edit(
                "API'da Mevcut Sohbet Varsayılan İzinleri Başarıyla Değiştirildi"
            )


@borg.on(admin_cmd(pattern="unlock ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if input_str in (("bots", "commands", "email", "forward", "url")):
        update_lock(peer_id, input_str, False)
        await event.edit(
            "Kilitli değil {}".format(input_str)
        )
    else:
        await event.edit(
            "API kilitlerinin kilidini açmak için herhangi bir parametre olmadan `.lock` kullanın"
        )


@borg.on(admin_cmd(pattern="curenabledlocks"))
async def _(event):
    if event.fwd_from:
        return
    res = ""
    current_db_locks = get_locks(event.chat_id)
    if not current_db_locks:
        res = "Bu sohbette DataBase kilidi yok"
    else:
        res = "Bu sohbette DataBase kilitleri aşağıdadır: \n"
        res += "👉 `botlar`: `{}`\n".format(current_db_locks.bots)
        res += "👉 `komutlar`: `{}`\n".format(current_db_locks.commands)
        res += "👉 `email`: `{}`\n".format(current_db_locks.email)
        res += "👉 `forward`: `{}`\n".format(current_db_locks.forward)
        res += "👉 `url`: `{}`\n".format(current_db_locks.url)
    current_chat = await event.get_chat()
    try:
        current_api_locks = current_chat.default_banned_rights
    except AttributeError as e:
        logger.info(str(e))
    else:
        res += "\nBu sohbette API kilitleri aşağıdadır: \n"
        res += "👉 `msg`: `{}`\n".format(current_api_locks.send_messages)
        res += "👉 `media`: `{}`\n".format(current_api_locks.send_media)
        res += "👉 `sticker`: `{}`\n".format(current_api_locks.send_stickers)
        res += "👉 `gif`: `{}`\n".format(current_api_locks.send_gifs)
        res += "👉 `gamee`: `{}`\n".format(current_api_locks.send_games)
        res += "👉 `ainline`: `{}`\n".format(current_api_locks.send_inline)
        res += "👉 `gpoll`: `{}`\n".format(current_api_locks.send_polls)
        res += "👉 `adduser`: `{}`\n".format(current_api_locks.invite_users)
        res += "👉 `cpin`: `{}`\n".format(current_api_locks.pin_messages)
        res += "👉 `changeinfo`: `{}`\n".format(current_api_locks.change_info)
    await event.edit(res)


@borg.on(events.MessageEdited())  # pylint:disable=E0602
@borg.on(events.NewMessage())  # pylint:disable=E0602
async def check_incoming_messages(event):
    # TODO: exempt admins from locks
    peer_id = event.chat_id
    if is_locked(peer_id, "commands"):
        entities = event.message.entities
        is_command = False
        if entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityBotCommand):
                    is_command = True
        if is_command:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "Burada ADMIN iznine sahip değilim. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "commands", False)
    if is_locked(peer_id, "forward"):
        if event.fwd_from:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "Burada ADMIN iznim yok gibi görünüyor. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "forward", False)
    if is_locked(peer_id, "email"):
        entities = event.message.entities
        is_email = False
        if entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityEmail):
                    is_email = True
        if is_email:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "Burada ADMIN iznim yok gibi görünüyor. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "email", False)
    if is_locked(peer_id, "url"):
        entities = event.message.entities
        is_url = False
        if entities:
            for entity in entities:
                if isinstance(
                    entity,
                    (types.MessageEntityTextUrl,
                     types.MessageEntityUrl)):
                    is_url = True
        if is_url:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "Burada ADMIN iznim yok gibi görünüyor. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "url", False)


@borg.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    # TODO: exempt admins from locks
    # check for "lock" "bots"
    if is_locked(event.chat_id, "bots"):
        # bots are limited Telegram accounts,
        # and cannot join by themselves
        if event.user_added:
            users_added_by = event.action_message.from_id
            is_ban_able = False
            rights = types.ChatBannedRights(
                until_date=None,
                view_messages=True
            )
            added_users = event.action_message.action.users
            for user_id in added_users:
                user_obj = await borg.get_entity(user_id)
                if user_obj.bot:
                    is_ban_able = True
                    try:
                        await borg(functions.channels.EditBannedRequest(
                            event.chat_id,
                            user_obj,
                            rights
                        ))
                    except Exception as e:
                        await event.reply(
                            "Burada ADMIN iznim yok gibi görünüyor. \n`{}`".format(str(e))
                        )
                        update_lock(event.chat_id, "bots", False)
                        break
            if Config.G_BAN_LOGGER_GROUP is not None and is_ban_able:
                ban_reason_msg = await event.reply(
                    "! UYARI [kullanıcı] (tg: // user? id = {}) Lütfen bu sohbete BOT Eklemeyin.".format(users_added_by)
                )

CMD_HELP.update({
    "locks":
    "**📌Komut ➥ **.lock <all veya türler> or .unlock <all veya türler>\
\n**Kullanım ➥ ** Sohbette bazı yaygın mesaj türlerini kilitlemenizi / kilidini açmanızı sağlar.\
[NOTE➥ Sohbette uygun yönetici hakları gerektirir !!]\
\n\nKilitlenecek / kilidi açılabilecek mesaj türleri şunlardır: \
\n➥API Options: msg, media, sticker, gif, gamee, ainline, gpoll, adduser, cpin, changeinfo\
\n➥DB Options: bots, commands, email, forward, url\
\n\n**📌Komut ➥ **.curenabledlocks\
\n**Kullanım ➥ ** aktif kilitleri görmek için"
})
