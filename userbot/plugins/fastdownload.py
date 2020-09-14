# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

"""
command: .url
"""
import aria2p
import asyncio
import os
from userbot.utils import admin_cmd
cmd = "aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --min-split-size=10M --follow-torrent=mem --split=10 --daemon=true"

aria2_is_running = os.system(cmd)

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret=""
    )
)

EDIT_SLEEP_TIME_OUT = 10


@borg.on(admin_cmd(pattern="fdownload ?(.*)"))
async def magnet_download(event):
    if event.fwd_from:
        return
    var = event.pattern_match.group(1)
    print(var)
    uris = [var]
    # Add URL Into Queue
    try:
        download = aria2.add_uris(uris, options=None, position=None)
    except Exception as e:
        await event.edit("`Error:\n`" + str(e))
        return
    gid = download.gid
    complete = None
    await progress_status(gid=gid, event=event, previous=None)
    file = aria2.get_download(gid)
    if file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await progress_status(gid=new_gid, event=event, previous=None)
    while complete != True:
        file = aria2.get_download(gid)
        complete = file.is_complete
        try:
            msg = "**Dosya indiriliyor:** " + str(file.name) + "\n**Hız:** " + str(file.download_speed_string()) + "\n**İlerleme:** " + str(
                file.progress_string()) + "\n**Toplam boyut:** " + str(file.total_length_string()) + "\n**ETA:**  " + str(file.eta_string()) + "\n\n"
            await event.edit(msg)
            await asyncio.sleep(10)
        except Exception:
            # print(str(e))
            pass
    await event.edit("**Dosya Başarıyla İndirildi:** `{}`".format(file.name))


async def progress_status(gid, event, previous):
    try:
        file = aria2.get_download(gid)
        if not file.is_complete:
            if not file.error_message:
                msg = "Dosya indiriliyor: `" + str(file.name) + "`\nHız: " + str(file.download_speed_string()) + "\nİlerleme: " + str(file.progress_string(
                )) + "\nToplam boyut: " + str(file.total_length_string()) + "\nDurum: " + str(file.status) + "\nETA:  " + str(file.eta_string()) + "\n\n"
            if previous != msg:
                await event.edit(msg)
                previous = msg
            else:
                logger.info(str(file.error_message))
                await event.edit("Hata : `{}`".format(str(file.error_message)))
                return
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            await progress_status(gid, event, previous)
        else:
            await event.edit("Dosya Başarıyla İndirildi: `{}`".format(file.name))
            return
    except Exception as e:
        if " bulunamadı" in str(e) or "'dosya'" in str(e):
            await event.edit("İndirme İptal Edildi :\n`{}`".format(file.name))
            return
        if " derinlik aşıldı" in str(e):
            file.remove(force=True)
            await event.edit("İndirme Otomatik İptal Edildi :\n`{}`\nTorrent'iniz / Bağlantınız Bitti.".format(file.name))
        else:
            logger.info(str(e))
            await event.edit("Hata :\n`{}`".format(str(e)))
            return


async def check_metadata(gid):
    file = aria2.get_download(gid)
    new_gid = file.followed_by_ids[0]
    logger.info("GID'yi değiştirme " + gid + " to " + new_gid)
    return new_gid
