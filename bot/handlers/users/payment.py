from aiogram import types
from loader import db,dp,bot
from filters.users import IsUser
from filters.admins import IsSuperAdmin
from states.ai_state import PaymentState
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from keyboards.inline.main_keyboard import prices_keybaord
from data.config import ADMINS
import asyncio
from io import BytesIO
import tempfile  
import  os
import uuid



CHANNEL = "-1002659040969"

@dp.callback_query_handler(IsUser(), text="hisobni_toldirish",state='*')
async def get_chek_callback(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.delete()
    text_1 = """📕Taqdimot/Slayd narxlari:
6 sahifadan, 10 sahifagacha - 4000 so'm
11 sahifadan, 20 sahifagacha - 5000 so'm

📘Mustaqil ish/Referal narxlari:
10 sahifagacha - 4000 so'm
25 sahifagacha - 5000 so'm"""
    await call.message.answer(text=text_1)

    text_2 = """<b>Iltimos faqat ushbu summalar miqdorida to'lov qiling:</b>
- 2 000 so'm
- 3 000 so'm
- 5 000 so'm
* 10 000 so'm to'lov qilsangiz, +2000 so'm bonus🎁
* 20 000 so'm to'lov qilsangiz, +5000 so'm bonus🎁
* 50 000 so'm to'lov qilsangiz, +15000 so'm bonus🎁

<b><i>Quyidagi karta raqamiga to'lov qiling va chekni skrenshot qilib oling (COPY qilish uchun karta raqam ustiga bosing).</i></b>
<code>9860 0801 5186 6938</code>
<b>Amirjon Karimov |Humo</b>
"""
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton(text="📨Chekni yuborish", callback_data="payment"))
    await call.message.answer_photo(
        photo="https://ak.picdn.net/shutterstock/videos/1094038991/thumb/4.jpg",
        caption=text_2,
        reply_markup=markup
    )
