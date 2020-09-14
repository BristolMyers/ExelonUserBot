# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

""" Bir şehrin hava durumunu öğrenmek için kullanıcı botu modülü. """
from pytz import country_timezones as c_tz, timezone as tz, country_names as c_n
from ..utils import admin_cmd, sudo_cmd, edit_or_reply, errors_handler
from .. import OPEN_WEATHER_MAP_APPID as OWM_API, CMD_HELP
from datetime import datetime
import requests
import aiohttp
import json
import time
import io
import logging
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING)

# ===== CONSTANT =====
DEFCITY = 'İstanbul'
# ====================


async def get_tz(con):
    """ Verilen ülkenin saat dilimini alın. """
    """ Credits: @BristolMyers. """
    for c_code in c_n:
        if con == c_n[c_code]:
            return tz(c_tz[c_code][0])
    try:
        if c_n[con]:
            return tz(c_tz[con][0])
    except KeyError:
        return


@borg.on(admin_cmd(pattern="weather (.*)"))
@borg.on(sudo_cmd(pattern="weather (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    sample_url = "https://api.openweathermap.org/data/2.5/weather?q={}&APPID={}&units=metric"
    input_str = event.pattern_match.group(1)
    async with aiohttp.ClientSession() as session:
        response_api_zero = await session.get(sample_url.format(input_str, Config.OPEN_WEATHER_MAP_APPID))
    response_api = await response_api_zero.json()
    if response_api["cod"] == 200:
        country_code = response_api["sys"]["country"]
        country_time_zone = int(response_api["timezone"])
        sun_rise_time = int(response_api["sys"]["sunrise"]) + country_time_zone
        sun_set_time = int(response_api["sys"]["sunset"]) + country_time_zone
        event = await edit_or_reply(event,
                                    """{}
🌡**Sıcaklık**: {}°С
    🥶__minimium__: {}°С
    🥵__maximum__ : {}°С
☁️**Nem**: {}%
🌬**rüzgar**: {}m/s
⛈bulutlar: {}hpa
🌄**gündoğumu**: {} {}
🌅**Gün batımı**: {} {}""".format(
                                        input_str,
                                        response_api["main"]["temp"],
                                        response_api["main"]["temp_min"],
                                        response_api["main"]["temp_max"],
                                        response_api["main"]["humidity"],
                                        response_api["wind"]["speed"],
                                        response_api["clouds"]["all"],
                                        # response_api["main"]["pressure"],
                                        time.strftime(
                                            "%Y-%m-%d %H:%M:%S", time.gmtime(sun_rise_time)),
                                        country_code,
                                        time.strftime(
                                            "%Y-%m-%d %H:%M:%S", time.gmtime(sun_set_time)),
                                        country_code
                                    )
                                    )
    else:
        event = await edit_or_reply(event, response_api["message"])


@borg.on(admin_cmd(outgoing=True, pattern="climate(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="climate(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def get_weather(weather):
    """ .weather komutu için bir şehrin güncel hava durumunu alır. """
    if not OWM_API:
        await edit_or_reply(weather,
                            "`Önce` https://openweathermap.org/ `adresinden bir API anahtarı alın.`")
        return
    APPID = OWM_API
    if not weather.pattern_match.group(1):
        CITY = DEFCITY
        if not CITY:
            await edit_or_reply(weather, "`Lütfen bir şehir belirtin veya varsayılan olarak ayarlayın.`")
            return
    else:
        CITY = weather.pattern_match.group(1)
    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items() for timezone in timezones
    }
    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f'{country}']
            except KeyError:
                await weather.edit("`Geçersiz ülke.`")
                return
            CITY = newcity[0].strip() + "," + countrycode.strip()
    url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={APPID}'
    request = requests.get(url)
    result = json.loads(request.text)
    if request.status_code != 200:
        await weather.edit(f"`Geçersiz ülke.`")
        return
    cityname = result['name']
    curtemp = result['main']['temp']
    humidity = result['main']['humidity']
    min_temp = result['main']['temp_min']
    max_temp = result['main']['temp_max']
    pressure = result['main']['pressure']
    feel = result['main']['feels_like']
    desc = result['weather'][0]
    desc = desc['main']
    country = result['sys']['country']
    sunrise = result['sys']['sunrise']
    sunset = result['sys']['sunset']
    wind = result['wind']['speed']
    winddir = result['wind']['deg']
    cloud = result['clouds']['all']
    ctimezone = tz(c_tz[country][0])
    time = datetime.now(ctimezone).strftime("%A, %I:%M %p")
    fullc_n = c_n[f"{country}"]
    # dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    #        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    div = (360 / len(dirs))
    funmath = int((winddir + (div / 2)) / div)
    findir = dirs[funmath % len(dirs)]
    kmph = str(wind * 3.6).split(".")
    mph = str(wind * 2.237).split(".")

    def fahrenheit(f):
        temp = str(((f - 273.15) * 9 / 5 + 32)).split(".")
        return temp[0]

    def celsius(c):
        temp = str((c - 273.15)).split(".")
        return temp[0]

    def sun(unix):
        xx = datetime.fromtimestamp(unix, tz=ctimezone).strftime("%I:%M %p")
        return xx
    await edit_or_reply(weather,
                        f"🌡**sıcaklık:** `{celsius(curtemp)}°C | {fahrenheit(curtemp)}°F`\n" +
                        f"🥰**Hissedilen** `{celsius(feel)}°C | {fahrenheit(feel)}°F`\n" +
                        f"🥶**En düşük sıcaklık.:** `{celsius(min_temp)}°C | {fahrenheit(min_temp)}°F`\n" +
                        f"🥵**En yüksek sıcaklık.:** `{celsius(max_temp)}°C | {fahrenheit(max_temp)}°F`\n" +
                        f"☁️**Nem:** `{humidity}%`\n" +
                        f"🧧**Basınç** `{pressure} hPa`\n" +
                        f"🌬**Rüzgar:** `{kmph[0]} kmh | {mph[0]} mph, {findir}`\n" +
                        f"⛈**Bulut:** `{cloud} %`\n" +
                        f"🌄**gündoğumu:** `{sun(sunrise)}`\n" +
                        f"🌅**Gün batımı:** `{sun(sunset)}`\n\n\n" +
                        f"**{desc}**\n" +
                        f"`{cityname}, {fullc_n}`\n" +
                        f"`{time}`\n")


@borg.on(admin_cmd(outgoing=True, pattern="setcity(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="setcity(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def set_default_city(city):
    """ .ctime komutu için, tarih ve saat komutları için varsayılan userbot ülkesini değiştirin. """
    if not OWM_API:
        await edit_or_reply(city,
                            "`Önce` https://openweathermap.org/ `adresinden bir API anahtarı alın.`")
        return
    global DEFCITY
    APPID = OWM_API
    if not city.pattern_match.group(1):
        CITY = DEFCITY
        if not CITY:
            await edit_or_reply(city, "`Lütfen varsayılan olarak ayarlamak için bir şehir belirtin.`")
            return
    else:
        CITY = city.pattern_match.group(1)
    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items() for timezone in timezones
    }
    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f'{country}']
            except KeyError:
                await edit_or_reply(city, "`Geçersiz ülke.`")
                return
            CITY = newcity[0].strip() + "," + countrycode.strip()
    url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={APPID}'
    request = requests.get(url)
    result = json.loads(request.text)
    if request.status_code != 200:
        await city.edit(f"`Geçersiz ülke.`")
        return
    DEFCITY = CITY
    cityname = result['name']
    country = result['sys']['country']
    fullc_n = c_n[f"{country}"]
    await edit_or_reply(city, f"`Set default city as {cityname}, {fullc_n}.`")


@borg.on(admin_cmd(pattern="wttr (.*)"))
@borg.on(sudo_cmd(pattern="wttr (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    sample_url = "https://wttr.in/{}.png"
    # logger.info(sample_url)
    input_str = event.pattern_match.group(1)
    async with aiohttp.ClientSession() as session:
        response_api_zero = await session.get(sample_url.format(input_str))
        # logger.info(response_api_zero)
        response_api = await response_api_zero.read()
        with io.BytesIO(response_api) as out_file:
            await event.reply(
                file=out_file
            )
    await event.edit(input_str)


CMD_HELP.update({"climate": "**PLUGİN İSMİ:** `climate`\
      \n\n**📌Komut ➥ **`.climate <şehir> veya .weather <şehir>, <ülke adı/kodu>` :\
      \n**Kullanım ➥ ** Bir şehrin havasını alır.\
      \n\n**📌Komut ➥ **`.setcity <şehir> veya .setcity <city>, <ülke adı/kodu>` :\
      \n**Kullanım ➥ ** Yalnızca .weather kullanabilmeniz için varsayılan şehrinizi ayarlar."
                 })
