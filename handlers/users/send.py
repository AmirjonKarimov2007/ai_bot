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



@dp.message_handler(IsUser(),text="💳 Mening Hisobim",state='*')
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


# @dp.callback_query_handler(IsUser(),text='select_service_package')
# async def get_premium_func(call: types.CallbackQuery):
#     user_id = call.from_user.id
#     with open('data.json', 'r') as file:
#         data = json.load(file)
#     max_balance = data['services']['Referat']
#     profile = await db.select_user(user_id=user_id)
#     if profile and max_balance:
#         user_balance = profile[0]['balance']
#         user_balance = int(user_balance)
#         max_balance = int(max_balance)
#         if user_balance < max_balance:
#             await bot.answer_callback_query(call.id, text=f"Xizmatga Pul sarflash uchun hisobingizda kamida {max_balance} so'm bo'lishi kerak!", show_alert=True)
#         elif user_balance>=max_balance:
#             await call.message.edit_text(text='Xizmatni Tanlang!',reply_markup=service_keyboard(user_balance))
        
            


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



@dp.message_handler(IsUser(),text='💸 Xizmat Narxlari',state='*')
async def premiumprices(message: types.Message):
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    services = data['services']
    text = "🔥 <b>Bilimli Talabalar Xizmatlari</b> 🔥\n\n"
    text += "✅ Ishonchli | 📚 Sifatli | ⏱ Tezkor\n"
    text += "Siz uchun eng yaxshi narxlarda mustaqil ish, referat, insho va boshqa yozma ishlar tayyorlab beramiz.\n\n"
    text += "📌 <b>Xizmatlar narxlari:</b>\n\n"

    for service_name, prices in services.items():
        text += f"🔹 <b>{service_name}</b>\n"
        for page_count, price in prices.items():
            price_str = f"{int(price):,}" if isinstance(price, (int, float, str)) and str(price).isdigit() else price
            text += f"   {page_count} bet — {price_str} so'm\n"
        text += "\n"

    text += "💡 <b>Nega aynan biz?</b>\n"
    text += "• Har bir ish plagiatsiyasiz yoziladi\n"
    text += "• Tajribali AI va mutaxassislar tomonidan tayyorlanadi\n"
    text += "• Har doim sizning talab va formatlaringizga mos\n\n"
    text += "🎯 Bugunoq buyurtma bering va o'qishda yengillik yarating!\n"
    text += "<i>Savollar uchun shunchaki yozing – javob berishga tayyormiz!</i> 💬"

    await message.answer(text,reply_markup=services_keyboards__board())

@dp.message_handler(text="Qollanma 📄",state='*')
async def bot_start_qollanma(message: types.Message):
    with open('data.json', 'r') as file:
        data = json.load(file) 
    
    if data['get_qollanma']['message_id'] and data['get_qollanma']['from_chat_id']:
        message_id = data['get_qollanma']['message_id']
        chat_id = data['get_qollanma']['from_chat_id']
        try:
            await bot.copy_message(chat_id=message.from_user.id,from_chat_id=chat_id,message_id=message_id)
        except Exception as e:
            print(e)


import json

@dp.message_handler(IsUser(),text="👨‍💻 Administrator",state='*')
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





# PromoCode olish
from data.config import PROMOCODE_CHANNEL
from states.admin_state import SuperAdminState
from aiogram.dispatcher import FSMContext

# PROMOCode PROMOCODE PROMOCODE PROMOCODE PROMOCODE PROMOCODE
# PROMOCode PROMOCODE PROMOCODE PROMOCODE PROMOCODE PROMOCODE
# PROMOCode PROMOCODE PROMOCODE PROMOCODE PROMOCODE PROMOCODE
# PROMOCode PROMOCODE PROMOCODE PROMOCODE PROMOCODE PROMOCODE
from aiogram.types import *
import asyncio
from utils.promocode_api import promocode_service

async def check_promocode(promocode,user_id):
    promoCodes = promocode_service.get_all_promcodes()
    promocode_id = None
    for promo in promoCodes:
        if promo['code']==promocode:
            promocode_id = promo['id']
            userCheck = promocode_service.is_user_activate_promocode(promocode_id=promocode_id,user_id=user_id)
            if userCheck==False:
                return 'busy'
            else:
                users_count = len(userCheck[1])
                promocode_data = promocode_service.get_promocode(promocode_id)
                if promocode_data['is_active']==True:
                    users_max_count = promocode_data['used_count']
                    if users_count<users_max_count:
                        start_date = promocode_data['start_date']
                        end_date = promocode_data['end_date']
                        end_date = datetime.fromisoformat(end_date)
                        today = datetime.now(end_date.tzinfo)
                        if today > end_date:
                            return 'ended'
                        else:
                            return promocode_id

                    else:
                        return 'full'
                else:
                    return False



    
   
    
