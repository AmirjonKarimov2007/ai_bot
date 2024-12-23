from aiogram import types
from loader import db,dp,bot
from filters.users import IsUser
from filters.admins import IsSuperAdmin
from states.ai_state import PaymentState
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
@dp.message_handler(commands="buy")
async def get_chek(message: types.Message):
    text_1 = """📕Taqdimot/Slayd narxlari:
6 sahifadan, 10 sahifagacha - 4000 so'm
11 sahifadan, 20 sahifagacha - 5000 so'm

📘Mustaqil ish/Referal narxlari:
10 sahifagacha - 4000 so'm
25 sahifagacha - 5000 so'm"""
    await message.answer(text=text_1)
    text_2 = """<b>Iltimos faqat ushbu summalar miqdorida to'lov qiling:</b>
- 2 000 so'm
- 3 000 so'm
- 5 000 so'm
* 10 000 so'm to'lov qilsangiz, +2000 so'm bonus🎁
* 20 000 so'm to'lov qilsangiz, +5000 so'm bonus🎁
* 50 000 so'm to'lov qilsangiz, +15000 so'm bonus🎁

<b><i>Quyidagi karta raqamiga to'lov qiling va chekni skrenshot qilib oling (COPY qilish uchun karta raqam ustiga bosing).</i></b>
<code>5614 6824 1453 1063</code>
<b>Ergashev Sardor |Uzcard</b>

<code>9860 1801 0909 0923</code>
<b>Ergashev Sardor | Humo</b>

"""

    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton(text="📨Chekni yuborish",callback_data=f"payment"),)
    await bot.send_photo(chat_id=message.from_user.id,photo="https://ak.picdn.net/shutterstock/videos/1094038991/thumb/4.jpg",caption=text_2,reply_markup=markup)



@dp.callback_query_handler(IsUser(),text="payment",state='*')
async def chek(call: types.CallbackQuery,state:FSMContext):
    await call.answer(cache_time=1)
    await call.message.answer(text=f"<b>📨To'lov qilganingizni tasdiqlovchi chekni skrenshotini yoki faylini yuboring:</b>")
    await PaymentState.PAYMENT_CHECK.set()
    

import asyncio
from photolink import PhotoLink
from io import BytesIO
import tempfile  
import  os
async def chek_to_link(photo_path):
    photolink = PhotoLink(client_id='lSeA0sSUgd')
    upload = photolink.upload_image(file_path="/home/amirjon/Documents/telegram_Botlar/ai_bot/bot/temp_AgACAgIAAxkBAAKnKWdpgXtZcYv3i9dCvokOGzBvJkoPAAL06jEbC0dQS4MBLEqXgeOnAQADAgADeQADNgQ.jpg")
    
    print(upload)
@dp.message_handler(IsUser(), content_types=types.ContentType.PHOTO, state=PaymentState.PAYMENT_CHECK)
async def jum_jum_jum(message: types.Message):
    # Get the last (highest resolution) photo from the message
    photo = message.photo[-1]
    
    # Download the photo to a temporary file
    file = await message.bot.get_file(photo.file_id)
    photo_path = f"temp_{photo.file_id}.jpg"
    await message.bot.download_file(file.file_path, photo_path)
    
    await chek_to_link(photo_path)
    
    if os.path.exists(photo_path):
        os.remove(photo_path)
    
    await message.answer_photo(photo=photo.file_id)