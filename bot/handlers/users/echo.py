from loader import db,dp,bot
from aiogram import types
from keyboards.inline.main_menu_super_admin import services_keyboards__board
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"<b>Bo'limni tanlang:</b>",reply_markup=services_keyboards__board())