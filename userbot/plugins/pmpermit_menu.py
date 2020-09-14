# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""
Pmpermit için sohbet kutusunu destekleyin.
Başlatma / tetikleme ile gelen mesajlar tarafından kullanılır
Zaten onaylanmış kişiler için çalışmayacak.
"""
import asyncio
import userbot.plugins.sql_helper.pmpermit_sql as pmpermit_sql
from telethon import functions
from userbot import ALIVE_NAME

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "exelon"
PREV_REPLY_MESSAGE = {}


@command(pattern=r"\/start", incoming=True)
async def _(event):
    chat_id = event.from_id
    event.sender_id
    if not pmpermit_sql.is_approved(chat_id):
        chat = await event.get_chat()
        if event.fwd_from:
            return
        if not event.is_private:
            return
        PM = (
            "`Merhaba. ustamın mevcut menüsüne erişiyorsunuz,`"
            f"{DEFAULTUSER}.\n"
            "__Hadi bunu düzeltelim ve neden burada olduğunu bilmeme izin ver.__\n"
            "**Burada olmanızın aşağıdaki nedenlerinden birini seçin:**\n\n"
            "`a`. Ustamla sohbet etmek\n"
            "`b`. Efendimin gelen kutusuna spam göndermek için.\n"
            "`c`. Bir şey sormak\n"
            "`d`. Bir şey istemek\n")
        ONE = (
            "__Tamam. Talebiniz kaydedildi. Ustamın gelen kutusunu spam yapmayın. 24 ışıkyılı içinde bir yanıt bekleyebilirsiniz. Muhtemelen senin aksine meşgul biri.__\n\n"
            "**⚠️ Ustama spam gönderirseniz engellenecek ve rapor edileceksiniz. ⚠️**\n\n"
            "__Kullanım__ `/start` __Ana menüye dönmek için__")
        TWO = (" `███████▄▄███████████▄  \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓███░░░░░░░░░░░░█\n██████▀▀▀█░░░░██████▀  \n░░░░░░░░░█░░░░█  \n░░░░░░░░░░█░░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░░▀▀ `\n\n**Hiç hoş değil, burası senin evin değil. Git başka birini rahatsız et. Bir sonraki duyuruya kadar engellendiniz ve rapor edildiniz.**")
        FOUR = ("__Tamam. Ustam henüz mesajınızı görmedi, geri kalmış olanlar hakkında kafayı taksa da, genellikle insanlara cevap verir.__\n __İsterse geri döndüğünde cevap verecektir. Zaten bekleyen çok sayıda mesaj var😶__\n **Engellenmek ve rapor edilmek istemediğiniz sürece lütfen spam yapmayın.**")
        FIVE = ("`Tamam. lütfen ustamı fazla rahatsız etmemek için temel davranışları gösterin. Size yardım etmek isterse, yakında size cevap verecektir.`\n**Tekrar tekrar sormayın, aksi takdirde engellenirsiniz ve rapor edilirsiniz.**")
        LWARN = ("**Bu son uyarınız. Başka bir mesaj GÖNDERMEYİN, aksi takdirde engellenir ve rapor edilirsiniz. Sabırlı ol. Ustam size en kısa sürede cevap verecektir.**\n__Kullanım__ `/start` __Ana menüye dönmek için__")

        async with borg.conversation(chat) as conv:
            if pmpermit_sql.is_approved(chat_id):
                return
            await borg.send_message(chat, PM)
            chat_id = event.from_id
            response = await conv.get_response(chat)
            y = response.text
            if y == "a":
                if pmpermit_sql.is_approved(chat_id):
                    return
                await borg.send_message(chat, ONE)
                response = await conv.get_response(chat)
                await event.delete()
                if not response.text == "/start":
                    await response.delete()
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await borg.send_message(chat, LWARN)
                    response = await conv.get_response(chat)
                    await event.delete()
                    await response.delete()
                    response = await conv.get_response(chat)
                    if not response.text == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await borg.send_message(chat, TWO)
                        await asyncio.sleep(3)
                        await event.client(functions.contacts.BlockRequest(chat_id))
            elif y == "b":
                if pmpermit_sql.is_approved(chat_id):
                    return
                await borg.send_message(chat, LWARN)
                response = await conv.get_response(chat)
                if not response.text == "/start":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await borg.send_message(chat, TWO)
                    await asyncio.sleep(3)
                    await event.client(functions.contacts.BlockRequest(chat_id))
            elif y == "c":
                if pmpermit_sql.is_approved(chat_id):
                    return
                await borg.send_message(chat, FOUR)
                response = await conv.get_response(chat)
                await event.delete()
                await response.delete()
                if not response.text == "/start":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await borg.send_message(chat, LWARN)
                    await event.delete()
                    response = await conv.get_response(chat)
                    if not response.text == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await borg.send_message(chat, TWO)
                        await asyncio.sleep(3)
                        await event.client(functions.contacts.BlockRequest(chat_id))
            elif y == "d":
                if pmpermit_sql.is_approved(chat_id):
                    return
                await borg.send_message(chat, FIVE)
                response = await conv.get_response(chat)
                if not response.text == "/start":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await borg.send_message(chat, LWARN)
                    response = await conv.get_response(chat)
                    if not response.text == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await borg.send_message(chat, TWO)
                        await asyncio.sleep(3)
                        await event.client(functions.contacts.BlockRequest(chat_id))
            else:
                if pmpermit_sql.is_approved(chat_id):
                    return
                await borg.send_message(chat, "`Geçersiz bir komut girdiniz. Engellenmek ve rapor edilmek istemiyorsanız, lütfen yeniden gönderin / başlayın veya başka bir mesaj göndermeyin.`")
                response = await conv.get_response(chat)
                z = response.text
                if not z == "/start":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await borg.send_message(chat, LWARN)
                    await conv.get_response(chat)
                    if not response.text == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await borg.send_message(chat, TWO)
                        await asyncio.sleep(3)
                        await event.client(functions.contacts.BlockRequest(chat_id))
