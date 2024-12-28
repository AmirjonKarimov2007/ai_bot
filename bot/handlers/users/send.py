from datetime import datetime
from datetime import datetime, timedelta
from data.config import ADMINS
from filters.users import IsUser
from filters.admins import IsSuperAdmin
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.menu import *
from loader import dp, db,bot
from keyboards.inline.boglanish_button import get_premium_keyboard,service_keyboard

from loader import db,dp,bot
from aiogram import types
from keyboards.default.menu import *
from filters.users import IsUser



from keyboards.inline.main_menu_super_admin import services_keyboards__board
@dp.message_handler(IsUser(),text='✅Foydalanish',state='*')
async def echo(message: types.Message):
    await message.answer(f"<b>Qaysi Xizmatdan Foydalanmoqchisiz:</b>",reply_markup=services_keyboards__board())


MANUAL = "<b>❓Botda qanday qilib pul ishlayman?</b>\n" \
         "— Botga do'stlaringizni taklif qiling va har bir yangi taklif qilgan do'stlaringiz uchun pullik mukofotlarga ega bo'ling.\n\n" \
         "<b>❓Pulni qanday qilib olish mumkin?</b>\n" \
         "— Botda ishlagan pullaringizni telefon raqamingizga chiqarib olishingiz mumkin. (HUMANS raqamlariga to'lab berilmaydi!)\n\n" \
         "<b>👥 Referal qachon aktiv xolatga o'tadi?</b>\n" \
         "— Siz chaqirgan do'stingiz bizning homiylar kanaliga a'zo bo'lganidan so'ng sizning referalingiz hisoblanadi va sizning balansingizga pul tushadi!\n\n" \
         "<i>✅ To'lovlar soni cheklanmagan, xohlaganingizcha shartlar bajaring va pul ishlang!</i>"

TARIX = "<b>Botimiz haqiqatdan ham to'lab beradi. ✅</b>\n\n<i>Quyidagi kanal orqali to'lovlar tarixini kuzatib borishingiz mumkin👇</i>\nhttps://t.me/+Q6TsT4YXvXplZDUy"
@dp.message_handler(IsUser(),text="💳 Mening Hisobim")
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    id_send = await db.select_user(user_id=user_id)
    if id_send:
        balance = id_send[0]['balance']
        number = id_send[0]['number']
        referred_count = await db.count_referred_users(user_id)
        await message.answer(text=f"<b>💰Hisobingiz: <code>{balance}</code> so'm</b>\n"
                 f"<b>👥Taklif qilgan do'stlaringiz: <code>{referred_count}</code> odam</b>\n"
                 f"<b>📱Hisob raqamingiz: <code>+{number}</code></b>\n",
            reply_markup=get_premium_keyboard,
            parse_mode=types.ParseMode.HTML
        )
    else:
        await message.reply("Foydalanuvchi ma'lumotlari topilmadi.", reply_markup=kb.main())


@dp.callback_query_handler(IsUser(),text='select_service_package')
async def get_premium_func(call: types.CallbackQuery):
    user_id = call.from_user.id
    with open('data.json', 'r') as file:
        data = json.load(file)
    max_balance = data['services']['Referat']
    profile = await db.select_user(user_id=user_id)
    if profile and max_balance:
        user_balance = profile[0]['balance']
        user_balance = int(user_balance)
        max_balance = int(max_balance)
        if user_balance < max_balance:
            await bot.answer_callback_query(call.id, text=f"Xizmatga Pul sarflash uchun hisobingizda kamida {max_balance} so'm bo'lishi kerak!", show_alert=True)
        elif user_balance>=max_balance:
            await call.message.edit_text(text='Xizmatni Tanlang!',reply_markup=service_keyboard(user_balance))
        
            


@dp.message_handler(IsUser(),text="TOP foydalanuvchilar",state='*')
async def top_active_users(message: types.Message):
    top_users = await db.get_top_users()  # DB-dan top 10 foydalanuvchilarni olamiz

    if top_users:
        response = "<b>Botimizning eng faol foydalanuvchilari:</b>\n\n"
        for i, user in enumerate(top_users, 1):
            name = user['name']
            balance = f"{user['balance']:,}".replace(",", " ")  # Balansni chiroyli formatlash
            response += f"<b>{i}) {name}</b>  — <code>{balance}</code> so'm\n"
    else:
        response = "🛑 Hozircha faol foydalanuvchilar mavjud emas."

    await message.reply(response, parse_mode=types.ParseMode.HTML)



@dp.message_handler(IsUser(),text='💸 Xizmat Narxlari')
async def premiumprices(message: types.Message):
    with open('data.json', 'r') as file:
        data = json.load(file)
    
    if data['premium_price']['message_id'] and data['premium_price']['from_chat_id']:
        message_id = data['premium_price']['message_id']
        fchat_id = data['premium_price']['from_chat_id']
        try:
            await bot.copy_message(chat_id=message.from_user.id,from_chat_id=fchat_id,message_id=message_id)
        except Exception as e:
            print(e)

@dp.message_handler(IsUser(),text="Qo'llanma 📄")
async def bot_start(message: types.Message):
    with open('data.json', 'r') as file:
        data = json.load(file) 
    
    if data['get_qollanma']['message_id'] and data['get_qollanma']['from_chat_id']:
        message_id = data['get_qollanma']['message_id']
        chat_id = data['get_qollanma']['from_chat_id']
        try:
            await bot.copy_message(chat_id=message.from_user.id,from_chat_id=chat_id,message_id=message_id,reply_markup=kb.manual())
        except Exception as e:
            print(e)
        
@dp.message_handler(IsUser(),text="To'lovlar tarixi 🧾")
async def bot_start(message: types.Message):
    await message.reply(text=TARIX, disable_web_page_preview=True)
import json

@dp.message_handler(IsUser(),text="👨‍💻 Administrator")
async def admin(message:types.Message):
    with open('data.json', 'r') as file:
        data = json.load(file) 
    if data['administator']['message_id'] and data['administator']['from_chat_id']:
        message_id = data['administator']['message_id']
        chat_id = data['administator']['from_chat_id']
        try:
            await bot.copy_message(chat_id=message.from_user.id,from_chat_id=chat_id,message_id=message_id,reply_markup=kb.manual())
        except Exception as e:
            print(e)

@dp.message_handler(IsUser(),text="🌟 Stars olish")
async def admin(message:types.Message):
    with open('data.json', 'r') as file:
        data = json.load(file) 
    if data['get_stars']['message_id'] and data['get_stars']['from_chat_id']:
        message_id = data['get_stars']['message_id']
        chat_id = data['get_stars']['from_chat_id']
        await bot.copy_message(chat_id=message.from_user.id,from_chat_id=chat_id,message_id=message_id)
