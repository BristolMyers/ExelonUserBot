# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers
#
""" Karma ve kodlama / kod çözme komutlarını içeren Userbot modülü. """

from subprocess import PIPE
from subprocess import run as runapp
import pybase64
from userbot import CMD_HELP
from userbot.utils import admin_cmd, errors_handler


@borg.on(admin_cmd(outgoing=True, pattern="hash (.*)"))
@errors_handler
async def gethash(hash_q):
    """ .Hash komutu için dizenin md5, sha1, sha256, sha512'yi bulun. """
    hashtxt_ = hash_q.pattern_match.group(1)
    hashtxt = open("hashdis.txt", "w+")
    hashtxt.write(hashtxt_)
    hashtxt.close()
    md5 = runapp(["md5sum", "hashdis.txt"], stdout=PIPE)
    md5 = md5.stdout.decode()
    sha1 = runapp(["sha1sum", "hashdis.txt"], stdout=PIPE)
    sha1 = sha1.stdout.decode()
    sha256 = runapp(["sha256sum", "hashdis.txt"], stdout=PIPE)
    sha256 = sha256.stdout.decode()
    sha512 = runapp(["sha512sum", "hashdis.txt"], stdout=PIPE)
    runapp(["rm", "hashdis.txt"], stdout=PIPE)
    sha512 = sha512.stdout.decode()
    ans = ("Text: `" + hashtxt_ + "`\nMD5: `" + md5 + "`SHA1: `" + sha1 +
           "`SHA256: `" + sha256 + "`SHA512: `" + sha512[:-1] + "`")
    if len(ans) > 4096:
        hashfile = open("hashes.txt", "w+")
        hashfile.write(ans)
        hashfile.close()
        await hash_q.client.send_file(
            hash_q.chat_id,
            "hashes.txt",
            reply_to=hash_q.id,
            caption="`Çok büyük, bunun yerine bir metin dosyası gönderiyor. `")
        runapp(["rm", "hashes.txt"], stdout=PIPE)
    else:
        await hash_q.reply(ans)


@borg.on(admin_cmd(outgoing=True, pattern="hbase (en|de) (.*)"))
@errors_handler
async def endecrypt(query):
    """ .base64 komutu için, verilen dizenin base64 kodlamasını bulun. """
    if query.pattern_match.group(1) == "en":
        lething = str(
            pybase64.b64encode(bytes(query.pattern_match.group(2),
                                     "utf-8")))[2:]
        await query.reply("Shhh! It's Encoded: `" + lething[:-1] + "`")
    else:
        lething = str(
            pybase64.b64decode(bytes(query.pattern_match.group(2), "utf-8"),
                               validate=True))[2:]
        await query.reply("Decoded: `" + lething[:-1] + "`")


CMD_HELP.update(
    {"hash": ".hbase en veya .hbase de \nUsage: Verilen dizenin base64 kodlamasını bulun\
    \n\n.hash\nUsage: Bir txt dosyasına yazıldığında dizenin md5, sha1, sha256, sha512'yi bulun."})
