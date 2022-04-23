# © SpEcHiDe 
import os
import shutil
import subprocess
import time
from info import ADMINS
from plugins.xtra_stuffz_KoshikKumar17.unzipper.utils import progress_for_pyrogram, humanbytes 
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

DLLC = "./DOWNLOADS/UNZIP/"
A = "**STARTING DOWNLOAD**"

Client.on_message(filters.command(["unzip"]))
async def unzip(bot, update):
    if update.from_user.id not in ADMINS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return
    saved_file_path = DLLC + \
        "/" + str(update.from_user.id) + ".unzip.zip"
    if os.path.exists(saved_file_path):
        os.remove(saved_file_path)
    reply_message = update.reply_to_message
    if ((reply_message is not None) and
        (reply_message.document is not None) and
        (reply_message.document.file_name.endswith("zip", "rar"))):
        a = await bot.send_message(
            chat_id=update.chat.id,
            text=A,
            reply_to_message_id=update.message_id
        )
        c_time = time.time()
        try:
            await bot.download_media(
                message=reply_message,
                file_name=saved_file_path,
                progress=progress_for_pyrogram,
                progress_args=(
                    A,
                    a,
                    c_time
                )
            )
        except (ValueError) as e:
            await bot.edit_message_text(
                chat_id=update.chat.id,
                text=str(e),
                message_id=a.message_id
            )
        else:
            await bot.edit_message_text(
                chat_id=update.chat.id,
                text="**Saved File successfully...✅**",
                message_id=a.message_id
            )
            extract_dir_path = DLLC + \
                "/" + str(update.from_user.id) + "zipped" + "/"
            if not os.path.isdir(extract_dir_path):
                os.makedirs(extract_dir_path)
            await bot.edit_message_text(
                chat_id=update.chat.id,
                text="**Analyzing received file. ⚠️ This might take some time. Please be patient.**",
                message_id=a.message_id
            )
            try:
                command_to_exec = [
                    "7z",
                    "e",
                    "-o" + extract_dir_path,
                    saved_file_path
                ]
                # https://stackoverflow.com/a/39629367/4723940
                logger.info(command_to_exec)
                t_response = subprocess.check_output(
                    command_to_exec, stderr=subprocess.STDOUT)
                # https://stackoverflow.com/a/26178369/4723940
            except:
                try:
                    os.remove(saved_file_path)
                    shutil.rmtree(extract_dir_path)
                except:
                    pass
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text="<i>Sorry. Errors occurred while processing compressed file. Please check everything again twice, and if the issue persists, report this to <a href='https://telegram.dog/KoshikKumar'>Click Here</a></i>",
                    disable_web_page_preview=True,
                    parse_mode="html",
                    message_id=a.message_id
                )
            else:
                os.remove(saved_file_path)
                inline_keyboard = []
                zip_file_contents = os.listdir(extract_dir_path)
                i = 0
                for current_file in zip_file_contents:
                    cb_string = "ZIP:{}:ZIP".format(str(i))
                    inline_keyboard.append([
                        InlineKeyboardButton(
                            current_file,
                            callback_data=cb_string.encode("UTF-8")
                        )
                    ])
                    i = i + 1
                cb_string = "ZIP:{}:ZIP".format("ALL")
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "Upload All Files",
                        callback_data=cb_string.encode("UTF-8")
                    )
                ])
                cb_string = "ZIP:{}:ZIP".format("NONE")
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "Cancel",
                        callback_data=cb_string.encode("UTF-8")
                    )
                ])
                reply_markup = InlineKeyboardMarkup(inline_keyboard)
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=Translation.EXTRACT_ZIP_STEP_TWO,
                    message_id=a.message_id,
                    reply_markup=reply_markup,
                )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.EXTRACT_ZIP_INTRO_ONE,
            reply_to_message_id=update.message_id
        )














