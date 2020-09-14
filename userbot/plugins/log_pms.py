# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
from asyncio import sleep
from userbot import CMD_HELP
from userbot.utils import admin_cmd
from telethon import events
import asyncio
from userbot.utils import admin_cmd
import asyncio
import logging
import os
import sys
from userbot.uniborgConfig import Config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARN)

NO_PM_LOG_USERS = []

BOTLOG = True
BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID


@borg.on(admin_cmd(outgoing=True, pattern=r"save(?: |$)([\s\S]*)"))
async def log(log_text):
    """ .log komutu için, bir mesajı veya komut argümanını bot günlükleri grubuna iletir """
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Chat ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("`Neyi kaydetmem gerekiyor?`")
            return
        await log_text.edit("`Başarıyla Oturum Açıldı`")
    else:
        await log_text.edit("`Bu özellik, Günlük Kaydının etkinleştirilmesini gerektirir!`")
    await sleep(2)
    await log_text.delete()


@borg.on(admin_cmd(outgoing=True, pattern="kickme$"))
async def kickme(leave):
    """ Temelde .kickme komutudur """
    await leave.edit("Hoşçakalın ben gidiyorum 💀")
    await leave.client.kick_participant(leave.chat_id, 'me')


@borg.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def monito_p_m_s(event):
    sender = await event.get_sender()
    if Config.NO_LOG_P_M_S and not sender.bot:
        chat = await event.get_chat()
        if chat.id not in NO_PM_LOG_USERS and chat.id != borg.uid:
            try:
                if Config.PM_LOGGR_BOT_API_ID:
                    if event.message:
                        e = await borg.get_entity(int(Config.PM_LOGGR_BOT_API_ID))
                        fwd_message = await borg.forward_messages(
                            e,
                            event.message,
                            silent=True
                        )
                    else:
                        return
                else:
                    return
            except Exception as e:
                # logger.warn(str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(e)


@borg.on(admin_cmd(pattern="log(?: |$)(.*)"))
async def set_no_log_p_m(event):
    if Config.PM_LOGGR_BOT_API_ID is not None:
        event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if chat.id in NO_PM_LOG_USERS:
                NO_PM_LOG_USERS.remove(chat.id)
                await event.edit("Bu sohbetten Mesaj Günlüğe Kaydedilecek")
                await asyncio.sleep(3)


@borg.on(admin_cmd(pattern="nolog(?: |$)(.*)"))
async def set_no_log_p_m(event):
    if Config.PM_LOGGR_BOT_API_ID is not None:
        event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if chat.id not in NO_PM_LOG_USERS:
                NO_PM_LOG_USERS.append(chat.id)
                await event.edit("Bu sohbetten Mesaj Günlüğe Kaydedilmeyecek")
                await asyncio.sleep(3)


CMD_HELP.update({"log_pms": "**PLUGİN İSMİ:** `log_pms`\
      \n\n**📌Komut ➥ **`.save` :\
      \n**Kullanım ➥ **etiketli mesajı özel grupta kaydeder.\
      \n\n**📌Komut ➥ **`.kickme` :\
      \n**Kullanım ➥ ** seni bunu kullandığın sohbetten atıyor.\
      \n\n**📌Komut ➥ ** `.log`\
      \n**Kullanım ➥ ** .Nolog kullanıyorsanız ve tekrar oturum açmak istiyorsanız, varsayılan olarak tüm özel sohbet mesajlarını günlüğe kaydedecektir, sonra bunu kullanmanız gerekir.\
      \n\n**📌Komut ➥ **`.nolog` :\
      \n**Kullanım ➥ ** özel bir sohbetten oturum açmayı durdurmak için."
                 })
