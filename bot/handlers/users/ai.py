from data.config import ADMINS
from loader import db,dp,bot
from aiogram import types
from filters.users import IsUser
from filters.admins import IsSuperAdmin
import json
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from states.ai_state import ServicesStates
from keyboards.inline.main_menu_super_admin import services_keyboards__board
from aiogram.types import ContentTypes
from utils.ai_api import get_response_from_server
from keyboards.inline.main_keyboard import success_keyboards



async def text_generator(type,user_id):
    with open('user_info.json','r') as file:
        data = json.load(file)
        mavzu = data[str(user_id)]['mavzu']
        min = data[str(user_id)]['min']
        max = data[str(user_id)]['max']
        user = await db.select_user(user_id=int(user_id))
        name = user[0]['author']
        univer = user[0]['univer']
        language = user[0]['language']
        caption = f"🌟Ajoyib, quyidagi ma'lumotlarni tekshiring\n\n"
        caption += f"<b>«{type}»</b>\n\n"
        caption += f"📃Mavzu: <b>{mavzu}</b>\n"
        caption += f"🏫Institut va kafedra: <b>{univer}</b>\n"
        caption += f"👤Muallif: <b>{name}</b>\n"
        caption += f"📰Sahifalar soni: <b>{min}dan – {max}gacha</b>\n"
        caption += f"👅Tili: <b>{language}</b>\n\n"

    return caption



@dp.callback_query_handler(IsUser(),text_contains='select_service:',state='*')
async def select_service(call: types.CallbackQuery):
    info =  call.data.rsplit(":")
    service = info[1]
    with open ('data.json','r') as f:
        data = json.load(f)
    service_price = data['services'][service]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="⬅️Orqaga",callback_data="back_to_service_menu"))
    await call.message.edit_text(text=f"<b>Sizdan so'ragalgan malumotlarni aniq va bexato yuborishga harakart qiling.\n\n{service} qaysi mavzu nomi ostiga tayyorlanishi kerak.</b>",reply_markup=markup)
    if service == "Referat":
        await ServicesStates.Referat.set()
    elif service == "Mustaqil ish":
        await ServicesStates.Mustaqil.set()
    elif service == "Slaydlar":
        await ServicesStates.Slaydlar.set()
    elif service == "Insho":
        await ServicesStates.Insho.set()
    elif service == "Tabrik":
        await ServicesStates.Tabrik.set()
    elif service == "Bayon":
        await ServicesStates.Bayon.set()  
        

async def check_info(user_id):
    user = await db.is_user(user_id=int(user_id))
    user_info = user[0]
    if user_info['author'] and user_info['language'] and user_info['univer']:
        return True
    elif not user_info['author']:
        return False
    elif not user_info['language']:
        return False
    elif not user_info['univer']:
        return False

import os






@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Referat)
async def handle_referal_message(message: types.Message, state: FSMContext):
    service = "REFERAT"
    markup = success_keyboards(service)
    mavzu = message.text
    user_id = str(message.from_user.id)  
    if os.path.exists('user_info.json'):
        with open('user_info.json', "r", encoding="utf-8") as file:
            user_info = json.load(file)
    else:
        user_info = {}
    if user_id in user_info and "min" in user_info[user_id] and "max" in user_info[user_id]:
        user_info[user_id]["mavzu"]=mavzu
    else:
        user_info[user_id] = {
            "mavzu": mavzu,
            "min": 5,  
            "max": 10 
        }

    with open('user_info.json', "w", encoding="utf-8") as file:
        json.dump(user_info, file, indent=4, ensure_ascii=False)

    try:
        status = await check_info(user_id=message.from_user.id)
    
        if status==True:
            caption = await text_generator(
                type=service,
                user_id=message.from_user.id,
            )
            caption += f"• Ma'lumotlar to'g'ri bo'lsa, '✅Tayyorlash'\n"
            caption += f"• Biror ma'lumotni o'zgartirish uchun, '✏️O'zgartirish'.\n"
            caption += f"• Bekor qilish uchun, '🚫Rad qilish'."
            await message.answer(text=caption,reply_markup=markup)
            await state.finish()
        else:
            text = """Institut va kafedrangizni(majburiy emas) to'liq kiriting.
📋Namuna: FARG‘ONA DAVLAT UNIVERSITETI IQTISODIYOT KAFEDRASI"""
            await message.answer(text=f"<b>{text}</b>")
            await ServicesStates.Referat_AUTHOR_NAME.set()
    except Exception as e:
        await state.finish()
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:52:error:{e}")





