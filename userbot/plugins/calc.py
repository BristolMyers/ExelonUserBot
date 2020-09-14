# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import io
import sys
import traceback
from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply


@borg.on(admin_cmd(pattern="calc (.*)"))
async def _(car):
    cmd = car.text.split(" ", maxsplit=1)[1]
    event = await edit_or_reply(car, "Hesaplanıyor ...")
    car.message.id
    if event.reply_to_msg_id:
        car.reply_to_msg_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    san = f"print({cmd})"
    try:
        await aexec(san, event)
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
        evaluation = "Maalesef verilen denklem için sonuç bulamıyorum"
    final_output = "**DENKLEM**: `{}` \n\n **ÇÖZÜM**: \n`{}` \n".format(
        cmd, evaluation)
    await event.edit(final_output)


async def aexec(code, event):
    exec(
        f'async def __aexec(event): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](event)


CMD_HELP.update({"calc": "**PLUGİN İSMİ:** `calc`\
      \n\n**📌Komut ➥ **`.calc` denklemin :\
      \n**Kullanım ➥ ** verilen matematik denklemini bodmass kuralı ile çözer."
                 })