@dp.message_handler(IsUser(),commands="buy")
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
<code>9860 0801 5186 6938</code>
<b>Amirjon Karimov |Humo</b>
"""

    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton(text="📨Chekni yuborish",callback_data=f"payment"),)
    await bot.send_photo(chat_id=message.from_user.id,photo="https://ak.picdn.net/shutterstock/videos/1094038991/thumb/4.jpg",caption=text_2,reply_markup=markup)


@dp.message_handler(IsUser(),commands="chek",state='*')
async def cheklar(message: types.Message,state:FSMContext):

    await message.answer(text=f"<b>📨To'lov qilganingizni tasdiqlovchi chekni skrenshotini yoki faylini yuboring:</b>")
    await PaymentState.PAYMENT_CHECK.set()
@dp.callback_query_handler(IsUser(),text="payment",state='*')
async def chek(call: types.CallbackQuery,state:FSMContext):
    await call.answer(cache_time=1)
    await call.message.answer(text=f"<b>📨To'lov qilganingizni tasdiqlovchi chekni skrenshotini yoki faylini yuboring:</b>")
    await PaymentState.PAYMENT_CHECK.set()
    

#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE
#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE
#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE
#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE
#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE#  CAPTION TO IMAGE

async def send_user_info(message,photo,summa:str,invoice):
    user = await db.select_user(user_id=message.from_user.id)
    phone_number = user[0]['number']
    balance = user[0]['balance']
    
    caption = f"<b>Xurmatli Admin sizga yangi to'lov mavjud.</b>\n\n"
    caption +=f"<b>👤Foydalanuvchi:<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a></b>\n"
    caption +=f"<b>👥Username: @{message.from_user.username} \n</b>"
    caption +=f"<b>🪪Telegram ID:<code>{message.from_user.id}</code>\n</b>"
    caption +=f"<b>☎️Telefon Raqam:{phone_number}\n</b>"
    caption +=f"<b>💸Foydalanuvchining Hozirgi Balansi:{balance}\n</b>"
    caption +=f"<b>💳Chek Summasi:{summa}\n</b>"
    caption +=f"<b>🆔chek ID: <code>{photo}</code>\n\n</b>"
    caption +=f"<b>📔Invoice: <code>{invoice}</code>\n\n</b>"
    caption +=f"#chek_{message.from_user.id}"
    return caption
# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE
# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE
# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE
# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE# END CAPTION TO IMAGE



@dp.message_handler(IsUser(), content_types=types.ContentType.PHOTO, state=PaymentState.PAYMENT_CHECK)
async def jum_jum_jum(message: types.Message,state: FSMContext):
    photo = message.photo[-1].file_id
    text = f"❓Qancha to'lov qildingiz? To'lov summangizni tanlang\n👇"
    markup = prices_keybaord()
    await bot.send_photo(chat_id=message.from_user.id,photo=photo,caption=text,reply_markup=markup)
    await state.finish()


# Invoice GENERATOR # Invoice GENERATOR# Invoice GENERATOR# Invoice GENERATOR# Invoice GENERATOR
# Invoice GENERATOR # Invoice GENERATOR# Invoice GENERATOR# Invoice GENERATOR# Invoice GENERATOR
# Invoice GENERATOR # Invoice GENERATOR# Invoice GENERATOR# Invoice GENERATOR# Invoice GENERATOR
# Invoice GENERATOR # Invoice GENERATOR# Invoice GENERATOR# Invoice GENERATOR# Invoice GENERATOR

generated_codes = set()

def generate_unique_invoice(length=12):
    while True:
        promo_code = str(uuid.uuid4()).replace("-", "")[:length]  
        promo_code = promo_code.upper()  
        if promo_code not in generated_codes:
            generated_codes.add(promo_code)  
            return promo_code
        else:
            continue

# promo_code = generate_unique_promo_code(length=8)


# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR
# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR
# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR
# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR# END INVOICE GENERATOR




# Client chek yuboriish qismi
@dp.callback_query_handler(IsUser(),text_contains="select_user_payment:",state='*')
async def select_user_payment_handler(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    photo = call.message.photo[-1].file_id

    data = call.data.rsplit(":")
    price = data[1]
    invoice = generate_unique_invoice(length=12)

    caption_text = await send_user_info(call,photo,price,invoice)

    text=f"<b>To'lovingiz:{price}</b>\n\n"
    text+=f"<b>⏳Biroz kuting adminlar sizning chekingizni ko'rib chiqadi va agar to'g'ri to'lov cheki bo'lsa balansingizga pul tushiriladi. Bot avtomatik bu haqida sizga xabar beradi.</b>"
    text+=f"\n\n<i>Sizning invoice raqamingiz:</i><code>{invoice}</code>"

    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton(text=f"✅Qabul Qilish",callback_data=f"checked_payment:{call.from_user.id}:{price}:{invoice}"))
    markup.insert(InlineKeyboardButton(text=f"❌Bekor qilish",callback_data=f"calceled_payment:{call.from_user.id}:{price}:{invoice}"))
    try:
        await call.message.edit_caption(caption=f"{text}")
        await bot.send_photo(photo=photo,chat_id=CHANNEL,caption=caption_text,reply_markup=markup)
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0],text=f"To'lov qisminida xatolik yuz berdi:{e}")
        await call.message.edit_caption(f"To'lovingiz Qabul qilinmadi.Admin bilan aloga chiqing.")
# /// Client chek yuboriish qismi///# /// Client chek yuboriish qismi///# /// Client chek yuboriish qismi///# /// Client chek yuboriish qismi///
import pytz
import datetime

@dp.callback_query_handler(IsSuperAdmin(),text_contains="checked_payment:",state='*')
async def tasdiqlangan_tolov(call: types.CallbackQuery):
    
    data = call.data.rsplit(":")
    user_id = data[1]
    user_price = data[2]
    invoice = data[3]
    photo = call.message.photo[-1].file_id
    uzbekistan_tz = pytz.timezone('Asia/Tashkent')
    datas = datetime.datetime.now(uzbekistan_tz)
    try:
        if await db.select_payment(invoice=invoice):
            await call.answer("❌Siz bu invoysni tasdiqlagansiz...",show_alert=True)
        else:
            
            user = await db.select_user(user_id=int(user_id))
            name = user[0]['name']
            username = user[0]['username']
            number = user[0]['number']
            await db.add_payment(name=name,username=username,user_id=int(user_id),file_id=photo,summa=int(user_price),
                                    number=int(number),created_date=datas,updated_date=datas,invoice=invoice)
            await db.update_balance(user_id=int(user_id),sum=int(user_price))
            await call.answer("✅Foydalanuvchining balansini yangiladingiz?",show_alert=True)
            user = await db.select_user(user_id=int(call.from_user.id))
            balance = user[0]['balance']
            text = f"✅ To'lovingiz qabul qilindi.\n"
            text += f"Balansingiz {user_price}ga to'ldirildi.\n"
            text += f"Balansingiz:{balance}\n"
            await bot.send_photo(chat_id=int(user_id),photo=photo,caption=text)
            await call.message.edit_reply_markup()
            photo_caption = call.message.caption
            if "📊Status: ✅Taqdiqlangan" not in photo_caption:
                photo_caption += "\n📊Status: ✅Taqdiqlangan"
                await call.message.edit_caption(caption=photo_caption)
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0],text=f"To'lov qisminida xatolik yuz berdi:{e}")

# Cenceled payment handlerlar
@dp.callback_query_handler(IsSuperAdmin(),text_contains="calceled_payment:",state='*')
async def atmen_qilingan_tolov(call: types.CallbackQuery):
    await call.answer(f"✅Invoys Muvaffaqiatli Bekor qilindi qilindi",show_alert=True)
    data = call.data.rsplit(":")
    user_id = data[1]
    user_price = data[2]
    invoice = data[3]
    photo = call.message.photo[-1].file_id
    uzbekistan_tz = pytz.timezone('Asia/Tashkent')
    datas = datetime.datetime.now(uzbekistan_tz)
    try:
        if await db.select_payment(invoice=invoice):
            await call.answer("❌Invoys Bazadan topildi,balansni qo'lda yangilang.",show_alert=True)
        else:
            user = await db.select_user(user_id=int(user_id))
            name = user[0]['name']
            username = user[0]['username']
            number = user[0]['number']
            text = f"💸Summa: {user_price} so'm\n"
            text+=f"🚫To'lovingiz rad etildi.\n\n"
            text+=f"🆘Sababi\n:"
            text+=f"Siz yuborgan rasmda to'lov ma'lumotlari yo'q\n"
            text+=f"Agar shikoyatingiz bo'lsa admin( @Amirjon_Karimov) bilan bog'laning!\n"
                        
            await bot.send_photo(chat_id=int(user_id),photo=photo,caption=text)
            caption = call.message.caption
            caption +="\n📊Status: ❌Bekor qilingan"
            await call.message.edit_reply_markup()
            await call.message.edit_caption(caption=caption)
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0],text=f"To'lov qisminida xatolik yuz berdi:{e}")




@dp.callback_query_handler(IsUser(),text="cancel_payment",state='*')
async def cancel_payment_handler(call: types.CallbackQuery,state:FSMContext):
    await call.message.delete()
    try:
        await call.message.answer("<b>❌To'lov qilish uchun arizangiz bekor qilindi.</b>")
        await state.finish()
    except:
        await call.message.answer("<b>❌o'lov qilish uchun arizangiz bekor qilindi.</b>")
        await state.finish()