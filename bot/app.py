from aiogram import executor

from data.config import ADMINS
from loader import dp,db,bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    try:
        await db.create_table_channel()
        await db.create_table_admins()
        await db.create_table_files()
    except Exception as err:
          print(err)
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    try:
        executor.start_polling(dp, on_startup=on_startup)
        dp.middleware.setup()
    except Exception as e:
        print(e)