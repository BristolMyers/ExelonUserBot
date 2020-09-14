# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""Speedtest.net tarafından desteklenen internet hızınızı kontrol edin
Syntax: .speedtest
Kullanılabilir Seçenekler: resim, dosya, metin """
from datetime import datetime
import speedtest
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="speedtest ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    as_text = True
    as_document = False
    if input_str == "image":
        as_document = False
    elif input_str == "file":
        as_document = True
    elif input_str == "text":
        as_text = True
    await event.edit("`İnternet hızımı hesaplıyorum. Lütfen bekle!`")
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = event.message.id
    if event.reply_to_msg_id:
        reply_msg_id = event.reply_to_msg_id
    try:
        response = s.results.share()
        speedtest_image = response
        if as_text:
            await event.edit("""`SpeedTest {} saniye içinde tamamlandı`

`İndirme: {}`
`Yükleme: {}`
`Ping: {}`
`İnternet servis sağlayıcısı: {}`
`ISP Derecelendirmesi: {}`""".format(ms, convert_from_bytes(download_speed), convert_from_bytes(upload_speed), ping_time, i_s_p, i_s_p_rating))
        else:
            await borg.send_file(
                event.chat_id,
                speedtest_image,
                caption="**SpeedTest ** {} saniyede tamamlandı".format(ms),
                force_document=as_document,
                reply_to=reply_msg_id,
                allow_cache=False
            )
            await event.delete()
    except Exception as exc:
        await event.edit("""**SpeedTest ** {} saniyede tamamlandı
İndirme: {}
Yükleme: {}
Ping: {}

__Aşağıdaki HATALARLA__
{}""".format(ms, convert_from_bytes(download_speed), convert_from_bytes(upload_speed), ping_time, str(exc)))


def convert_from_bytes(size):
    power = 2**10
    n = 0
    units = {
        0: "",
        1: "kilobytes",
        2: "megabytes",
        3: "gigabytes",
        4: "terabytes"
    }
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"
