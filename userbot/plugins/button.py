# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import os
import re
from .. import CMD_HELP
from telethon import Button
from ..utils import admin_cmd, sudo_cmd, edit_or_reply

# regex obtained from:
# https://github.com/PaulSonOfLars/tgbot/blob/master/tg_bot/modules/helper_funcs/string_handling.py#L23
BTN_URL_REGEX = re.compile(
    r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")


@borg.on(admin_cmd(pattern=r"cbutton(?: |$)(.*)", outgoing=True))
@borg.on(sudo_cmd(pattern="cbutton(?: |$)(.*)", allow_sudo=True))
async def _(event):
    chat = event.chat_id
    reply_message = await event.get_reply_message()
    if reply_message:
        markdown_note = reply_message.text
    else:
        markdown_note = event.pattern_match.group(1)
    prev = 0
    note_data = ""
    buttons = []
    for match in BTN_URL_REGEX.finditer(markdown_note):
        # Bt url'nin çıkıp çıkmadığını kontrol edin
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1
        # bile olsa, çıkış yapılmamışsa -> düğme oluştur
        if n_escapes % 2 == 0:
            # düğme etiketi, url ve satırsonu durumu ile bir grup oluşturun
            buttons.append(
                (match.group(2),
                 match.group(3),
                 bool(
                    match.group(4))))
            note_data += markdown_note[prev:match.start(1)]
            prev = match.end(1)
        # tuhafsa, kaçtı -> ilerle
        else:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
    else:
        note_data += markdown_note[prev:]
    message_text = note_data.strip()
    tl_ib_buttons = build_keyboard(buttons)
    tgbot_reply_message = None
    if reply_message:
        if reply_message.media:
            tgbot_reply_message = await borg.download_media(reply_message.media)
    await tgbot.send_message(
        entity=chat,
        message=message_text,
        parse_mode="html",
        file=tgbot_reply_message,
        link_preview=False,
        buttons=tl_ib_buttons,
        silent=True
    )
    await event.delete()
    if tgbot_reply_message:
        os.remove(tgbot_reply_message)

# Helpers


@borg.on(admin_cmd(pattern=r"ibutton(?: |$)(.*)", outgoing=True))
@borg.on(sudo_cmd(pattern="ibutton(?: |$)(.*)", allow_sudo=True))
async def _(event):
    reply_to_id = None
    exeloninput = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    await event.get_reply_message()
    # soon will try to add media support
    if not exeloninput:
        exeloninput = (await event.get_reply_message()).text
    if not exeloninput:
        await edit_or_reply(event, "`Bana bot satır içi yazmam için bir şeyler ver`")
        return
    exeloninput = "Inline buttons " + exeloninput
    tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
    results = await bot.inline_query(
        tgbotusername,
        exeloninput
    )
    await results[0].click(
        event.chat_id,
        reply_to=reply_to_id,
        hide_via=True
    )
    await event.delete()


def build_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb


CMD_HELP.update({"button": "**PLUGİN İSMİ:** `button`\
      \n\n**📌Komut ➥ **`.cbutton` :\
      \n**Kullanım ➥ ** butonlar [butandaki ad] <buton url: açmak istediğiniz bağlantı> biçiminde olmalıdır ve işaretleme varsayılan html'dir.\
      \n**ÖRNEK ➥ **`.cbutton test [google]<buttonurl:https://www.google.com> [ExelonUserBot]<buttonurl:https://t.me/ExelonUserBot:same> [Exelon Support]<buttonurl:https://t.me/ExelonSupport>` :\
      \n\n**📌Komut ➥ ** `.ibutton`\
      \n**Kullanım ➥ ** Butonlar [Butondaki ad] <buton url: açmak istediğiniz bağlantı biçiminde olmalıdır.\
      \n**ÖRNEK ➥ **`.ibutton test [google]<buttonurl:https://www.google.com> [ExelonUserBot]<buttonurl:https://t.me/ExelonUserBot:same> [Exelon Support]<buttonurl:https://t.me/ExelonSupport>` :\ "
                 })
