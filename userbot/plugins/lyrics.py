# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import os
import lyricsgenius
from userbot.utils import admin_cmd
from userbot import CMD_HELP
from tswift import Song
import io
GENIUS = os.environ.get("GENIUS_API_TOKEN", None)


@borg.on(admin_cmd(outgoing=True, pattern="lyrics ?(.*)"))
async def _(event):
    await event.edit("wi8..! Şarkı sözlerini arıyorum....`")
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply.text:
        query = reply.message
    else:
        await event.edit("`Ne bulmam gerekiyor `")
        return
    song = ""
    song = Song.find_song(query)
    if song:
        if song.lyrics:
            reply = song.format()
        else:
            reply = "O şarkı için herhangi bir şarkı sözü bulunamadı! Hala çalışmıyorsa şarkıyla birlikte sanatçı adını deneyin `.glyrics` i deneyin"
    else:
        reply = "şarkı sözleri bulunamadı! Hala çalışmıyorsa şarkıyla birlikte sanatçı adını deneyin `.glyrics` i deneyin"
    if len(reply) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(reply)) as out_file:
            out_file.name = "lyrics.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=query,
                reply_to=reply_to_id
            )
            await event.delete()
    else:
        await event.edit(reply)


@borg.on(admin_cmd(outgoing=True, pattern="glyrics ?(.*)"))
async def lyrics(lyric):
    if lyric.pattern_match.group(1):
        query = lyric.pattern_match.group(1)
    else:
        await lyric.edit("Hata: lütfen <sanatçı> ve <şarkı> için ayırıcı olarak '-' kullanın\neÖrneğin `.glyrics Nicki Minaj - Super Bass`")
        return
    if r"-" in query:
        pass
    else:
        await lyric.edit("Hata: lütfen <sanatçı> ve <şarkı> için ayırıcı olarak '-' kullanın \neg: `.glyrics Nicki Minaj - Super Bass`")
        return
    if GENIUS is None:
        await lyric.edit("`Config.py veya Heroku Var'a genius erişim belirteci sağlayın ilk kthxbye!`")
    else:
        genius = lyricsgenius.Genius(GENIUS)
        try:
            args = query.split('-', 1)
            artist = args[0].strip(' ')
            song = args[1].strip(' ')
        except Exception as e:
            await lyric.edit(f"Error:\n`{e}`")
            return
    if len(args) < 1:
        await lyric.edit("`Lütfen sanatçı ve şarkı adlarını belirtin`")
        return
    await lyric.edit(f"`{artist} - {song} için şarkı sözleri aranıyor...`")
    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None
    if songs is None:
        await lyric.edit(f"{Artist} adlı şarkı - {song} bulunamadı!")
        return
    if len(songs.lyrics) > 4096:
        await lyric.edit("`Şarkı sözleri çok büyük, görmek için dosyayı görüntüleyin.`")
        with open("lyrics.txt", "w+") as f:
            f.write(f"Arama sorgusu: \n{artist} - {song}\n\n{songs.lyrics}")
        await lyric.client.send_file(
            lyric.chat_id,
            "lyrics.txt",
            reply_to=lyric.id,
        )
        os.remove("lyrics.txt")
    else:
        await lyric.edit(f"**Arama sorgusu**: \n`{artist} - {song}`\n\n```{songs.lyrics}```")
    return

CMD_HELP.update(
    {"lyrics": "Lyrics Plugin Syntax: `.lyrics` <sanatçı adı - şarkı adı> or `.lyrics` <song_name>\
    \n**Kullanım ➥ ** şarkı sözlerini arar ve şarkı adı işe yaramazsa size gönderir, sanatçı adıyla birlikte deneyin\
    \n\n**📌Komut ➥ ** .`glyrics <sanatçı adı> - <şarkı adı>`\
    \n📌NOT ➥ **-** bölünmüş sanatçı ve şarkı sözlerini ararken gereklidir\
    \n\n**Genius lyrics plugin**\
    \nbu değeri `https: // genius.com / developer` dan alın \
    \n📌Ekle ➥ Heroku uygulama ayarlarında `GENIUS_API_TOKEN`değerini doldurun \
    "})
