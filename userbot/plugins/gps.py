# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from geopy.geocoders import Nominatim
from userbot.utils import admin_cmd, sudo_cmd
from telethon.tl import types
from userbot import CMD_HELP


@borg.on(admin_cmd(pattern="gps ?(.*)"))
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.edit("ne bulmalıyım bana konum ver.")

    await event.edit("buluyorum")

    geolocator = Nominatim(user_agent="ExelonUserBot")
    geoloc = geolocator.geocode(input_str)

    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await reply_to_id.reply(
            input_str,
            file=types.InputMediaGeoPoint(
                types.InputGeoPoint(
                    lat, lon
                )
            )
        )
        await event.delete()
    else:
        await event.edit("bulamadım")


@borg.on(sudo_cmd(pattern="gps ?(.*)", allow_sudo=True))
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.reply("ne bulmalıyım bana konum ver.")

    exelon = await event.reply("buluyorum")

    geolocator = Nominatim(user_agent="ExelonUserBo")
    geoloc = geolocator.geocode(input_str)

    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await reply_to_id.reply(
            input_str,
            file=types.InputMediaGeoPoint(
                types.InputGeoPoint(
                    lat, lon
                )
            )
        )
        await exelon.delete()
    else:
        await exelon.edit("bulamadım")


CMD_HELP.update({"gps": "`.gps` <yer ismi> :\
      \nKullanım ➥ size verilen yer adını gönderir\
      "
                 })
