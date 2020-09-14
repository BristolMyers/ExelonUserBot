# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import html
import userbot.plugins.sql_helper.warns_sql as sql
from ..utils import admin_cmd, sudo_cmd, edit_or_reply


@borg.on(admin_cmd(pattern="warn (.*)"))
@borg.on(sudo_cmd(pattern="warn (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    warn_reason = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(
        reply_message.from_id, event.chat_id, warn_reason)
    if num_warns >= limit:
        sql.reset_warns(reply_message.from_id, event.chat_id)
        if soft_warn:
            logger.info("Yapılacaklar: Kullanıcıyı at")
            reply = "{} dikkat, <u><a href='tg://user?id={}'>user</a></u> atıldı!".format(
                limit, reply_message.from_id)
        else:
            logger.info("Yapılacaklar: Kullanıcıyı yasakla")
            reply = "{} dikkat, <u><a href='tg://user?id={}'>user</a></u> yasaklandı!".format(
                limit, reply_message.from_id)
    else:
        reply = "<u><a href='tg://user?id={}'>user</a></u> has {}/{} uyarılar... dikkat et!".format(
            reply_message.from_id, num_warns, limit)
        if warn_reason:
            reply += "\nSon uyarı ve sebebi:\n{}".format(
                html.escape(warn_reason))
    await edit_or_reply(event, reply, parse_mode="html")


@borg.on(admin_cmd(pattern="get_warns$"))
@borg.on(sudo_cmd(pattern="get_warns$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    result = sql.get_warns(reply_message.from_id, event.chat_id)
    if result and result[0] != 0:
        num_warns, reasons = result
        limit, soft_warn = sql.get_warn_setting(event.chat_id)
        if reasons:
            text = "Bu kullanıcı, {}/{} uyarılarına sahip. Şu sebepten dolayı:".format(
                num_warns, limit)
            text += "\r\n"
            text += reasons
            await event.edit(text)
        else:
            await edit_or_reply(event, "Bu kullanıcının uyarıları var, {} / {} ancak hiçbirinin sebebi yok!".format(num_warns, limit))
    else:
        await edit_or_reply(event, "Bu kullanıcının herhangi bir uyarısı yok!")


@borg.on(admin_cmd(pattern="reset_warns$"))
@borg.on(sudo_cmd(pattern="reset_warns$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    sql.reset_warns(reply_message.from_id, event.chat_id)
    await edit_or_reply(event, "Warnings have been reset!")