# Register Jarayoni
@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Referat_AUTHOR_NAME)
async def handle_referal_author__message(message: types.Message, state: FSMContext):
    univer = message.text
    text = """Muallif ism-familiyasi, guruhi va hokazolarni to'liq kiriting.

📋Namuna: Isroilov Ismoiljon Muhiddin o'g'li, 4-kurs, 21.36-guruh"""
    service = "REFERAT"
    markup = success_keyboards(service)
    try:
        await db.update_user_univer(univer=univer,user_id=int(message.from_user.id))
        status = await check_info(user_id=message.from_user.id)
    
        if status==True:
            caption = await text_generator(
                type=service,
                user_id=message.from_user.id,
            )
            caption += f"• Ma'lumotlar to'g'ri bo'lsa, '✅Tayyorlash'\n"
            caption += f"• Biror ma'lumotni o'zgartirish uchun, '✏️O'zgartirish'.\n"
            caption += f"• Bekor qilish uchun, '🚫Rad qilish'."
            await message.answer(text=caption,reply_markup=markup)
            await state.finish()
        else:
            await message.answer(f"<b>{text}</b>")
            await ServicesStates.SUCCESS_SERVICE.set()
    except Exception as e:
        await state.finish()
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:137:error:{e}")

@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.SUCCESS_SERVICE)
async def handle_referal_author_NAME_message(message: types.Message, state: FSMContext):
    author = message.text
    service = "REFERAT"
    markup = success_keyboards(service)
    try:
        await db.update_user_author(author=author,user_id=int(message.from_user.id))
        status = await check_info(user_id=message.from_user.id)
    
        if status==True:
            caption = await text_generator(
                type=service,
                user_id=message.from_user.id,
            )
            caption += f"• Ma'lumotlar to'g'ri bo'lsa, '✅Tayyorlash'\n"
            caption += f"• Biror ma'lumotni o'zgartirish uchun, '✏️O'zgartirish'.\n"
            caption += f"• Bekor qilish uchun, '🚫Rad qilish'."
            await message.answer(text=caption,reply_markup=markup)
            await state.finish()
        else:
            print('salom')
    except Exception as e:
        await state.finish()
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:70:error:{e}")














@dp.callback_query_handler(IsUser(),text_contains="cancel:")
async def referal_cancel(call: types.CallbackQuery):
    data = call.data.rsplit(":")
    service = data[1]
    text = f"""Referat bekor qilindi.
Yangi {service} yaratish uchun quyidagi ✅Foydalanish tugmasini bosing!"""
    await call.message.edit_text(text=f"<b>{text}</b>")


from keyboards.inline.main_keyboard import editable_keyboards
@dp.callback_query_handler(IsUser(),text_contains="edit:",state='*')
async def referal_cancel(call: types.CallbackQuery):
    data = call.data.rsplit(":")
    service = data[1]
    caption = await text_generator(type=f"{service}",user_id=call.from_user.id)
    caption += "<b>Nimani o'zgartirmoqchisiz❓ Quyidagilardan birini tanlang👇</b>"
    markup = editable_keyboards(service=service)
    await call.message.edit_text(text=caption,reply_markup=markup)




@dp.callback_query_handler(IsUser(),text="back_to_REFERAT",state='*')
async def handle_referal_success_message(call: types.CallbackQuery):
    service = "REFERAT"
    markup = success_keyboards(service)
    try:
        status = await check_info(user_id=call.from_user.id)
        if status==True:
            caption = await text_generator(
                type=service,
                user_id=call.from_user.id,
            )
            caption += f"• Ma'lumotlar to'g'ri bo'lsa, '✅Tayyorlash'\n"
            caption += f"• Biror ma'lumotni o'zgartirish uchun, '✏️O'zgartirish'.\n"
            caption += f"• Bekor qilish uchun, '🚫Rad qilish'."
            await call.message.edit_text(text=caption,reply_markup=markup)
        else:
            print('salom')
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:70:error:{e}")

# Sun'iy intelekt qismi.
# Sun'iy intelekt qismi.
# Sun'iy intelekt qismi.
# Sun'iy intelekt qismi.
# Sun'iy intelekt qismi.
# Sun'iy intelekt qismi.
# Sun'iy intelekt qismi.


import json
import re
import asyncio
import pytz
import datetime
from aiogram import types
from aiogram.types import InputFile
from docx_generator import word_generator
uzbekistan_tz = pytz.timezone('Asia/Tashkent')


