# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from telethon import events
from .. import CMD_HELP
from telethon.utils import pack_bot_file_id
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from userbot.plugins.sql_helper.welcome_sql import get_current_welcome_settings, \
    add_welcome_setting, rm_welcome_setting, update_previous_welcome


@bot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        if event.user_joined:
            if cws.should_clean_welcome:
                try:
                    await bot.delete_messages(  # pylint:disable=E0602
                        event.chat_id,
                        cws.previous_welcome
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    logger.warn(str(e))  # pylint:disable=E0602

            exelon = await bot.get_me()
            my_first = exelon.first_name
            my_last = exelon.last_name
            my_fullname = f"{my_first} {my_last}"
            my_mention = "[{}](tg://user?id={})".format(my_first, exelon.id)
            my_username = f"@{exelon.username}"
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await bot.get_me()
            title = chat.title if chat.title else "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            first = a_user.first_name
            last = a_user.last_name
            if last:
                fullname = f"{first} {last}"
            else:
                fullname = first
            username = f"@{me.username}" if me.username else f"[Me](tg://user?id={me.id})"
            userid = a_user.id
            current_saved_welcome_message = cws.custom_welcome_message
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            current_message = await event.reply(
                current_saved_welcome_message.format(mention=mention, title=title, count=count, first=first, last=last, fullname=fullname, username=username, userid=userid,
                                                     my_first=my_first, my_fullname=my_fullname, my_last=my_last, my_mention=my_mention, my_username=my_username),
                file=cws.media_file_id
            )
            update_previous_welcome(event.chat_id, current_message.id)


@borg.on(admin_cmd(pattern="savewelcome ?(.*)"))
@borg.on(sudo_cmd(pattern="savewelcome", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        bot_api_file_id = pack_bot_file_id(msg.media)
        add_welcome_setting(
            event.chat_id,
            msg.message,
            True,
            0,
            bot_api_file_id)
        await edit_or_reply(event, " Hoşgeldin mesajı kaydedildi. ")
    else:
        if event.pattern_match.group(1):
            input_str = event.pattern_match.group(1)
        else:
            await edit_or_reply(event, " Karşılama mesajı olarak ne ayarlamalıyım? ")
        add_welcome_setting(event.chat_id, input_str, True, 0, None)
        await edit_or_reply(event, " Hoşgeldin mesajı kaydedildi ")


@borg.on(admin_cmd(pattern="clearwelcome$"))
@borg.on(sudo_cmd(pattern="clearwelcome$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await edit_or_reply(event, " Hoşgeldin mesajı silindi. " +
                        "En son belirlenen hoşgeldin mesajı : `{}`.".format(cws.custom_welcome_message))


@borg.on(admin_cmd(pattern="listwelcome$"))
@borg.on(sudo_cmd(pattern="listwelcome$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    if hasattr(cws, 'custom_welcome_message'):
        await edit_or_reply(event,
                            "Karşılama mesajı bulundu. " +
                            "Karşılama mesajınız:\n\n`{}`.".format(cws.custom_welcome_message))
    else:
        await edit_or_reply(event, "No Welcome Message found")

CMD_HELP.update({
    "welcome":
    "**Plugin :** `welcome`\
\n\n**📌Komut ➥ ** `.savewelcome` <karşılama mesajı> veya .setwelcome ile bir mesajı yanıtlayın\
\n**Kullanım ➥ ** Mesajı sohbette bir hoş geldiniz notu olarak kaydeder.\
\n\nKarşılama mesajlarını biçimlendirmek için mevcut değişkenler :\
\n`{mention}, {title}, {count}, {first}, {last}, {fullname}, {userid}, {username}, {my_first}, {my_fullname}, {my_last}, {my_mention}, {my_username}`\
\n\n**📌Komut ➥ ** `.listwelcome`\
\n**Kullanım ➥ **Sohbette bir karşılama notunuz olup olmadığını kontrol edin.\
\n\n**📌Komut ➥ ** `.clearwelcome`\
\n**Kullanım ➥ ** Mevcut sohbetin hoş geldiniz notunu siler.\
"
})
