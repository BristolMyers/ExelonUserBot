# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""Telegram Hesabınızda bulunan İletişim Kutularını sayın
Syntax: .stat"""
from telethon.tl.types import User, Chat, Channel
from userbot.utils import admin_cmd
import time
from telethon.events import NewMessage
from telethon.tl.custom import Dialog


@borg.on(admin_cmd(pattern='stat'))
async def stats(event: NewMessage.Event) -> None:  # pylint: disable = R0912, R0914, R0915
    """Hesapla ilgili istatistikleri alma komutu"""
    await event.edit('`İstatistikler toplanıyor, bekle adamım`')
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel):
            # participants_count = (await event.get_participants(dialog,
            # limit=0)).total
            if entity.broadcast:
                broadcast_channels += 1
                if entity.creator or entity.admin_rights:
                    admin_in_broadcast_channels += 1
                if entity.creator:
                    creator_in_channels += 1
            elif entity.megagroup:
                groups += 1
                # if participants_count > largest_group_member_count:
                #     largest_group_member_count = participants_count
                if entity.creator or entity.admin_rights:
                    # if participants_count > largest_group_with_admin:
                    #     largest_group_with_admin = participants_count
                    admin_in_groups += 1
                if entity.creator:
                    creator_in_groups += 1
        elif isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        elif isinstance(entity, Chat):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    full_name = inline_mention(await event.client.get_me())
    response = f'📌 **İçin istatistikler {full_name}** \n\n'
    response += f'**Özel Sohbetler:** {private_chats} \n'
    response += f'   ★ `Kullanıcılar: {private_chats - bots}` \n'
    response += f'   ★ `Botlar: {bots}` \n'
    response += f'**Gruplar:** {groups} \n'
    response += f'**Kanallar:** {broadcast_channels} \n'
    response += f'**Yönetici olduğu Gruplar:** {admin_in_groups} \n'
    response += f'   ★ `Kurucu: {creator_in_groups}` \n'
    response += f'   ★ `Yönetici Hakları: {admin_in_groups - creator_in_groups}` \n'
    response += f'**Yönetici olduğu Kanallar:** {admin_in_broadcast_channels} \n'
    response += f'   ★ `Kurucu: {creator_in_channels}` \n'
    response += f'   ★ `Yönetici hakları: {admin_in_broadcast_channels - creator_in_channels}` \n'
    response += f'**Okunmamış:** {unread} \n'
    response += f'**Okunmamış etiketler:** {unread_mentions} \n\n'
    response += f'📌 __Exelon Hesaplama Süresi:__ {stop_time:.02f}s \n'
    await event.edit(response)


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = ' '.join(names)
    return full_name
