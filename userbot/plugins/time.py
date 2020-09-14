# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
""" Hayallere takılıp yaşamayı unutmak işe yaramaz
Syntax: .getime"""

import os
import asyncio
from datetime import datetime
from pytz import timezone as tz
from userbot.utils import admin_cmd
from datetime import datetime as dt
from pytz import country_names as c_n
from pytz import country_timezones as c_tz
from PIL import Image, ImageDraw, ImageFont
from userbot import CMD_HELP, COUNTRY, TZ_NUMBER

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"

LOCATION = Config.TZ


async def get_tz(con):
    """ Verilen ülkenin saat dilimini alın. """
    if "(Uk)" in con:
        con = con.replace("Uk", "UK")
    if "(Us)" in con:
        con = con.replace("Us", "US")
    if " Of " in con:
        con = con.replace(" Of ", " of ")
    if "(Western)" in con:
        con = con.replace("(Batı)", "(batı)")
    if "Minor Outlying Islands" in con:
        con = con.replace("Küçük Dış Adaları", "küçük dış adalar")
    if "Nl" in con:
        con = con.replace("Nl", "NL")
    for c_code in c_n:
        if con == c_n[c_code]:
            return c_tz[c_code]
    try:
        if c_n[con]:
            return c_tz[con]
    except KeyError:
        return


@borg.on(admin_cmd(outgoing=True,
                   pattern="ctime(?: |$)(.*)(?<![0-9])(?: |$)([0-9]+)?"))
async def time_func(tdata):
    """ .time komutu için, zamanı döndürün
        1. Ülke ergumanı,
        2. Varsayılan userbot ülkesi (.settime kullanarak ayarlayın),
        3. Kullanıcı botunun çalıştığı sunucu.
    """
    con = tdata.pattern_match.group(1).title()
    tz_num = tdata.pattern_match.group(2)
    t_form = "%H:%M"
    c_name = None
    if len(con) > 4:
        try:
            c_name = c_n[con]
        except KeyError:
            c_name = con
        timezones = await get_tz(con)
    elif COUNTRY:
        c_name = COUNTRY
        tz_num = TZ_NUMBER
        timezones = await get_tz(COUNTRY)
    else:
        await tdata.edit(f"**{dt.now().strftime(t_form)}**  `burada.`")
        return
    if not timezones:
        await tdata.edit("`Geçersiz ülke!`")
        return
    if len(timezones) == 1:
        time_zone = timezones[0]
    elif len(timezones) > 1:
        if tz_num:
            tz_num = int(tz_num)
            time_zone = timezones[tz_num - 1]
        else:
            return_str = f"`{c_name} birden çok saat dilimine sahip:`\n\n"

            for i, item in enumerate(timezones):
                return_str += f"`{i+1}. {item}`\n"

            return_str += "\n`Numarayı yazarak birini seçin!`"
            return_str += "komutta.`\n"
            return_str += f"`Örnek: .ctime {c_name} 2`"

            await tdata.edit(return_str)
            return

    dtnow = dt.now(tz(time_zone)).strftime(t_form)
    if c_name != COUNTRY:
        await tdata.edit(
            f"`{C_name} ({time_zone} saat dilimi) '** {dtnow} ** `.`")
        return
    if COUNTRY:
        await tdata.edit(f"`Burada, {COUNTRY} için` **{dtnow}** "
                         f"`({time_zone} saat dilimi).`")
        return


@borg.on(admin_cmd(outgoing=True,
                   pattern="cdate(?: |$)(.*)(?<![0-9])(?: |$)([0-9]+)?"))
async def date_func(dat):
    """ .date komutu için tarihini döndürün
        1. Ülke argümani,
        2. Varsayılan userbot ülkesi (.settime kullanarak ayarlayın),
        3. Kullanıcı botunun çalıştığı sunucu.
    """
    con = dat.pattern_match.group(1).title()
    tz_num = dat.pattern_match.group(2)

    d_form = "%d/%m/%y - %A"
    c_name = ''

    if len(con) > 4:
        try:
            c_name = c_n[con]
        except KeyError:
            c_name = con
        timezones = await get_tz(con)
    elif COUNTRY:
        c_name = COUNTRY
        tz_num = TZ_NUMBER
        timezones = await get_tz(COUNTRY)
    else:
        await dat.edit(f"`**{dt.now (). Strftime (d_form)}** `burada.`")
        return

    if not timezones:
        await dat.edit("`Geçersiz ülke.`")
        return

    if len(timezones) == 1:
        time_zone = timezones[0]
    elif len(timezones) > 1:
        if tz_num:
            tz_num = int(tz_num)
            time_zone = timezones[tz_num - 1]
        else:
            return_str = f"`{c_name} birden çok saat dilimine sahip:`\n"

            for i, item in enumerate(timezones):
                return_str += f"`{i+1}. {item}`\n"

            return_str += "\n`Numarayı yazarak birini seçin"
            return_str += "komutta.`\n"
            return_str += f"Örnek: .cdate {c_name} 2"
            await dat.edit(return_str)
            return
    dtnow = dt.now(tz(time_zone)).strftime(d_form)
    if c_name != COUNTRY:
        await dat.edit(
            f"`It's`  **{dtnow}**  `in {c_name}({time_zone} timezone).`")
        return
    if COUNTRY:
        await dat.edit(f"`It's`  **{dtnow}**  `here, in {COUNTRY}"
                       f"({time_zone} timezone).`")
        return


@borg.on(admin_cmd(pattern="time ?(.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    current_time = datetime.now().strftime(
        f"\n  USERBOT TIMEZONE  \nLOCATION:{LOCATION}\n  Time: %H:%M:%S \n  Date: %d.%m.%y \n")
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.message.id
    if input_str:
        current_time = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
    if not os.path.isdir(
            Config.TMP_DOWNLOAD_DIRECTORY):  # pylint:disable=E0602
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)  # pylint:disable=E0602
    # pylint:disable=E0602
    required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + \
        " " + str(datetime.now()) + ".webp"
    img = Image.new("RGBA", (350, 220), color=(0, 0, 0, 115))
    fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
    drawn_text = ImageDraw.Draw(img)
    drawn_text.text((10, 10), current_time, font=fnt, fill=(255, 255, 255))
    img.save(required_file_name)
    await borg.send_file(  # pylint:disable=E0602
        event.chat_id,
        required_file_name,
        caption="Userbot: Powered by exelon",
        # Courtesy: @ManueI15
        reply_to=reply_msg_id
    )
    os.remove(required_file_name)
    end = datetime.now()
    time_taken_ms = (end - start).seconds
    await event.edit("Çıkartma {} saniye içinde oluşturuldu !!".format(time_taken_ms))
    await asyncio.sleep(5)
    await event.delete()

CMD_HELP.update({
    "time":
    "**📌Komut ➥ **.ctime <ülke adı / kodu> <saat dilimi numarası> \
    \n**Kullanım ➥ ** Bir ülkenin saatini öğrenin. Bir ülkenin birden fazla saat dilimi varsa, hepsini listeler ve birini seçmenize izin verir..\
    \n\n**📌Komut ➥ **.cdate <ülke adı / kodu> <saat dilimi numarası> \
    \n**USAGE : **Bir ülkenin tarihini öğrenin. Bir ülkenin birden fazla saat dilimi varsa, hepsini listeler \ave birini seçmene izin verir.\
    \n\n**📌Komut ➥ **.time \
    \n**Kullanım ➥** heroku değişkeninde TZ'yi değiştirerek değiştirebileceğiniz mevcut varsayılan zamanı gösterir"
})
