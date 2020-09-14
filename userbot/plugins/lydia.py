# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
import asyncio
import io
from userbot.plugins.sql_helper.lydia_ai_sql import get_s, get_all_s, add_s, remove_s
from time import time
from userbot.utils import admin_cmd
from userbot import CMD_HELP

if Var.LYDIA_API_KEY:
    api_key = Var.LYDIA_API_KEY
    # Coffeehouse API'sini oluşturun
    coffeehouse_api = API(api_key)
    # Lydia örneği oluşturun
    lydia = LydiaAI(coffeehouse_api)


@borg.on(admin_cmd(pattern="(en|re|li)ai"))
async def lydia_disable_enable(event):
    if event.fwd_from:
        return
    if Var.LYDIA_API_KEY is None:
        await event.edit("Lütfen gerekli `LYDIA_API_KEY` ekleyin")
        return
    if event.reply_to_msg_id is not None:
        input_str = event.pattern_match.group(1)
        reply_msg = await event.get_reply_message()
        user_id = reply_msg.from_id
        chat_id = event.chat_id
        await event.edit("İşleniyor...")
        if input_str == "tr":
            # Create a new chat session (Like a conversation)
            session = lydia.create_session()
            logger.info(session)
            # logger.info("Session ID: {0}".format(session.id))
            # logger.info("Session Available: {0}".format(str(session.available)))
            # logger.info("Session Language: {0}".format(str(session.language)))
            # logger.info("Session Expires: {0}".format(str(session.expires)))
            logger.info(add_s(user_id, chat_id, session.id, session.expires))
            await event.edit(f"Selam")
        elif input_str == "re":
            logger.info(remove_s(user_id, chat_id))
            await event.edit(f"[__Kayıp sinyal__](tg://user?id={user_id})")
        elif input_str == "li":
            lsts = get_all_s()
            if len(lsts) > 0:
                output_str = "AI etkin kullanıcılar:\n\n"
                for lydia_ai in lsts:
                    output_str += f"[User](tg://user?id={lydia_ai.user_id}) konuşmada `{lydia_ai.chat_id}`\n"
            else:
                output_str = "Lydia AI etkin kullanıcı / sohbet yok. Herhangi bir sohbette herhangi bir kullanıcıya `.enai` yazarak başlayın!"
            if len(output_str) > Config.MAX_MESSAGE_SIZE_LIMIT:
                with io.BytesIO(str.encode(output_str)) as out_file:
                    out_file.name = "lydia_ai.text"
                    await event.client.send_file(
                        event.chat_id,
                        out_file,
                        force_document=True,
                        allow_cache=False,
                        caption="Lydia AI özellikli kullanıcılar",
                        reply_to=event
                    )
            else:
                await event.edit(output_str)
        else:
            await event.edit("Lydia Otomatik Sohbetinden Eklemek / Silmek için Kullanıcı Mesajını Yanıtlayın.")
    else:
        await event.edit("Lydia Otomatik Sohbetinden Eklemek / Silmek İçin Bir Kullanıcının Mesajını Yanıtlayın.")


@borg.on(admin_cmd(incoming=True))
async def on_new_message(event):
    if event.chat_id in Config.UB_BLACK_LIST_CHAT:
        return
    if Var.LYDIA_API_KEY is None:
        return
    reply = await event.get_reply_message()
    if reply is None:
        pass
    elif reply.from_id == borg.uid:
        pass
    else:
        return
    if not event.media:
        user_id = event.from_id
        chat_id = event.chat_id
        s = get_s(user_id, chat_id)
        if s is not None:
            session_id = s.session_id
            session_expires = s.session_expires
            query = event.text
            # Oturumun süresinin dolup dolmadığını kontrol edin
            # Bu yöntem bu noktada bir istisna atarsa,
            # API, Kimlik Doğrulama veya Sunucu ile ilgili bir sorun var.
            if session_expires < time():
                # re-generate session
                session = lydia.create_session()
                logger.info(session)
                session_id = session.id
                session_expires = session.expires
                logger.info(
                    add_s(
                        user_id,
                        chat_id,
                        session_id,
                        session_expires))
            # Bir düşünce düşünmeye çalışın.
            try:
                async with event.client.action(event.chat_id, "location"):
                    await asyncio.sleep(5)
                    output = lydia.think_thought(session_id, query)
                    await event.reply("💫" + output)
            except cf.exception.CoffeeHouseError as e:
                logger.info(str(e))


CMD_HELP.update({
    "lydia":
    "`.enai` kullanıcıya yanıt verin\
    \n**Kullanım ➥** Botunuz, siz `.remcf` ile durdurana kadar etiketlenen kullanıcıya otomatik olarak cevap verecektir.\
    \n\n**Kullanım ➥**`.reai` lydia'yı devre dışı bırakmak istediğiniz kişiye cevap verin\
    \n\n**Kullanım ➥**`.liai`, ai'yi (lydia) etkinleştirdiğiniz kullanıcıları listelemek için\
    \n\n**NOTE➥**bu eklentiyi çalıştırmak için heroku var\
    \n**NOTE➥** anahtar `LYDIA_API_KEY` ve `https: // coffeehouse.intellivoid.net / `adresinden değişken alın\
"
})
