# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""
  Kullanıcı botunuz için Heroku yöneticisi
"""

import os
import math
import heroku3
import asyncio
import urllib3
import requests
from .. import CMD_HELP
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# =================

Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY


@borg.on(
    admin_cmd(
        pattern=r"(set|get|del) var(?: |$)(.*)(?: |$)([\s\S]*)",
        outgoing=True))
@borg.on(
    sudo_cmd(
        pattern=r"(set|get|del) var(?: |$)(.*)(?: |$)([\s\S]*)",
        allow_sudo=True))
async def variable(var):
    """
        Config Vars ayarlarının çoğunu yönetin, yeni değişken ayarlayın, mevcut değişkeni alın veya değişkeni silin...
    """
    if Var.HEROKU_APP_NAME is not None:
        app = Heroku.app(Var.HEROKU_APP_NAME)
    else:
        return await edit_or_reply(var, "`[HEROKU]:"
                                   "\nLütfen kurulumunu yap` **HEROKU_APP_NAME**")
    exe = var.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "get":
        exelon = await edit_or_reply(var, "`Bilgi alınıyor...`")
        await asyncio.sleep(1.0)
        try:
            variable = var.pattern_match.group(2).split()[0]
            if variable in heroku_var:
                return await exelon.edit("**ConfigVars**:"
                                         f"\n\n`{variable} = {heroku_var[variable]}`\n")
            return await exelon.edit("**ConfigVars**:"
                                     f"\n\n`Error:\n-> {variable} don't exists`")
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await bot.send_file(
                        var.chat_id,
                        "configs.json",
                        reply_to=var.id,
                        caption="`Çıktı çok büyük, dosya olarak gönderiliyor`",
                    )
                else:
                    await exelon.edit("`[HEROKU]` ConfigVars:\n\n"
                                      "================================"
                                      f"\n```{result}```\n"
                                      "================================"
                                      )
            os.remove("configs.json")
            return
    elif exe == "set":
        exelon = await edit_or_reply(var, "`Ayar bilgileri...`")
        variable = var.pattern_match.group(2)
        if not variable:
            return await exelon.edit(">`.set var <ConfigVars-name> <value>`")
        value = var.pattern_match.group(3)
        if not value:
            variable = variable.split()[0]
            try:
                value = var.pattern_match.group(2).split(' ', 1)[1]
            except IndexError:
                return await exelon.edit(">`.set var <ConfigVars-name> <value>`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await exelon.edit(f"`{variable}`** başarıyla  **`{value}` **olarak değiştirildi**")
        else:
            await exelon.edit(f"`{variable}`**  değerle başarıyla eklendi`  ->  **{value}`")
        heroku_var[variable] = value
    elif exe == "del":
        exelon = await edit_or_reply(var, "`Değişkeni silmek için bilgi alma...`")
        try:
            variable = var.pattern_match.group(2).split()[0]
        except IndexError:
            return await exelon.edit("`Lütfen silmek istediğiniz Config Vars'ı belirtin`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await exelon.edit(f"`{variable}`  **Başarıyla silindi**")
            del heroku_var[variable]
        else:
            return await exelon.edit(f"`{variable}`**  mevcut değil**")


@borg.on(admin_cmd(pattern="usage$", outgoing=True))
@borg.on(sudo_cmd(pattern="usage$", allow_sudo=True))
async def dyno_usage(dyno):
    """
        Hesabınızı Dyno Kullanımı alın
    """
    dyno = await edit_or_reply(dyno, "`İşleniyor...`")
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/80.0.3987.149 Mobile Safari/537.36'
                 )
    user_id = Heroku.account().id
    headers = {
        'User-Agent': useragent,
        'Authorization': f'Bearer {Var.HEROKU_API_KEY}',
        'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("`Hata: kötü bir şey oldu`\n\n"
                               f">.`{r.reason}`\n")
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    """ - Current - """
    App = result['apps']
    try:
        App[0]['quota_used']
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]['quota_used'] / 60
        AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    return await dyno.edit("**Dyno Kullanımı**:\n\n"
                           f" -> `Dyno kullanımı`  **{Var.HEROKU_APP_NAME}**:\n"
                           f"     •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
                           f"**|**  [`{AppPercentage}`**%**]"
                           "\n\n"
                           " -> `Bu ay kalan Dyno saat kotası`:\n"
                           f"     •  `{hours}`**h**  `{minutes}`**m**  "
                           f"**|**  [`{percentage}`**%**]"
                           )


@borg.on(admin_cmd(pattern="herokulogs$", outgoing=True))
@borg.on(sudo_cmd(pattern="herokulogs$", allow_sudo=True))
async def _(dyno):
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await dyno.reply(" Lütfen Heroku API Anahtarınızın, Uygulama adınızın heroku'da doğru şekilde yapılandırıldığından emin olun")
    data = app.get_log()
    key = requests.post('https://nekobin.com/api/documents',
                        json={"content": data}).json().get('result').get('key')
    url = f'https://nekobin.com/{key}'
    reply_text = f'Son 100 satır heroku günlüğüs: [burada]({url})'
    await edit_or_reply(dyno, reply_text)


def prettyjson(obj, indent=2, maxlinelength=80):
    """JSON içeriğini maksimum uzunluğa uyacak şekilde girinti ve çizgi bölmeleri / birleştirmeleriyle işler.
    Yalnızca dikteler, listeler ve temel türler desteklenir"""
    items, _ = getsubitems(obj, itemkey="", islast=True,
                           maxlinelength=maxlinelength - indent, indent=indent)
    return indentitems(items, indent, level=0)


CMD_HELP.update({
    "heroku":
    "Heroku'yu Yönetmek İçin Modül Bilgileri:**\
    \n\n**📌Komut ➥ ** `.usage`\
    \nKullanım ➥__Heroku dyno saatleri durumunuzu kontrol edin.__\
    \n\n**📌Komut ➥ **`.set var <NEW VAR> <VALUE>`\
    \nKullanım ➥ __yeni değişken ekleyin veya mevcut değer değişkenini güncelleyin__\
    \n**!!! UYARI !!!, bir değişken ayarladıktan sonra bot yeniden başlayacaktır.**\
    \n\n**📌Komut ➥ **`.get var veya .get var <VAR>`\nKullanım ➥ __mevcut değişkenlerinizi alın, sadece özel grubunuzda kullanın!__\
    \n**Bu, tüm özel bilgilerinizi döndürür, lütfen dikkatli olun...**\
    \n\n**📌Komut ➥** `.del var <VAR>`\
    \nKullanım ➥ __mevcut değişkeni sil__\
    \n**!!! UYARI !!!, değişkeni sildikten sonra bot yeniden başlayacaktır**\
    \n\n**📌Komut ➥** `.herokulogs`\
    \nUsage:size heroku'daki son 100 satırlık günlükleri gönderir"
})
