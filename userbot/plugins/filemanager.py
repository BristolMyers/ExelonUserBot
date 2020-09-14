# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import io
import os
import os.path
import time
from . import runcmd
from userbot import CMD_HELP
from ..utils import admin_cmd, sudo_cmd, edit_or_reply, humanbytes
from os.path import exists, isdir


@borg.on(admin_cmd(pattern="ls ?(.*)"))
@borg.on(sudo_cmd(pattern="ls ?(.*)", allow_sudo=True))
async def lst(event):
    exelon = event.pattern_match.group(1)
    if exelon:
        path = exelon
    else:
        path = os.getcwd()
    if not exists(path):
        await edit_or_reply(event, f" `{exelon}` adında böyle bir dizin veya dosya yok tekrar kontrol edin")
        return
    if isdir(path):
        if exelon:
            msg = "Klasörler ve Dosyalar `{}` :\n".format(path)
            lists = os.listdir(path)
        else:
            msg = "Mevcut Dizindeki Klasörler ve Dosyalar :\n"
            lists = os.listdir(path)
        files = ""
        folders = ""
        for contents in sorted(lists):
            exelonpath = path + "/" + contents
            if not isdir(exelonpath):
                size = os.stat(exelonpath).st_size
                if contents.endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += "🎵" + f"`{contents}`\n"
                if contents.endswith((".opus")):
                    files += "🎙" + f"`{contents}`\n"
                elif contents.endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
                    files += "🎞" + f"`{contents}`\n"
                elif contents.endswith((".zip", ".tar", ".tar.gz", ".rar")):
                    files += "🗜" + f"`{contents}`\n"
                elif contents.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
                    files += "🖼" + f"`{contents}`\n"
                else:
                    files += "📄" + f"`{contents}`\n"
            else:
                folders += f"📁`{contents}`\n"
        if files or folders:
            msg = msg + folders + files
        else:
            msg = msg + "__boş yol__"
    else:
        size = os.stat(path).st_size
        msg = f"Verilen dosyanın detayları :\n"
        if path.endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎵"
        if path.endswith((".opus")):
            mode = "🎙"
        elif path.endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎞"
        elif path.endswith((".zip", ".tar", ".tar.gz", ".rar")):
            mode = "🗜"
        elif path.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
            mode = "🖼"
        else:
            mode = "📄"
        time.ctime(os.path.getctime(path))
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        msg += f"**yer :** `{path}`\n"
        msg += f"**ikon :** `{mode}`\n"
        msg += f"**Boyut :** `{humanbytes(size)}`\n"
        msg += f"**Son Değiştirilme Zamanı:** `{time2}`\n"
        msg += f"**Son Erişim Zamanı:** `{time3}`"
    if len(msg) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "ls.txt"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=path
            )
            await event.delete()
    else:
        await edit_or_reply(event, msg)


@borg.on(admin_cmd(pattern="rem ?(.*)"))
@borg.on(sudo_cmd(pattern="rem ?(.*)", allow_sudo=True))
async def lst(event):
    exelon = event.pattern_match.group(1)
    if exelon:
        path = exelon
    else:
        await edit_or_reply(event, "neyi silmeliyim")
        return
    if not exists(path):
        await edit_or_reply(event, f" `{exelon}` adında böyle bir dizin veya dosya yok tekrar kontrol edin")
        return
    exeloncmd = f"rm -rf {path}"
    if isdir(path):
        await runcmd(exeloncmd)
        await edit_or_reply(event, f"`{path}` dizini başarıyla kaldırıldı")
    else:
        await runcmd(exeloncmd)
        await edit_or_reply(event, f"{path}` dosyası başarıyla kaldırıldı")


CMD_HELP.update({"filemanager": "**PLUGİN İSMİ:** `filemanager`\
      \n\nUserbot için Dosyaları Listeleme eklentisi \
      \n\n**📌Komut ➥ **`.ls` :\
      \n**Kullanım ➥ ** dosyaları geçerli çalışma dizininden döndürür.\
      \n\n**📌Komut ➥ **`.ls path` :\
      \n**Kullanım ➥ ** yola göre çıktı döndürecektir.\
      \n\n**📌Komut ➥ ** `.ls dosya yolu`\
      \n**Kullanım ➥ ** dosya ayrıntılarını döndürür.\
      \n\nDosyaları listelemek için kabuk yürütücüsünü kullanmak istemeyen kişiler için Basit Modül.\
      \n\n**📌Komut ➥ **`.rem path` :\
      \n**Kullanım ➥ ** Gerekli öğeyi bot sunucusundan silmek için."
                 })
