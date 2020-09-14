# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

""" @ukinti_bot
Available Commands:
.unbanall
.kick option
Available Options: d, y, m, w, o, q, r """
from telethon.tl.types import UserStatusEmpty, UserStatusLastMonth, UserStatusLastWeek, UserStatusOffline, UserStatusOnline, UserStatusRecently, ChannelParticipantsKicked, ChatBannedRights
from telethon.tl import functions
from time import sleep
import asyncio
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="unbanall ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        logger.info("TODO: Henüz Uygulanmadı")
    else:
        if event.is_private:
            return False
        await event.edit("Katılımcı Listeleri Aranıyor.")
        p = 0
        async for i in borg.iter_participants(event.chat_id, filter=ChannelParticipantsKicked, aggressive=True):
            rights = ChatBannedRights(
                until_date=0,
                view_messages=False
            )
            try:
                await borg(functions.channels.EditBannedRequest(event.chat_id, i, rights))
            except FloodWaitError as ex:
                logger.warn("{} saniye uyuyor".format(ex.seconds))
                sleep(ex.seconds)
            except Exception as ex:
                await event.edit(str(ex))
            else:
                p += 1
        await event.edit("{}: {} yasaklanmadı".format(event.chat_id, p))


@borg.on(admin_cmd(pattern="ikuck ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return False
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not (chat.admin_rights or chat.creator):
            await event.edit("`Yönetici değilsiniz!`")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    await event.edit("Katılımcı Listeleri Aranıyor.")
    async for i in borg.iter_participants(event.chat_id):
        p = p + 1
        #
        # "Ters" olduğuna dikkat edin. İzinleri ``True`` olarak ayarlamalısınız
        # KALDIRMAK ve SAKLAMAK istediklerinizi ``Yok`` olarak bırakmak
        # istiyorsanız.
        rights = ChatBannedRights(
            until_date=None,
            view_messages=True
        )
        if isinstance(i.status, UserStatusEmpty):
            y = y + 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("Bu işlemi gerçekleştirmek için yönetici ayrıcalıklarına ihtiyacım var!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusLastMonth):
            m = m + 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("Bu işlemi gerçekleştirmek için yönetici ayrıcalıklarına ihtiyacım var!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusLastWeek):
            w = w + 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("Bu işlemi gerçekleştirmek için yönetici ayrıcalıklarına ihtiyacım var!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusOffline):
            o = o + 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("Bu işlemi gerçekleştirmek için yönetici ayrıcalıklarına ihtiyacım var!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusOnline):
            q = q + 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("Bu işlemi gerçekleştirmek için yönetici ayrıcalıklarına ihtiyacım var!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusRecently):
            r = r + 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("Bu işlemi gerçekleştirmek için yönetici ayrıcalıklarına ihtiyacım var!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if i.bot:
            b = b + 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("Bu işlemi gerçekleştirmek için yönetici ayrıcalıklarına ihtiyacım var!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        elif i.deleted:
            d = d + 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit("Bu işlemi gerçekleştirmek için yönetici ayrıcalıklarına ihtiyacım var!")
                    e.append(str(e))
                else:
                    c = c + 1
        elif i.status is None:
            n = n + 1
    if input_str:
        required_string = """Kicked {} / {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}"""
        await event.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await asyncio.sleep(5)
    await event.edit("""Total: {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}""".format(p, d, y, m, w, o, q, r, b, n))


async def ban_user(chat_id, i, rights):
    try:
        await borg(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)
