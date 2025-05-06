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
    with open('data.json', 'r') as file:
        data = json.load(file)
    
    if data['premium_price']['message_id'] and data['premium_price']['from_chat_id']:
        message_id = data['premium_price']['message_id']
        fchat_id = data['premium_price']['from_chat_id']
        try:
            await bot.copy_message(chat_id=message.from_user.id,from_chat_id=fchat_id,message_id=message_id)
        except Exception as e:
            print(e)

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
        
@dp.message_handler(IsUser(),text="To'lovlar tarixi 🧾",state='*')
async def bot_start(message: types.Message):
    await message.reply(text=TARIX, disable_web_page_preview=True)
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
async def check_promocode(promocode,user_id):
    
    with open('promo_codes.json', 'r') as file:
        data = json.load(file)
    if 'promo_codes' in data and promocode in data['promo_codes']:
        users_count = len(data['promo_codes'][promocode]['users'])
        max_count = int(data['promo_codes'][promocode]['count'])
        if promocode in data['promo_codes'] and users_count<max_count and user_id not in data['promo_codes'][promocode]['users']:
            return True
        elif user_id in data['promo_codes'][promocode]['users']:
            return "busy"
        elif users_count>=max_count:
            return 'full'
        else:
            return False
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
    status = await check_promocode(promocode=promocode,user_id=message.from_user.id)
    if status==True:
        try:
            with open('promo_codes.json', 'r') as file:
                data = json.load(file)
                if data['promo_codes'][promocode]['status']=='private':
                    price = int(data['promo_codes'][promocode]['price'])
                    user = await db.select_user(user_id=message.from_user.id)
                    balance= user[0]['balance']
                    data['promo_codes'][promocode].setdefault('users', []).append(message.from_user.id)
                    await db.update_balances(user_id=message.from_user.id,sum=int(balance)+int(price))
                    with open('promo_codes.json','w') as file:
                        json.dump(data,file,indent=4)
                    await message.answer(f"<b>✅PromoCode Muvaffaqiyatli aktivatsiya bo'ldi va Balansingiz {price} so'mga yangilandi.</b>")
                    text = f"Foydalanuvchi: {message.from_user.first_name},<code>{promocode} </code>ni aktivatsiya qildi\n\n"
                    for admin in ADMINS:
                        await bot.send_message(chat_id=admin,text=text)
                    await state.finish()
                else:
                    price = int(data['promo_codes'][promocode]['price'])
                    user = await db.select_user(user_id=message.from_user.id)
                    balance= user[0]['balance']
                    data['promo_codes'][promocode].setdefault('users', []).append(message.from_user.id)
                    await db.update_balances(user_id=message.from_user.id,sum=int(balance)+int(price))
                    with open('promo_codes.json','w') as file:
                        json.dump(data,file,indent=4)
                    with open('promo_codes.json', 'r') as file:
                        data = json.load(file)
                    users_count = len(data['promo_codes'][promocode]['users'])
                    max_count = data['promo_codes'][promocode]['count']
                    bosh_joylar = int(max_count)-int(users_count)
                    text = f"🎟 Promokod:<code> {promocode}</code>\n"
                    text += f"💰 Qiymat: <b>{str(price)}</b>\n"
                    text += f"💰 Foydalanishlar soni: <b>{str(users_count)}</b>\n"
                    text += f"🗂 Bo'sh Joylar soni: <b>{str(bosh_joylar)}</b>\n"
                    await message.answer(f"<b>✅PromoCode Muvaffaqiyatli aktivatsiya bo'ldi va Balansingiz {price} so'mga yangilandi.</b>")
                    markup = InlineKeyboardMarkup(row_width=1)
                    bot_name = await bot.get_me()
                    bot_name = bot_name.username
                    markup.insert(InlineKeyboardButton(text="🤖Botga o'tish",url=f"t.me/{bot_name}"))
                    try:
                        await asyncio.sleep(0.25)
                        with open('promo_codes.json', 'r') as file:
                            promo_data = json.load(file)
                        xabar_id = promo_data['promo_codes'][promocode]['message_id']
                        channel = promo_data['promo_codes'][promocode]['channel']
                        group_text = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> {promocode} promo kodidan foydalandi."
                        
                        try:
                            with open('promo_codes.json', 'r') as file:
                                promo_data = json.load(file)
                            xabar_id = promo_data['promo_codes'][promocode]['message_id']
                            channel = promo_data['promo_codes'][promocode]['channel']
                            await bot.delete_message(chat_id=channel,message_id=xabar_id)
                        except Exception as e:
                            await asyncio.sleep(2)
                            with open('promo_codes.json', 'r') as file:
                                promo_data = json.load(file)
                            xabar_id = promo_data['promo_codes'][promocode]['message_id']
                            channel = promo_data['promo_codes'][promocode]['channel']
                            await bot.delete_message(chat_id=channel,message_id=xabar_id)
                        await asyncio.sleep(1)
                        xabar = await bot.send_message(chat_id=PROMOCODE_CHANNEL,text=text,reply_markup=markup)
                        promo_data['promo_codes'][promocode]['channel'] = PROMOCODE_CHANNEL
                        promo_data['promo_codes'][promocode]['message_id'] = xabar.message_id
                        with open('promo_codes.json','w') as file:  
                            json.dump(promo_data,file,indent=4)
                        try:
                            await bot.send_message(chat_id='@Arelax_gurpasi',text=group_text,reply_markup=markup)
                        except:
                            await asyncio.sleep(1)
                            await bot.send_message(chat_id='@Arelax_gurpasi',text=group_text,reply_markup=markup)
                        await asyncio.sleep(1)
                    except Exception as e:
                        print(e)
                        await bot.delete_message(chat_id=channel,message_id=xabar_id)
                        await asyncio.sleep(1)
                        await bot.send_message(chat_id=ADMINS[0],text=f"Xatolik:116 line,send.py: {e}")
                        await asyncio.sleep(1)

                        xabar = await bot.send_message(chat_id=PROMOCODE_CHANNEL,text=text,reply_markup=markup)
                        promo_data['promo_codes'][promocode]['channel'] = PROMOCODE_CHANNEL
                        promo_data['promo_codes'][promocode]['message_id'] = xabar.message_id
                        with open('promo_codes.json','w') as file:  
                            json.dump(promo_data,file,indent=4)



                    await state.finish()
        except Exception as e:
            await message.answer(f"Xatolik yuz berdi: 59 line send.py:{e}")
            await state.finish()
    elif status=='busy':
        await message.answer(f"<b>❌Siz Allaqachon bu PromoCodedan foydalangansiz.</b>")
        await state.finish()
    elif status=='full':
        await message.answer(f"<b>❌PromoCodeda bo'sh joylar qolmagan!</b>")
        await state.finish()

    elif status=='None PromoCode':
        await message.answer(f"<b>❌Uzur lekin bunday PromoCode mavjuda emas.</b>")
        await state.finish()

    else:
        await message.answer(text="<b>❌Bunday PromoCode Mavjud emas.</b>")
        await state.finish()
    await state.finish()