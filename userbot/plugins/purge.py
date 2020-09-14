# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
""" Gereksiz mesajları (genellikle spam veya ot) temizlemek için Userbot modülü. """

from asyncio import sleep
from telethon.errors import rpcbaseerrors
from userbot import CMD_HELP
from userbot.utils import admin_cmd, errors_handler
from userbot.uniborgConfig import Config


if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID


@borg.on(admin_cmd(outgoing=True, pattern="purge$"))
@errors_handler
async def fastpurger(purg):
    """ .purge komutu için, yanıttan başlayarak tüm mesajları temizleyin. """
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count = count + 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        await purg.edit("`Mesaj belirtilmedi.`", )
        return

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id,
        "Hızlı temizleme tamamlandı!\nPurged " + str(count) + " messages.",
    )

    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID,
            "#PURGE \n" + Str(count) + " mesajlarının temizlenmesi başarıyla tamamlandı.")
    await sleep(2)
    await done.delete()


@borg.on(admin_cmd(outgoing=True, pattern="purgeme"))
@errors_handler
async def purgeme(delme):
    """ .purgeme için, son mesajınızın x sayısını silin."""
    message = delme.text
    count = int(message[9:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id,
                                                    from_user='me'):
        if i > count + 1:
            break
        i = i + 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "`Temizleme tamamlandı!` Temizlendi" + str(sayım) + "mesajları.",
    )
    if BOTLOG:
        await delme.client.send_message(
            BOTLOG_CHATID,
            "#PURGEME \n" + Str(count) + " mesajlarının temizlenmesi başarıyla tamamlandı.")
    await sleep(2)
    i = 1
    await smsg.delete()


@borg.on(admin_cmd(outgoing=True, pattern="del$"))
@errors_handler
async def delete_it(delme):
    """ .Del komutu için, cevaplanan mesajı silin. """
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "#DEL \nMesajın silinmesi başarılı oldu")
        except rpcbaseerrors.BadRequestError:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Pekala, bir mesajı silemiyorum")


@borg.on(admin_cmd(outgoing=True, pattern="edit"))
@errors_handler
async def editer(edit):
    """ .ditme komutu için son mesajınızı düzenleyin. """
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id('me')
    string = str(message[6:])
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i = i + 1
    if BOTLOG:
        await edit.client.send_message(BOTLOG_CHATID,
                                       "#EDIT \nDüzenleme sorgusu başarıyla yürütüldü")


CMD_HELP.update({
    'purge':
    "**📌Komut ➥ **.purge\
    \n**Kullanım ➥ ** Yanıttan başlayarak tüm mesajları temizler.\
    \n\n**📌Komut ➥ **.purgeme <x>\
    \n**Kullanım ➥ ** En son mesajlarınızın x miktarını siler.\
    \n\n**📌Komut ➥ **.del\
    \n**Kullanım ➥ ** Cevapladığınız mesajı siler.\
    \n\n**📌Komut ➥ **.edit <newmessage>\
    \n**Kullanım ➥ ** Son mesajınızı <newmessage> ile değiştirin."
})
