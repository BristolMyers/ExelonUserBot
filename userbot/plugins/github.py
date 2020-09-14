# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import requests
from userbot.utils import admin_cmd
from github import Github
import os
import time
from datetime import datetime
from userbot import CMD_HELP

GIT_TEMP_DIR = "./userbot/temp/"


@borg.on(admin_cmd(pattern="github (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    url = "https://api.github.com/users/{}".format(input_str)
    r = requests.get(url)
    if r.status_code != 404:
        b = r.json()
        avatar_url = b["avatar_url"]
        html_url = b["html_url"]
        gh_type = b["type"]
        name = b["name"]
        company = b["company"]
        blog = b["blog"]
        location = b["location"]
        bio = b["bio"]
        created_at = b["created_at"]
        await borg.send_file(
            event.chat_id,
            caption="""Name: [{}]({})
Tür: {}
şirket: {}
Blog: {}
yer: {}
Bio: {}
Profil Oluşturuldu: {}""".format(name, html_url, gh_type, company, blog, location, bio, created_at),
            file=avatar_url,
            force_document=False,
            allow_cache=False,
            reply_to=event
        )
        await event.delete()
    else:
        await event.edit("`{}`: {}".format(input_str, r.text))


@borg.on(admin_cmd(pattern="commit", outgoing=True))
async def download(event):
    if event.fwd_from:
        return
    if Var.GITHUB_ACCESS_TOKEN is None:
        await event.edit("`Lütfen github.com'dan Uygun Erişim Belirteci EKLEYİN`")
        return
    if Var.GIT_REPO_NAME is None:
        await event.edit("`Lütfen kullanıcı botunuzun Uygun Github Repo Adını EKLEYİN`")
        return
    mone = await event.reply("İşleniyor...")
    if not os.path.isdir(GIT_TEMP_DIR):
        os.makedirs(GIT_TEMP_DIR)
    start = datetime.now()
    reply_message = await event.get_reply_message()
    try:
        time.time()
        print("TEMP dizinine indiriliyor")
        downloaded_file_name = await bot.download_media(
            reply_message.media,
            GIT_TEMP_DIR
        )
    except Exception as e:
        await mone.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.delete()
        await mone.edit("{} Saniye içinde `{}` klasörüne indirildi.".format(downloaded_file_name, ms))
        await mone.edit("Committing to Github....")
        await git_commit(downloaded_file_name, mone)


async def git_commit(file_name, mone):
    content_list = []
    access_token = Var.GITHUB_ACCESS_TOKEN
    g = Github(access_token)
    file = open(file_name, "r", encoding='utf-8')
    commit_data = file.read()
    repo = g.get_repo(Var.GIT_REPO_NAME)
    print(repo.name)
    create_file = True
    contents = repo.get_contents("")
    for content_file in contents:
        content_list.append(str(content_file))
        print(content_file)
    for i in content_list:
        create_file = True
        if i == 'ContentFile(path="' + file_name + '")':
            return await mone.edit("`File Already Exists`")
            create_file = False
    file_name = "userbot/plugins/" + file_name
    if create_file:
        file_name = file_name.replace("./userbot/temp/", "")
        print(file_name)
        try:
            repo.create_file(
                file_name,
                "Yeni Plugin Yüklendi",
                commit_data,
                branch="master")
            print("Committed File")
            ccess = Var.GIT_REPO_NAME
            ccess = ccess.strip()
            await mone.edit(f"`Github Reponuza Bağlı`\n\n[Your PLUGINS](https://github.com/{ccess}/tree/master/userbot/plugins/)")
        except BaseException:
            print("Eklenti Oluşturulamıyor")
            await mone.edit("Eklenti Yüklenemiyor")
    else:
        return await mone.edit("`Taahhütlü İntihar`")


CMD_HELP.update({"github": "**PLUGİN İSMİ:** `github`\
      \n\n**📌Komut ➥ **`.github` USERNAME :\
      \n**Kullanım ➥ ** Verdiğiniz kullanıcı adıyla ilgili github bilgilerini size gösterir.\
      \n\n**📌Komut ➥ **`.commit` github'a yüklemek için python dosyasını yanıtla\
      \nEklenti tamamlama çalışması için Heroku vars First'te `GITHUB_ACCESS_TOKEN` ve` GIT_REPO_NAME` Değişkenlerini ayarlayın"
                 })
