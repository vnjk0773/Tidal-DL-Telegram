import tidal_dl
from bot import CMD, LOGGER
from pyrogram import Client, filters
from tidal_dl.util import CONF, TOKEN
from pyrogram.types import CallbackQuery
from bot.helpers.translations import lang
from bot.helpers.utils.auth_check import check_id
from tidal_dl.download import start as tidal_dl_start


@Client.on_message(filters.command(CMD.DOWNLOAD))
async def download_tidal(bot, update):
    if check_id(message=update):
        try:
            if update.reply_to_message:
                link = update.reply_to_message.text
                reply_to_id = update.reply_to_message.message_id
            else:
                link = update.text.split(" ", maxsplit=1)[1]
                reply_to_id = update.message_id
        except:
            link = None
        if link:
            msg = await bot.send_message(
                chat_id=update.chat.id,
                text=lang.INIT_DOWNLOAD,
                reply_to_message_id=update.message_id
            )
            await tidal_dl_start(TOKEN, CONF, link, bot, update.chat.id, reply_to_id)
            await bot.delete_messages(
                chat_id=update.chat.id,
                message_ids=msg.message_id
            )
        else:
            await bot.send_message(
                chat_id=update.chat.id,
                text=lang.ERR_NO_LINK,
                reply_to_message_id=update.message_id
            )

@Client.on_message(filters.command(CMD.AUTH_TIDAL))
def auth_tidal(bot, update):
    if check_id(update.from_user.id, restricted=True):
        chat_id = update.chat.id
        reply_to_id = update.message_id
        tidal_dl.checkLogin(bot, chat_id, reply_to_id, True)

@Client.on_callback_query(filters.regex("z_"))
async def zip_tidal(c: Client, cb: CallbackQuery):
        LOGGER.info("ZIPPING")
        string = cb.data.split("_")[1]
        await tidal_dl_start(TOKEN, CONF, string, c, cb.message.chat.id, cb.message.reply_to_message.message_id, "allowed")

@Client.on_callback_query(filters.regex("t_"))
async def zip_tidal(c: Client, cb: CallbackQuery):
        string = cb.data.split("_")[1]
        await tidal_dl_start(TOKEN, CONF, string, c, cb.message.chat.id, cb.message.reply_to_message.message_id, "not_allowed")

