import os
import shutil
from pyrogram import Client, filters
from telegraph import upload_file

TMP_DOWNLOAD_DIRECTORY = "./DOWNLOADS/"

@Client.on_message(
    filters.command("telegraph") 
)
async def telegraph(client, message):
    koshik = await message.reply_text("**Processing...😪**")
    replied = message.reply_to_message
    if not replied:
        await koshik.edit_text("Reply to a supported media file")
        return
    file_info = get_file_id(replied)
    if not file_info:
        await koshik.edit_text("Not supported!")
        return
    _t = os.path.join(
        TMP_DOWNLOAD_DIRECTORY,
        str(replied.message_id)
    )
    if not os.path.isdir(_t):
        os.makedirs(_t)
    _t += "/"
    download_location = await replied.download(
        _t
    )
    try:
        response = upload_file(download_location)
    except Exception as document:
        await koshik.edit_text(message, text=document)
    else:
        await koshik.edit_text(
            f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>\n\n<b>",
            disable_web_page_preview=True
        )
    finally:
        shutil.rmtree(
            _t,
            ignore_errors=True
        )
