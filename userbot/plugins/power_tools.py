# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""Herhangi bir sohbetten botu yeniden başlatın veya sonlandırın
Available Commands:
.restart
.shutdown"""
import os
import sys
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="restart"))
async def _(event):
    if event.fwd_from:
        return
    # await asyncio.sleep(2)
    # await event.edit("Restarting [██░] ...\n`.ping` me or `.help` to check if I am online after a lil bit.")
    # await asyncio.sleep(2)
    # await event.edit("Restarting [███]...\n`.ping` me or `.help` to check if I am online after a lil bit.")
    # await asyncio.sleep(2)
    await event.edit("Yeniden başlatıldı. `.ping` me veya `.help` çevrimiçi olup olmadığımı kontrol etmek için, aslında yeniden başlatmak 1-2 dakika sürüyor")
    await borg.disconnect()
    # https://archive.is/im3rt
    os.execl(sys.executable, sys.executable, *sys.argv)
    # You probably don't need it but whatever
    quit()


@borg.on(admin_cmd(pattern="shutdown"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Kapatılıyor ... Beni daha sonra manuel olarak aç")
    await borg.disconnect()