@dp.callback_query_handler(IsUser(), text_contains="success:", state="*")
async def success_handler(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await gg_generate(call=call)


async def gg_generate(call: types.CallbackQuery):
    time = datetime.datetime.now(uzbekistan_tz)
    message_text = call.message.text
    topic_line = next((line for line in message_text.split('\n') if line.startswith("📃Mavzu:")), "")
    page_range_line = next((line for line in message_text.split('\n') if line.startswith("📰Sahifalar soni:")), "")
    page_numbers = re.search(r'(\d+dan)\s*–\s*(\d+gacha)', page_range_line)
    max_pages = page_numbers.group(2).replace('gacha', '')
    topic = topic_line.split(":", 1)[-1].strip() if topic_line else "Unknown"
    
    print(f"Start: {time.hour}:{time.minute}:{time.second}")

    user_id = call.from_user.id
    data = call.data.split(":")
    service = data[1]
    mavzu = topic
    max_pages = int(max_pages)

    page_count = {"10": 0, "15": 2, "20": 3, "25": 4}

    # Fetch user from database
    user = await db.select_user(user_id=user_id)
    if not user:
        await call.message.answer("Foydalanuvchi ma'lumotlari topilmadi.")
        return

    language = user[0].get('language', "")
    univer = user[0].get('univer', "")
    author = user[0].get('author', "")

    with open("ai_history.json", "r") as f:
        ai_history = json.load(f)

    if str(user_id) not in ai_history:
        ai_history[str(user_id)] = {}
    with open("ai_history.json", "w") as f:
        json.dump(ai_history, f, indent=4)

    msg = await call.message.edit_text("⏳")

    # Generate themes
    theme_data = [
        {
            "role": "user",
            "content": (
                f"Men seni telegram botga ulaganman. Ortiqcha hech narsa demasdan faqat quyidagi promptni bajar: "
                f"{mavzu} mavzusi bo'yicha {service} uchun 3 ta mavzu yozib ber, {language} tilida. "
                "Albatta, bajaraman degan so'zlarni yozishing shart emas."
            )
        }
    ]

    response = await get_response_from_server(history=theme_data)
    themes = response.get('response', "").split('\n')

    tasks = []

    for theme in themes:
        tasks.append(generate_text_for_theme(user_id, theme, language, page_count, max_pages, ai_history))

    await asyncio.gather(*tasks)

    

    file_stream = await word_generator(
        type=service,
        mavzu=mavzu,
        univer=univer,
        name=author,
        rejalar=themes,
        theme_text=ai_history[str(user_id)],
        user_id=str(user_id)
    )
    ai_history[str(user_id)]={}
    with open("ai_history.json", "w") as f:
        json.dump(ai_history, f, indent=4)


    await bot.send_chat_action(user_id, "upload_document")
    await asyncio.sleep(0.5)

    await msg.delete()
    await call.message.answer_document(InputFile(file_stream, filename=f"{mavzu}.docx"))

    ai_history[str(user_id)] = {}
    with open("ai_history.json", "w") as f:
        json.dump(ai_history, f, indent=4)

    time = datetime.datetime.now(uzbekistan_tz)
    print(f"End: {time.hour}:{time.minute}:{time.second}")


async def generate_text_for_theme(user_id, theme, language, page_count, max_pages, ai_history):
    # Agar theme lug‘atda mavjud bo‘lmasa, uni bo‘sh qiymat bilan boshlash
    if theme not in ai_history[str(user_id)]:
        ai_history[str(user_id)][theme] = ""

    if page_count[str(max_pages)] == 0:
        history = [
            {
                "role": "system",
                "content": (
                    f"Men seni telegram botga ulaganman. {theme} mavzusida matn kerak. "
                    f"{language} tilida. Matning 500 so'zdan oshmasin. "
                    "Faqat kerakli matnlarni yubor."
                )
            }
        ]
        response = await get_response_from_server(history=history)
        ai_history[str(user_id)][theme] += response['response']
    else:
        

        for _ in range(page_count[str(max_pages)]):
            previous_text = ai_history[str(user_id)].get(theme, "")
            history = [
                {
                    "role": "system",
                    "content": (
                        f"Men seni telegram botga ulaganman. {theme} mavzusida matn kerak. "
                        f"{language} tilida. Matning 700 so'zdan oshmasin. "
                        f"Bu oldingi matning: {previous_text}. Yangi, farqli matn yozib ber."
                    )
                }
            ]
            response = await get_response_from_server(history=history)
            ai_history[str(user_id)][theme] += response['response']
            with open("ai_history.json", "w") as f:
                json.dump(ai_history, f, indent=4)






@dp.callback_query_handler(IsUser(), text="back_to_service_menu", state="*")
async def back_to_main_menu_method(call: types.CallbackQuery,state: FSMContext):
    await call.answer(cache_time=1)
    if call.message.text != "Qaysi Xizmatdan Foydalanmoqchisiz:":
        await call.message.edit_text(text="<b>Qaysi Xizmatdan Foydalanmoqchisiz:</b>", reply_markup=services_keyboards__board())
    else:
        await call.message.edit_text(text="<b>Qaysi Xizmatdan Foydalanmoqchisiz?</b>", reply_markup=services_keyboards__board())
    await state.finish()