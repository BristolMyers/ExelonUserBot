# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from userbot.utils import admin_cmd
from random import choice
from urllib import parse
from os import remove
import requests
import random
from telethon import events, types, functions, utils

BASE_URL = "https://headp.at/pats/{}"
PAT_IMAGE = "pat.jpg"


def choser(cmd, pack, blacklist={}):
    docs = None

    @borg.on(events.NewMessage(pattern=rf'\.{cmd}', outgoing=True))
    async def handler(event):
        await event.delete()
        nonlocal docs
        if docs is None:
            docs = [
                utils.get_input_document(x)
                for x in (await borg(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack)))).documents
                if x.id not in blacklist
            ]
        await event.respond(file=random.choice(docs))


choser('brain', 'supermind')
choser('dab', 'DabOnHaters', {
    1653974154589768377,
    1653974154589768312,
    1653974154589767857,
    1653974154589768311,
    1653974154589767816,
    1653974154589767939,
    1653974154589767944,
    1653974154589767912,
    1653974154589767911,
    1653974154589767910,
    1653974154589767909,
    1653974154589767863,
    1653974154589767852,
    1653974154589768677
})

# HeadPat Module for Userbot (http://headp.at)
# cmd:- .pat username or reply to msg
# By:- git: jaskaranSM tg: @Zero_cool7870


@borg.on(admin_cmd(pattern="pat ?(.*)", outgoing=True))
async def lastfm(event):
    if event.fwd_from:
        return
    username = event.pattern_match.group(1)
    if not username and not event.reply_to_msg_id:
        await event.edit("`Bir mesajı yanıtlayın veya kullanıcı adı sağlayın`")
        return
    resp = requests.get("http://headp.at/js/pats.json")
    pats = resp.json()
    pat = BASE_URL.format(parse.quote(choice(pats)))
    await event.delete()
    with open(PAT_IMAGE, 'wb') as f:
        f.write(requests.get(pat).content)
    if username:
        await borg.send_file(event.chat_id, PAT_IMAGE, caption=username)
    else:
        await borg.send_file(event.chat_id, PAT_IMAGE, reply_to=event.reply_to_msg_id)
    remove(PAT_IMAGE)
