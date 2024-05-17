from pyrogram import filters
from pyrogram.types import Message

from ZeMusic import app
from ZeMusic.misc import SUDOERS
from ZeMusic.utils.database import add_sudo, remove_sudo
from ZeMusic.utils.decorators.language import language
from ZeMusic.utils.extraction import extract_user
from ZeMusic.utils.inline import close_markup
from config import BANNED_USERS, OWNER_ID


@app.on_message(filters.command(["رفع ngd "]) & filters.user(OWNER_ID))
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply(_["sudo_1"].format(user.mention))
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply(_["sudo_2"].format(user.mention))
    else:
        await message.reply(_["sudo_8"])


@app.on_message(filters.command(["تنزيل ngd ", "rmsudo"]) & filters.user(OWNER_ID))
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply(_["general_1"])
    user = await extract_user(message)
    if user.id not in SUDOERS:
        return await message.reply(_["sudo_3"].format(user.mention))
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply(_["sudo_4"].format(user.mention))
    else:
        await message.reply(_["sudo_8"])


@app.on_message(filters.command(["Dev", "listsudo", "sudoers"]) & ~BANNED_USERS)
@language
async def sudoers_list(client, message: Message, _):
    text = _["sudo_5"]
    user = await app.get_users(OWNER_ID)
    user = user.first_name if not user.mention else user.mention
    text += f"1➤ {user}\n"
    count = 0
    smex = 0
    for user_id in SUDOERS:
        if user_id != OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += _["sudo_6"]
                count += 1
                text += f"{count}➤ {user}\n"
            except:
                continue
    if not text:
        await message.reply(_["sudo_7"])
    else:
        await message.reply(text, reply_markup=close_markup(_))
