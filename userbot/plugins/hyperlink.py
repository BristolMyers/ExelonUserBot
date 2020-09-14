# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="hl ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input = event.pattern_match.group(1)
    await event.edit("[ㅤㅤㅤㅤㅤㅤㅤ](" + input + ")")
