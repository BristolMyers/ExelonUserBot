# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""Desteklenmeyen istemcilerle ilgili Anket Bilgilerini alın
Syntax: .get_poll"""
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="get_poll"))
async def _(event):
    reply_message = await event.get_reply_message()
    if reply_message.media is None:
        await event.edit("Soruları ve yanıtları görüntülemek için lütfen bir media_type == @gPoll'a yanıt verin")
    elif reply_message.media.poll is None:
        await event.edit("Soruları ve yanıtları görüntülemek için lütfen bir media_type == @gPoll'a yanıt verin")
    else:
        media = reply_message.media
        poll = media.poll
        closed_status = poll.closed
        answers = poll.answers
        question = poll.question
        edit_caption = """Anket Kapandı: {}
Soru: {}
Yanıtlar: \n""".format(closed_status, question)
        if closed_status:
            results = media.results
            i = 0
            for result in results.results:
                edit_caption += "{}> {}    {}\n".format(
                    result.option, answers[i].text, result.voters)
                i += 1
            edit_caption += "Tüm seçmenler: {}".format(results.total_voters)
        else:
            for answer in answers:
                edit_caption += "{}> {}\n".format(answer.option, answer.text)
        await event.edit(edit_caption)
