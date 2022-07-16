# Copyright (C) 2021-present by Altruix@Github, < https://github.com/Altruix >.
#
# This file is part of < https://github.com/Altruix/Altruix > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Altriux/Altruix/blob/main/LICENSE >
#
# All rights reserved.

import os
import time
from Main import Altruix
from Main.utils.essentials import Essentials
from pyrogram.types import Message


@Altruix.register_on_cmd(
    ["rename"],
    cmd_help={"help": "rename files from telegram", "cmd_help": "rename"},
    requires_reply=True,
)
async def download_files_from_telegram(c, m: Message):
    msg = await m.handle_message("PROCESSING")
    if not m.reply_to_message.media:
        return await msg.edit_msg('REPLY_TO_FILE')
    input_ = m.user_input
    user_args = m.user_args
    start_time = time.time()
    downloads_path = (
        "./custom_files/thumb.jpg" if "-sethumb" in user_args else "./downloads/"+str(input_)
    )
    if not os.path.exists(downloads_path):
            os.mkdir(downloads_path)
    if "-sethumb" in user_args and not m.reply_to_message.photo:
        return await msg.edit_msg("INVALID_REPLY")
    file_ = await m.reply_to_message.download(
        file_name=downloads_path + (input_ or ""),
        progress=(None if "-np" in m.user_args else Essentials.progress),
        progress_args=("download", start_time, m),
    )

    end_time = round(time.time() - start_time, 2)
    await msg.edit_msg("FILE_DOWNLOADED", string_args=(file_, end_time))
    msg = await m.handle_message("PROCESSING")
    msg_id = m.reply_to_message.id if m.reply_to_message else m.id
    thumb = "./custom_files/thumb.jpg"
    thumb = thumb if os.path.exists(thumb) else None
    if not os.path.exists(input_):
        return await msg.edit_msg("404_FILE_NOT_FOUND")
    await c.send_file(
        m.chat.id,
        file_,
        thumb=thumb,
        progress=(None if "-np" in m.user_args else Essentials.progress),
        progress_args=("upload", start_time, msg),
        reply_to_message_id=msg_id,
    )
    time_taken = round(time.time() - start_time, 2)
    file_size = Essentials.humanbytes(os.stat(input_).st_size)
    await msg.edit_msg("FILE_UPLOAD", string_args=(input_, file_size, time_taken))
