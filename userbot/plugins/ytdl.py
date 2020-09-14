# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
"""
Youtube-dl kullanarak ses ve video indirici
.yta mp3 formatında indirmek için
.ytv mp4 formatında indirmek için
"""

import os
import time
from html import unescape
import math
import asyncio
from youtube_dl import YoutubeDL
from googleapiclient.discovery import build
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)
from telethon.tl.types import DocumentAttributeAudio
from ..utils import admin_cmd, sudo_cmd, edit_or_reply


async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Yüklemeler ve indirmeler için genel progress_callback."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            ''.join(["▰" for i in range(math.floor(percentage / 10))]),
            ''.join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2))
        tmp = progress_str + \
            "{0} of {1}\nETA: {2}".format(
                humanbytes(current),
                humanbytes(total),
                time_formatter(estimated_total_time)
            )
        if file_name:
            await event.edit("{}\nDosya Adı: `{}`\n{}".format(
                type_of_ps, file_name, tmp))
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))


def humanbytes(size):
    """Bayt cinsinden giriş boyutu,
    insan tarafından okunabilir bir formatta çıktılar"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Zamanı milisaniye olarak girerek güzelleşen zamana sahip olun,
    dize olarak"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " günler, ") if days else "") + \
        ((str(hours) + " saatler, ") if hours else "") + \
        ((str(minutes) + " dakikalar, ") if minutes else "") + \
        ((str(seconds) + " saniyeler, ") if seconds else "") + \
        ((str(milliseconds) + " milisaniyeler, ") if milliseconds else "")
    return tmp[:-2]


@borg.on(admin_cmd(pattern="yt(a|v) (.*)"))
@borg.on(sudo_cmd(pattern="yt(a|v) (.*)", allow_sudo=True))
async def download_video(v_url):
    """ .ytdl komutu için, medyayı YouTube'dan ve diğer birçok siteden indirin. """
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()
    v_url = await edit_or_reply(v_url, "`İndirmeye hazırlanıyor...`")
    if type == "a":
        opts = {
            'format':
            'bestaudio',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'writethumbnail':
            True,
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl':
            '%(id)s.mp3',
            'quiet':
            True,
            'logtostderr':
            False
        }
        video = False
        song = True
    elif type == "v":
        opts = {
            'format':
            'best',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl':
            '%(id)s.mp4',
            'logtostderr':
            False,
            'quiet':
            True
        }
        song = False
        video = True
    try:
        await v_url.edit("`Veriler alınıyor, lütfen bekleyin..`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await v_url.edit("`İndirilen içerik çok kısaydı.`")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "`Bir web sitesi tarafından uygulanan coğrafi kısıtlamalar nedeniyle video, coğrafi konumunuzda kullanılamıyor.`"
        )
        return
    except MaxDownloadsReached:
        await v_url.edit("`Maksimum indirme sınırına ulaşıldı.`")
        return
    except PostProcessingError:
        await v_url.edit("`Sonradan işleme sırasında bir hata oluştu.`")
        return
    except UnavailableVideoError:
        await v_url.edit("`Medya, istenen formatta mevcut değil.`")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("`Bilgi çıkarma sırasında bir hata oluştu.`")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await v_url.edit(f"`Şarkıyı yüklemeye hazırlanıyor:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*")
        await borg.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(duration=int(ytdl_data['duration']),
                                       title=str(ytdl_data['title']),
                                       performer=str(ytdl_data['uploader']))
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Yükleniyor..",
                         f"{ytdl_data['title']}.mp3")))
        os.remove(f"{ytdl_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await v_url.edit(f"`Video yüklemeye hazırlanıyor:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*")
        await borg.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp4",
            supports_streaming=True,
            caption=ytdl_data['title'],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Yükleniyor..",
                         f"{ytdl_data['title']}.mp4")))
        os.remove(f"{ytdl_data['id']}.mp4")
        await v_url.delete()


@borg.on(admin_cmd(pattern="yts (.*)"))
@borg.on(sudo_cmd(pattern="yts (.*)", allow_sudo=True))
async def yt_search(video_q):
    """ .yts komutu için Telegram'dan bir YouTube araması yapın. """
    query = video_q.pattern_match.group(1)
    result = ''
    if not Config.YOUTUBE_API_KEY:
        await edit_or_reply(video_q, "`Hata: YouTube API anahtarı eksik! Heroku veya userbot / uniborgConfig.py'deki yapılandırma değişkenlerini github çatalında ortaya çıkarmak için ekleyin.`")
        return
    video_q = await edit_or_reply(video_q, "```İşleniyor...```")
    full_response = await youtube_search(query)
    videos_json = full_response[1]
    for video in videos_json:
        title = f"{unescape(video['snippet']['title'])}"
        link = f"https://youtu.be/{video['id']['videoId']}"
        result += f"{title}\n{link}\n\n"
    reply_text = f"**Arama Sorgusu:**\n`{query}`\n\n**Sonuçlar:**\n\n{result}"
    await video_q.edit(reply_text)


async def youtube_search(query,
                         order="relevance",
                         token=None,
                         location=None,
                         location_radius=None):
    """ Bir YouTube araması yapın. """
    youtube = build('youtube',
                    'v3',
                    developerKey=Config.YOUTUBE_API_KEY,
                    cache_discovery=False)
    search_response = youtube.search().list(
        q=query,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",
        maxResults=10,
        location=location,
        locationRadius=location_radius).execute()
    videos = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    try:
        nexttok = search_response["nextPageToken"]
        return (nexttok, videos)
    except HttpError:
        nexttok = "last_page"
        return (nexttok, videos)
    except KeyError:
        nexttok = "KeyError, try again."
        return (nexttok, videos)