@dp.message_handler(IsUser(),text="🔑Promo Kod",state='*')
async def get_promocode(message: types.Message):
    try:
        await message.answer("<b>Iltimos sizga berilgan promocodeni kiriting.</b>")
        await SuperAdminState.GET_PROMOCODE.set()
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0],text="Botda xatolik yuz berdi:60 line,send.py")

@dp.message_handler(IsUser(),content_types=types.ContentType.TEXT,state=SuperAdminState.GET_PROMOCODE)
async def promocode(message: types.Message,state: FSMContext):
    
    promocode = message.text
    user = await db.select_user(user_id=message.from_user.id)

    status = await check_promocode(promocode=promocode,user_id=user[0]['id'])
    
    if isinstance(status, (int, float)):
        try:
            promocode_id =status
            promocode_data = promocode_service.get_promocode(promocode_id)
            if promocode_data['status']=='private':
                price = promocode_data['price']
               
                user = await db.select_user(user_id=message.from_user.id)
                balance= user[0]['balance']

                await db.update_balances(user_id=message.from_user.id,sum=int(balance)+int(price))

                promocode_service.create_promocode_usage(user_id=user[0]['id'],promocode_id=promocode_id)
                await message.answer(f"<b>✅PromoCode Muvaffaqiyatli aktivatsiya bo'ldi va Balansingiz {price} so'mga yangilandi.</b>")
                text = f"Foydalanuvchi: {message.from_user.first_name},<code>{promocode} </code>ni aktivatsiya qildi\n\n"
                for admin in ADMINS:
                    await bot.send_message(chat_id=admin,text=text)
                await state.finish()
            else:
                price = promocode_data['price']
                user = await db.select_user(user_id=message.from_user.id)
                balance= user[0]['balance']
                promocode_service.create_promocode_usage(user_id=user[0]['id'],promocode_id=promocode_id)
                await db.update_balances(user_id=message.from_user.id,sum=int(balance)+int(price))
                userCheck = promocode_service.get_promocode_activated_users(promocode_id=promocode_id)
                users_count = len(userCheck)
                max_count = promocode_data['used_count']
                bosh_joylar = int(max_count)-int(users_count)
                text = f"🎟 Promokod:<code> {promocode}</code>\n"
                text += f"💰 Qiymat: <b>{str(price)}</b>\n"
                text += f"💰 Foydalanishlar soni: <b>{str(users_count)}</b>\n"
                text += f"🗂 Bo'sh Joylar soni: <b>{str(bosh_joylar)}</b>\n"
                text += f"Foydalanuvchi: {message.from_user.first_name}\nUsername: @{message.from_user.username}\nID: {message.from_user.id}"
                await message.answer(f"<b>✅PromoCode Muvaffaqiyatli aktivatsiya bo'ldi va Balansingiz {price} so'mga yangilandi.</b>")
                markup = InlineKeyboardMarkup(row_width=1)
                bot_name = await bot.get_me()
                bot_name = bot_name.username
                markup.insert(InlineKeyboardButton(text="🤖Botga o'tish",url=f"t.me/{bot_name}"))
                try:
                    for admin in ADMINS:
                        await bot.send_message(chat_id=admin,text=text)
                    await state.finish()
                except Exception as e:
                    
                    await state.finish()
                finally:
                    state.finish()
        except Exception as e:
            await message.answer(f"Xatolik yuz berdi: 59 line send.py:{e}")
            await state.finish()
    elif status=='busy':
        await message.answer(f"<b>❌Siz Allaqachon bu PromoCodedan foydalangansiz.</b>")
        await state.finish()
    elif status=='full':
        await message.answer(f"<b>❌PromoCodeda bo'sh joylar qolmagan!</b>")
        await state.finish()
    elif status=='ended':
        await message.answer(f"<b>❌PromoCode Muddati tugagan!</b>")
        await state.finish()

    elif status=='None PromoCode':
        await message.answer(f"<b>❌Uzur lekin bunday PromoCode mavjuda emas.</b>")
        await state.finish()

    else:
        await message.answer(text="<b>❌Bunday PromoCode Mavjud emas.</b>")
        await state.finish()
    await state.finish()