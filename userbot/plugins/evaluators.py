# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import io
import sys
import time
import asyncio
import traceback
from .. import CMD_HELP
from ..utils import admin_cmd, sudo_cmd, edit_or_reply


@borg.on(admin_cmd(pattern="bash ?(.*)"))
@borg.on(sudo_cmd(pattern="bash ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from or event.via_bot_id:
        return
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    OUTPUT = f"`{stdout.decode()}`"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "bash.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
            await event.delete()
    else:
        await edit_or_reply(event, OUTPUT)


@borg.on(admin_cmd(pattern="exec ?(.*)"))
@borg.on(sudo_cmd(pattern="exec ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from or event.via_bot_id:
        return
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "Hata yok"
    o = stdout.decode()
    if not o:
        o = "**Tip**: \n`Kodunuzun sonuçlarını görmek istiyorsanız, bunları standart çıktıya yazdırmanızı öneririm..`"
    else:
        _o = o.split("\n")
        o = "`\n".join(_o)
    OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "exec.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
            await event.delete()
    else:
        await edit_or_reply(event, OUTPUT)


@borg.on(admin_cmd(pattern="eval"))
@borg.on(sudo_cmd(pattern="eval", allow_sudo=True))
async def _(event):
    if event.fwd_from or event.via_bot_id:
        return
    cmd = event.text.split(" ", maxsplit=1)[1]
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    event = await edit_or_reply(event, "İşleme...")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(
        cmd, evaluation)
    if len(final_output) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
            await event.delete()
    else:
        await event.edit(final_output)


async def aexec(code, event):
    exec(f'async def __aexec(event): ' +
         ''.join(f'\n {l}' for l in code.split('\n'))
         )
    return await locals()['__aexec'](event)

CMD_HELP.update({
    "evaluators": "**Synatax : **.eval <expr>`:\
     \n**Usage : **Python betiğini yürütün.\
     \n\n**Synatax : **.exec <command>`:\
     \n**Usage : **ExelonUserBot sunucusunda bir bash komutu yürütün ve ayrıntıları gösterir.\
     \n\n**Synatax : **.bash <command>`:\
     \n**Usage : **ExelonUserBot sunucusunda bir bash komutu yürütün ve çıktıları kopyalamak kolaydır\
     "
})
