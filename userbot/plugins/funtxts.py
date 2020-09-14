# Copyright (C) 2020 BristolMyers
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# ExelonUserBot - BristolMyers

import nekos
from ..utils import admin_cmd


@borg.on(admin_cmd(pattern="texelon$"))
async def hmm(exelon):
    if exelon.fwd_from:
        return
    reactexelon = nekos.textexelon()
    await exelon.edit(reactexelon)


@borg.on(admin_cmd(pattern="why$"))
async def hmm(exelon):
    if exelon.fwd_from:
        return
    whyexelon = nekos.why()
    await exelon.edit(whyexelon)


@borg.on(admin_cmd(pattern="fact$"))
async def hmm(exelon):
    if exelon.fwd_from:
        return
    factexelon = nekos.fact()
    await exelon.edit(factexelon)
