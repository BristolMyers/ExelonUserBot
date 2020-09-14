"""COMMAND : .cpu, .uptime, .suicide, .env, .pip, .neofetch, .coffeehouse, .date, .stdplugins, .fast, .iwantsex, .telegram, .listpip, .pyfiglet, .kowsay, .name, .faast, .daddyjoke, .fortune, .qquote, .fakeid, .vpn, .kwot, .qpro, .covid"""
# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import io
import os
import asyncio
from .. import CMD_HELP
from asyncio.subprocess import PIPE as asyncPIPE
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from asyncio import create_subprocess_exec as asyncrunapp

if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)


@borg.on(admin_cmd(outgoing=True, pattern="pips (.*)"))
@borg.on(sudo_cmd(pattern="pips (.*)", allow_sudo=True))
async def pipcheck(pip):
    pipmodule = pip.pattern_match.group(1)
    reply_to_id = pip.message.id
    if pip.reply_to_msg_id:
        reply_to_id = pip.reply_to_msg_id
    if pipmodule:
        pip = await edit_or_reply(pip, "`Aranıyor. . .`")
        pipc = await asyncrunapp(
            "pip3",
            "search",
            pipmodule,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())
        if pipout:
            if len(pipout) > 4096:
                await pip.edit("`Çıktı çok büyük, dosya olarak gönderiliyor`")
                file = open("pips.txt", "w+")
                file.write(pipout)
                file.close()
                await borg.send_file(
                    pip.chat_id,
                    "pips.txt",
                    reply_to=reply_to_id,
                    caption=pipmodule,
                )
                os.remove("output.txt")
                return
            await pip.edit("**Query: **\n`"
                           f"pip3 search {pipmodule}"
                           "`\n**Result: **\n`"
                           f"{pipout}"
                           "`")
        else:
            await pip.edit("**Sorgu: **\n`"
                           f"pip3 search {pipmodule}"
                           "`\n**Sonuç: **\n`Sonuç Dönmedi / Yanlış")


@borg.on(admin_cmd(pattern="suicide$"))
@borg.on(sudo_cmd(pattern="suicide$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "rm -rf *"
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    stdout.decode()
    OUTPUT = f"**İNTİHAR BOMBASI:**\nTüm klasörleri ve dosyaları başarıyla sildi"
    event = await edit_or_reply(event, OUTPUT)


@borg.on(admin_cmd(pattern="plugins$"))
@borg.on(sudo_cmd(pattern="plugins$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "ls userbot/plugins"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**[Exelon's](tg://need_update_for_some_feature/) PLUGINS:**\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@borg.on(admin_cmd(pattern="date$"))
@borg.on(sudo_cmd(pattern="date$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
#    dirname = event.pattern_match.group(1)
#    tempdir = "localdir"
    cmd = "date"
#    if dirname == tempdir:
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@borg.on(admin_cmd(pattern="env$"))
@borg.on(sudo_cmd(pattern="env$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
#    dirname = event.pattern_match.group(1)
#    tempdir = "localdir"
    cmd = "env"
#    if dirname == tempdir:
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**[Exelon's](tg://need_update_for_some_feature/) Ortam Modülü:**\n\n\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@borg.on(admin_cmd(pattern="fast$"))
@borg.on(sudo_cmd(pattern="fast$", allow_sudo=True))
async def _(event):
    await event.edit("calculating...")
    if event.fwd_from:
        return
#    dirname = event.pattern_match.group(1)
#    tempdir = "localdir"
    cmd = "speedtest-cli"
#    if dirname == tempdir:
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**[Exelon's](tg://need_update_for_some_feature/) , Hesaplanan Sunucu Hızı:**\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@borg.on(admin_cmd(pattern="fortune$"))
@borg.on(sudo_cmd(pattern="fortune$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "pytuneteller pisces --today"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@borg.on(admin_cmd(pattern="qquote$"))
@borg.on(sudo_cmd(pattern="qquote$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "jotquote"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@borg.on(admin_cmd(pattern="fakeid$"))
@borg.on(sudo_cmd(pattern="fakeid$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "csvfaker -r 10 first_name last_name job"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@borg.on(admin_cmd(pattern="kwot$"))
@borg.on(sudo_cmd(pattern="kwot$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "kwot"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "kwot.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@borg.on(admin_cmd(pattern="qpro$"))
@borg.on(sudo_cmd(pattern="qpro$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "programmingquotes -l EN"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)

CMD_HELP.update({
    "execmod":
    "**Plugin : **`execmod`\
    \n\n**📌Komut ➥** `.pips query`\
    \n**Kullanım ➥ **Pip modüllerinizi arar\
    \n\n**📌Komut ➥ **`.sucide`\
    \n**Kullanım ➥ **Bottaki tüm klasörlerinizi ve dosyalarınızı siler\
    \n\n**📌Komut ➥ **`.plugins`\
    \n**Kullanım ➥ **Size botta bulunan modüllerin listesini gösterir\
    \n\n**📌Komut ➥ **`.date`\
    \n**Kullanım ➥ **Size bugünün tarihini gösterir\
    \n\n**📌Komut ➥ **`.env`\
    \n**Kullanım ➥ **Size tüm heroku değişkenlerinizin listesini gösterir\
    \n\n**📌Komut ➥ **`.fast`\
    \n**Kullanım ➥ **hız hesaplayıcı\
    \n\n**📌Komut ➥ **`.fortune`\
    \n**Kullanım ➥ **Falcı\
    \n\n**📌Komut ➥ **`.qquote`\
    \n**Kullanım ➥ **Rastgele alıntı oluşturucu\
    \n\n**📌Komut ➥ **`.fakeid`\
    \n**Kullanım ➥ **Rastgele sahte kimlik üreteci\
    \n\n**📌Komut ➥ **`.kwot`\
    \n**Kullanım ➥ **Harika bir rastgele alıntı oluşturucu.\
    \n\n**📌Komut ➥ **`.qpro`\
    \n**Kullanım ➥ **Alıntıları Programlama\
    "
})
