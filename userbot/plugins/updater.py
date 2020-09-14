# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""
Bu modül, kullanıcı botunu yukarı akış revizyonuna göre günceller.
"""
import sys
import asyncio
from git import Repo
from .. import CMD_HELP
from os import environ, execle, path, remove
from ..utils import admin_cmd, sudo_cmd, edit_or_reply
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

HEROKU_APP_NAME = Var.HEROKU_APP_NAME
HEROKU_API_KEY = Var.HEROKU_API_KEY
UPSTREAM_REPO_BRANCH = "master"
UPSTREAM_REPO_URL = "https://github.com/BristolMyers/ExelonUserBot"

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"•[{c.committed_datetime.strftime(d_form)}]: "
            f"{c.summary} <{c.author}>\n"
        )
    return ch_log


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"**EXELON için yeni GÜNCELLEME mevcut!! [{ac_br}]:\n\nDEĞİŞİKLİK:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await event.edit("`Değişiklik günlüğü çok büyük, görmek için dosyayı görüntüleyin.`")
        file = open("output.txt", "w+")
        file.write(changelog_str)
        file.close()
        await event.client.send_file(
            event.chat_id, "output.txt", reply_to=event.id,
        )
        remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id, changelog_str, reply_to=event.id,
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if HEROKU_APP_NAME is None:
            await event.edit(
                "`[HEROKU] `\n`Lütfen ** HEROKU_APP_NAME ** değişkenini ayarlayın!!"
                " Exelonu güncellemek için..."
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await event.edit(
                f"{txt}\n" "`Exelon dyno'yu yüklemek için geçersiz Heroku kimlik bilgileri!!`"
            )
            return repo.__del__()
        await event.edit(
            "`[HEROKU]`" "\n`Exelon dyno derlemesi devam ediyor, lütfen bekleyin...`"
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except Exception as error:
            await event.edit(f"{txt}\n`İşte hata günlüğü:\n{error}`")
            return repo.__del__()
        build = app.builds(order_by="created_at", sort="desc")[0]
        if build.status == "failed":
            await event.edit(
                "`Yapı hatalı oldu!\n" "İptal edildi veya bazı hatalar var...`"
            )
            await asyncio.sleep(5)
            return await event.delete()
        await event.edit("`Başarıyla Güncellendi!\n "" Yeniden başlatılıyor, lütfen bekleyin...`")
    else:
        await event.edit(
            "`[HEROKU] `\n`Lütfen ** HEROKU_APP_NAME ** değişkenini ayarlayın!!"
        )
    return


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    await event.edit(
        "`Başarıyla Güncellendi! \n "" Bot yeniden başlatılıyor... Bir dakika bekleyin!`"
    )
    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)
    return


@bot.on(admin_cmd(outgoing=True, pattern=r"update($| (now|deploy))"))
@borg.on(sudo_cmd(pattern="update($| (now|deploy))", allow_sudo=True))
async def upstream(event):
    ".update komutu için, botun güncel olup olmadığını kontrol edin, belirtilmişse güncelleyin"
    conf = event.pattern_match.group(1).strip()
    event = await edit_or_reply(event, "`Güncellemeler kontrol ediliyor, lütfen bekleyin....`")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    try:
        txt = "`Hata.. nedeniyle güncelleyici devam edemiyor!!"
        txt += "**LOGTRACE**\nbazı problemler oluştu\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`{error} dizini bulunamadı`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Erken başarısızlık! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`Maalesef {error} dizini"
                "bir git reposu gibi görünmüyor.\n"
                "Ancak bunu, Exelon kullanarak düzeltebiliriz."
                ".update now.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[GÜNCELLEYİCİ]:**\n"
            f"`Galiba Exelon botunu modifiye ettin ve kendi branşını kullanıyorsun ({ac_br}). "
            "Bu durum güncelleyicinin kafasını karıştırıyor "
            "Güncelleme nereden çekilecek?. "
            "Lütfen Exelon botunu resmi repodan kullan`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    # Special case for deploy
    if conf == "deploy":
        await event.edit("`Userbot dağıtılıyor, lütfen bekleyin...`")
        await deploy(event, repo, ups_rem, ac_br, txt)
        return
    if changelog == "" and not force_update:
        await event.edit(
            "\n`EXELONUSERBOT is`  **up-to-date**  `with`  "
            f"**{UPSTREAM_REPO_BRANCH}**\n"
        )
        return repo.__del__()
    if conf == "" and force_update is False:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        return await event.respond("**Exelonu Güncellemek İçin** `.update now` **veya** `.update deploy` **Komutunu Kullanın. Ayrıntılar için** `.info updater` yazınız!")

    if force_update:
        await event.edit(
            "`En son kararlı userbot koduna zorla senkronizasyon, lütfen bekleyin ...`"
        )
    if conf == "now":
        await event.edit("`Userbot güncelleniyor, lütfen bekleyin...`")
        await update(event, repo, ups_rem, ac_br)
    return


CMD_HELP.update({"updater": "**PLUGİN İSMİ:** `updater`\
      \n\n**📌Komut ➥ **`.update`\
      \n**Kullanım ➥ ** Botunuza siz kurduktan sonra herhangi bir güncelleme gelip gelmediğini kontrol eder.\
      \n\n**📌Komut ➥ **`.update now`\
      \n**Kullanım ➥ ** Botunuzu günceller.\
      \nExelon deponuzda herhangi bir güncelleme varsa, yeniden başlatırsanız, bunlar en son konuşlandırdığınız zamana geri döner\
      \n\n**📌Komut ➥ ** `.update deploy`\
      \n**Kullanım ➥ ** Exelonu konuşlandırın, böylece yeniden başlatsanız bile önceki sürüme geri dönmez..\
      \nBu, güncelleme olmasa bile her zaman güncellemeyi tetikler"
                 })
