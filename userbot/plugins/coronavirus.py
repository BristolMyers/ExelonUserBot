# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

from .. import CMD_HELP
from covid import Covid
from ..utils import admin_cmd, sudo_cmd, edit_or_reply


@borg.on(admin_cmd(pattern="corona(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="corona(?: |$)(.*)", allow_sudo=True))
async def corona(event):
    if event.pattern_match.group(1):
        country = event.pattern_match.group(1)
    else:
        country = "Dünya"
    covid = Covid(source="Dünya Geneli")
    data = ""
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data['confirmed'] + country_data['new_cases']
        hmm2 = country_data['deaths'] + country_data['new_deaths']
        data += f"\n**⚠️Onaylanmış**  : `{hmm1}`"
        data += f"\n**😔Aktif**          : `{country_data['active']}`"
        data += f"\n**⚰️Ölen**          : `{hmm2}`"
        data += f"\n**🤕Kritik**          : `{country_data['critical']}`"
        data += f"\n**😊Kurtarılan**  : `{country_data['recovered']}`"
        data += f"\n**💉Toplam test**    : `{country_data['total_tests']}`"
        data += f"\n**🥺Yeni Vakalar**   : `{country_data['new_cases']}`"
        data += f"\n**😟Yeni Ölümler** : `{country_data['new_deaths']}`"
    else:
        data += "\nBu ülke hakkında henüz bilgi yok!"
    await edit_or_reply(event, "**Corona Virüs Bilgisi {}:**\n{}".format(country.capitalize(), data))


CMD_HELP.update({"coronavirus": "**PLUGİN İSMİ:** `coronavirus`\
      \n\n**📌Komut ➥ **``.covid ` <ülke adı> :\
      \n**Kullanım ➥ ** Verilen ülkedeki covid-19 verileri hakkında bilgi alın.\
      "
                 })
