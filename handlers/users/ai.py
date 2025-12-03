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
import os
import json
import re
import asyncio
import pytz
import datetime
from aiogram import types
from aiogram.types import InputFile
from docx_generator import word_generator
uzbekistan_tz = pytz.timezone('Asia/Tashkent')
from keyboards.inline.boglanish_button import get_premium_keyboard



async def text_generator(type,user_id,ai=False):
    with open('user_info.json','r',encoding='utf-8') as file:
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
    caption += f"Rejalar:👇👇👇\n"

    if ai:
        themes = await themeCreator(mavzu=mavzu,service=type,language=language)
        data[str(user_id)]['rejalar'] = themes
        with open('user_info.json', "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        themes.join('\n')
        caption+=themes
    else:
        themes = data[str(user_id)]['rejalar']
        themes.join('\n')

        caption+=themes
    return f"{caption}\n\n"

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
    elif service == "Mustaqil Ish":
        await ServicesStates.Mustaqil.set()
    elif service == "Slaydlar":
        await ServicesStates.Slaydlar.set()
    elif service == "Insho":
        await ServicesStates.Insho.set()
    elif service == "Tabrik":
        await ServicesStates.Tabrik.set()
    elif service == "Bayon":
        await ServicesStates.Bayon.set()  
        
# Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish
# Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish
# Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish
# Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish
# Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish Mustaqil Ish



@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Mustaqil)
async def handle_mustaqil_message(message: types.Message, state: FSMContext):
    timeicon = await message.answer("⏳")
    service = "MUSTAQIL ISH"
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
                ai=True

            )
            caption += f"• Ma'lumotlar to'g'ri bo'lsa, '✅Tayyorlash'\n"
            caption += f"• Biror ma'lumotni o'zgartirish uchun, '✏️O'zgartirish'.\n"
            caption += f"• Bekor qilish uchun, '🚫Rad qilish'."
            await timeicon.delete()
            await message.answer(text=caption,reply_markup=markup)
            await state.finish()
        else:
            text = """Institut va kafedrangizni(majburiy emas) to'liq kiriting.
📋Namuna: FARG‘ONA DAVLAT UNIVERSITETI IQTISODIYOT KAFEDRASI"""
            await message.answer(text=f"<b>{text}</b>")
            await ServicesStates.Mustaqil_AUTHOR_NAME.set()
    except Exception as e:
        await state.finish()
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:52:error:{e}")


@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Mustaqil_AUTHOR_NAME)
async def handle_mustaqil_author__message(message: types.Message, state: FSMContext):
    univer = message.text
    text = """Muallif ism-familiyasi, guruhi va hokazolarni to'liq kiriting.

📋Namuna: Isroilov Ismoiljon Muhiddin o'g'li, 4-kurs, 21.36-guruh"""
    service = "MUSTAQIL ISH"
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
async def handle_mustaqil_author_NAME_message(message: types.Message, state: FSMContext):
    author = message.text
    service = "MUSTAQIL ISH"
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
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:209:error:{e}")


# Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi....
# Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi....
# Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi....
# Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi....
# Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi....
# Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi...Referat qismi....

@dp.callback_query_handler(IsUser(),text_contains="cancel:",state='*')
async def referal_cancel(call: types.CallbackQuery):
    data = call.data.rsplit(":")
    service = data[1]
    text = f"""{service} bekor qilindi.
Yangi {service} yaratish uchun quyidagi ✅Foydalanish tugmasini bosing!"""
    await call.message.edit_text(text=f"<b>{text}</b>")


from keyboards.inline.main_keyboard import editable_keyboards
@dp.callback_query_handler(IsUser(),text_contains="edit:",state='*')
async def referal_edit(call: types.CallbackQuery):
    data = call.data.rsplit(":")
    service = data[1]
    caption = await text_generator(type=f"{service}",user_id=call.from_user.id)
    caption += "<b>Nimani o'zgartirmoqchisiz❓ Quyidagilardan birini tanlang👇</b>"
    markup = editable_keyboards(service=service)
    await call.message.edit_text(text=caption,reply_markup=markup)

@dp.callback_query_handler(IsUser(),text_contains="back_to_:",state='*')
async def handle_referal_success_message(call: types.CallbackQuery):
    service = call.data.rsplit(":")[1]
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
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:256:error:{e}")

# Referat mavzusini olamiz
@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Referat)
async def handle_referal_message(message: types.Message, state: FSMContext):
    timeicon = await message.answer("⏳")

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
                ai=True
            )
            caption += f"• Ma'lumotlar to'g'ri bo'lsa, '✅Tayyorlash'\n"
            caption += f"• Biror ma'lumotni o'zgartirish uchun, '✏️O'zgartirish'.\n"
            caption += f"• Bekor qilish uchun, '🚫Rad qilish'."

            await timeicon.delete()
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

# Register foydalanuvningg ismini olamiz va instinutini olamiz.
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
# Referatda author nomini olganimizdan keyingi handler
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
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:362:error:{e}")

@dp.callback_query_handler(IsUser(),text_contains="cancel:")
async def referal_cancel(call: types.CallbackQuery):
    data = call.data.rsplit(":")
    service = data[1]
    text = f"""{service} bekor qilindi.
Yangi {service} yaratish uchun quyidagi ✅Foydalanish tugmasini bosing!"""
    await call.message.edit_text(text=f"<b>{text}</b>")


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
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line::error:{e}")

# Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy 
# Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy 
# Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy 
# Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy 
# Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy intelekt qismi Sun'iy 



@dp.callback_query_handler(IsUser(), text_contains="success:", state="*")
async def success_handler(call: types.CallbackQuery):

    data = call.data.rsplit(":")
    service = data[1]
    user = await db.select_user(user_id = int(call.from_user.id))
    user = user[0]
    
    with open("data.json", "r") as f:
        user_data = json.load(f)
    balance = user['balance']
    if service=="REFERAT":
        page_range_line = next((line for line in call.message.text.split('\n') if line.startswith("📰Sahifalar soni:")), "")
        page_numbers = re.search(r'(\d+dan)\s*–\s*(\d+gacha)', page_range_line)
        max_pages = page_numbers.group(2).replace('gacha', '')
        price = user_data['services']['Referat'][max_pages]
        if balance>=price:
            await db.update_balances(user_id=call.from_user.id,sum=int(balance)-int(price))
            await gg_generate_referat(call=call)
        else:
            await call.answer(cache_time=1)
            await call.message.answer(text=f"<b>😔Sizda {service} generatsiya qilish uchun yetarlicha mablag' yo'q</b>",reply_markup=get_premium_keyboard)
    elif service=="MUSTAQIL ISH":
        page_range_line = next((line for line in call.message.text.split('\n') if line.startswith("📰Sahifalar soni:")), "")
        page_numbers = re.search(r'(\d+dan)\s*–\s*(\d+gacha)', page_range_line)
        max_pages = page_numbers.group(2).replace('gacha', '')
        price = user_data['services']['Mustaqil Ish'][max_pages]
        if balance>=price:
            await db.update_balances(user_id=call.from_user.id,sum=int(balance)-int(price))
            await gg_generate_mustaqil(call=call)

        else:
            await call.answer(cache_time=1)
            await call.message.answer(text=f"<b>😔Sizda {service} generatsiya qilish uchun yetarlicha mablag' yo'q</b>",reply_markup=get_premium_keyboard)
    elif service=="BAYON":
        page_range_line = next((line for line in call.message.text.split('\n') if line.startswith("📰Sahifalar soni:")), "")
        page_numbers = re.search(r'(\d+dan)\s*–\s*(\d+gacha)', page_range_line)
        max_pages = page_numbers.group(2).replace('gacha', '')

        price = user_data['services']['Bayon'][max_pages]
        if balance>=price:
            try:
                await db.update_balances(user_id=call.from_user.id,sum=int(balance)-int(price))
                await gg_generate_bayon(call=call)
            except Exception as e:
                await bot.send_message(chat_id=ADMINS[0],text=f"Botda xatolik:ai.py:433 line:{e}")

        else:
            await call.answer(cache_time=1)
            await call.message.answer(text=f"<b>😔Sizda {service} generatsiya qilish uchun yetarlicha mablag' yo'q</b>",reply_markup=get_premium_keyboard)
    elif service=="INSHO":
            page_range_line = next((line for line in call.message.text.split('\n') if line.startswith("📰Sahifalar soni:")), "")
            page_numbers = re.search(r'(\d+dan)\s*–\s*(\d+gacha)', page_range_line)
            max_pages = page_numbers.group(2).replace('gacha', '')

            price = user_data['services']['Insho'][max_pages]
            if balance>=price:
                try:
                    await db.update_balances(user_id=call.from_user.id,sum=int(balance)-int(price))
                    await gg_generate_bayon(call=call)
                except Exception as e:
                    await bot.send_message(chat_id=ADMINS[0],text=f"Botda xatolik:ai.py:433 line:{e}")

            else:
                await call.answer(cache_time=1)
                await call.message.answer(text=f"<b>😔Sizda {service} generatsiya qilish uchun yetarlicha mablag' yo'q</b>",reply_markup=get_premium_keyboard)
    elif service=="TABRIK":
                page_range_line = next((line for line in call.message.text.split('\n') if line.startswith("📰Sahifalar soni:")), "")
                page_numbers = re.search(r'(\d+dan)\s*–\s*(\d+gacha)', page_range_line)
                max_pages = page_numbers.group(2).replace('gacha', '')

                price = user_data['services']['Tabrik'][max_pages]
                if balance>=price:
                    try:
                        await db.update_balances(user_id=call.from_user.id,sum=int(balance)-int(price))
                        await gg_generate_tabrik(call=call)
                    except Exception as e:
                        await bot.send_message(chat_id=ADMINS[0],text=f"Botda xatolik:ai.py:433 line:{e}")

                else:
                    await call.answer(cache_time=1)
                    await call.message.answer(text=f"<b>😔Sizda {service} generatsiya qilish uchun yetarlicha mablag' yo'q</b>",reply_markup=get_premium_keyboard)

async def themeCreator(mavzu,service,language,old_theme='None'):
    theme_data = [
        {
            "role": "user",
            "content": (
                f"Ortiqcha hech narsa demasdan faqat quyidagi promptni bajar: "
                f"{mavzu} mavzusi bo'yicha {service} uchun 3 ta mavzu yozib ber, {language} tilida. "
                f"Uni faqat sarlavha shaklida va to‘liq iboralarda yoz. "
                f"1.,2.,3. ko'rinishida yoz "
                "Hech qanday formatlash belgilaridan foydalanma: #, ##, *, **, _, ===, ``, >, [], (), markdown yoki html ishlatma. "
                    "Faqat oddiy, toza matn yoz."

                "Albatta, bajaraman degan so'zlarni yozishing shart emas.mavzular orasida hech qanday bosh joy tashlama"
            )
        }
    ]
    response = await get_response_from_server(history=theme_data)

    themes = response.get('response', "") #.split('\n')
    return themes


#  referal uchun mavzu generatsiya qiladi
# Generatsiya qilgan matni bo'yicha  matn generatsiya qiladi.

async def gg_generate_referat(call: types.CallbackQuery):
    time = datetime.datetime.now(uzbekistan_tz)
    message_text = call.message.text
    topic_line = next((line for line in message_text.split('\n') if line.startswith("📃Mavzu:")), "")
    topic = topic_line.split(":", 1)[-1].strip() if topic_line else "Unknown"
    page_range_line = next((line for line in message_text.split('\n') if line.startswith("📰Sahifalar soni:")), "")
    page_numbers = re.search(r'(\d+dan)\s*–\s*(\d+gacha)', page_range_line)
    max_pages = page_numbers.group(2).replace('gacha', '')
    
    themes_section = message_text.split("Rejalar:👇👇👇", 1)[-1].strip()
    themes_lines = []
    for line in themes_section.split('\n'):
        if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):  # maxsus punktlar uchun
            themes_lines.append(line.strip())
    themes = "\n".join(themes_lines)
    themes = [
        line.strip()
        for line in message_text.split("Rejalar:👇👇👇", 1)[-1].strip().split('\n')
        if re.match(r'^\d+\.', line.strip())
    ]
    user_id = call.from_user.id
    data = call.data.split(":")
    service = data[1]
    mavzu = topic
    max_pages = int(max_pages)

    page_count = {"10": 0, "15": 2, "20": 3, "25":4,"30":5}

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
    tasks = []

    for theme in themes:
        tasks.append(generate_text_for_theme_referat(user_id, theme, language, page_count, max_pages, ai_history))

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
async def generate_text_for_theme_referat(user_id, theme, language, page_count, max_pages, ai_history):
    # Agar theme lug‘atda mavjud bo‘lmasa, uni bo‘sh qiymat bilan boshlash
    if theme not in ai_history[str(user_id)]:
        ai_history[str(user_id)][theme] = ""

    if page_count[str(max_pages)] == 0:
        history = [
            {
                "role": "system",
                "content": (
                    f"Men seni telegram botga ulaganman. {theme} mavzusida matn kerak. "
                    f"{language} tilida. Matning 450 so'zdan oshmasin. "
                    "Faqat kerakli matnlarni yubor."
                     "Hech qanday formatlash belgilaridan foydalanma: #, ##, *, **, _, ===, ``, >, [], (), markdown yoki html ishlatma. "
                    "Faqat oddiy, toza matn yoz."
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
                        f"{language} tilida. Matning 700 so'zdan kam ham ko'p ham bo'lmasligi shart.xulosa yozishing shart emas"
                        f"Bu oldingi matning: {previous_text}. Yangi, farqli matn yozib ber."
                         "Hech qanday formatlash belgilaridan foydalanma: #, ##, *, **, _, ===, ``, >, [], (), markdown yoki html ishlatma. "
                    "Faqat oddiy, toza matn yoz."
                    )
                }
            ]
            response = await get_response_from_server(history=history)
            ai_history[str(user_id)][theme] += response['response']
            with open("ai_history.json", "w") as f:
                json.dump(ai_history, f, indent=4)

async def gg_generate_mustaqil(call: types.CallbackQuery):
    time = datetime.datetime.now(uzbekistan_tz)
    message_text = call.message.text
    topic_line = next((line for line in message_text.split('\n') if line.startswith("📃Mavzu:")), "")
    page_range_line = next((line for line in message_text.split('\n') if line.startswith("📰Sahifalar soni:")), "")
    page_numbers = re.search(r'(\d+dan)\s*–\s*(\d+gacha)', page_range_line)
    max_pages = page_numbers.group(2).replace('gacha', '')
    topic = topic_line.split(":", 1)[-1].strip() if topic_line else "Unknown"
    themes_section = message_text.split("Rejalar:👇👇👇", 1)[-1].strip()
    themes_lines = []
    for line in themes_section.split('\n'):
        if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):  # maxsus punktlar uchun
            themes_lines.append(line.strip())
    themes = "\n".join(themes_lines)
    themes = [
        line.strip()
        for line in message_text.split("Rejalar:👇👇👇", 1)[-1].strip().split('\n')
        if re.match(r'^\d+\.', line.strip())
    ]

    user_id = call.from_user.id
    data = call.data.split(":")
    service = data[1]
    mavzu = topic
    max_pages = int(max_pages)

    page_count = {"10": 0, "15": 2, "20": 3, "25": 4,"30":5}

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
    tasks = []
    for theme in themes:
        tasks.append(generate_text_for_theme_mustaqil(user_id, theme, language, page_count, max_pages, ai_history))
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
   

    await bot.send_chat_action(user_id, "upload_document")
    await asyncio.sleep(0.5)

    await msg.delete()
    await call.message.answer_document(InputFile(file_stream, filename=f"{mavzu}.docx"))

    ai_history[str(user_id)] = {}
    with open("ai_history.json", "w") as f:
        json.dump(ai_history, f, indent=4)

    time = datetime.datetime.now(uzbekistan_tz)
async def generate_text_for_theme_mustaqil(user_id, theme, language, page_count, max_pages, ai_history):
    # Agar theme lug‘atda mavjud bo‘lmasa, uni bo‘sh qiymat bilan boshlash
    if theme not in ai_history[str(user_id)]:
        ai_history[str(user_id)][theme] = ""

    if page_count[str(max_pages)] == 0:
        history = [
            {
                "role": "system",
                "content": (
                    f"{theme} mavzusida matn kerak. "
                    f"{language} tilida. Matning 450 so'zdan oshmasin. "
                    "Faqat kerakli matnlarni yubor."
                     "Hech qanday formatlash belgilaridan foydalanma: #, ##, *, **, _, ===, ``, >, [], (), markdown yoki html ishlatma. "
                    "Faqat oddiy, toza matn yoz."
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
                        f" {theme} mavzusida matn kerak. "
                        f"{language} tilida. Matning 700 so'zdan kam ham ko'p ham bo'lmasligi shart.xulosa yozishing shart emas"
                        f"Bu oldingi matning: {previous_text}. Yangi, farqli matn yozib ber."
                         "Hech qanday formatlash belgilaridan foydalanma: #, ##, *, **, _, ===, ``, >, [], (), markdown yoki html ishlatma. "
                    "Faqat oddiy, toza matn yoz."
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


from keyboards.inline.main_keyboard import success_keyboards_bayon
@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Bayon)
async def handle_bayon_message(message: types.Message, state: FSMContext):
    service = "BAYON"
    markup = success_keyboards_bayon(service)
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
            with open('user_info.json','r') as file:
                data = json.load(file)

            mavzu = data[str(user_id)]['mavzu']
            caption = f"🌟Ajoyib, quyidagi ma'lumotlarni tekshiring\n\n"
            caption += f"<b>«{service}»</b>\n\n"
            caption += f"📰Sahifalar soni: <b>5dan – 10gacha</b>\n"
            caption += f"📃Mavzu: <b>{mavzu}</b>\n"
            await message.answer(text=caption,reply_markup=markup)
            await state.finish()
    except Exception as e:
        await state.finish()
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:52:error:{e}")


@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Insho)
async def handle_insho_message(message: types.Message, state: FSMContext):
    service = "INSHO"
    markup = success_keyboards_bayon(service)
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
        with open('user_info.json','r') as file:
            data = json.load(file)
        mavzu = data[str(user_id)]['mavzu']
        caption = f"🌟Ajoyib, quyidagi ma'lumotlarni tekshiring\n\n"
        caption += f"<b>«{service}»</b>\n\n"
        caption += f"📰Sahifalar soni: <b>5dan – 10gacha</b>\n"
        caption += f"📃Mavzu: <b>{mavzu}</b>\n"
        await message.answer(text=caption,reply_markup=markup)
        await state.finish()

        mavzu = data[str(user_id)]['mavzu']
        caption = f"🌟Ajoyib, quyidagi ma'lumotlarni tekshiring\n\n"
        caption += f"<b>«{service}»</b>\n\n"
        caption += f"📰Sahifalar soni: <b>5dan – 10gacha</b>\n"
        caption += f"📃Mavzu: <b>{mavzu}</b>\n"
        await message.answer(text=caption,reply_markup=markup)
        await state.finish()
    except Exception as e:
        await state.finish()
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:52:error:{e}")



@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Tabrik)
async def handle_tabrik_message(message: types.Message, state: FSMContext):
    service = "TABRIK"
    markup = success_keyboards_bayon(service)
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
        with open('user_info.json','r') as file:
            data = json.load(file)
        mavzu = data[str(user_id)]['mavzu']
        caption = f"🌟Ajoyib, quyidagi ma'lumotlarni tekshiring\n\n"
        caption += f"<b>«{service}»</b>\n\n"
        caption += f"📰Sahifalar soni: <b>5dan – 10gacha</b>\n"
        caption += f"Tabrik Egasining ismi: <b>{mavzu}</b>\n"
        await message.answer(text=caption,reply_markup=markup)
        await state.finish()
    except Exception as e:
        await state.finish()
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:52:error:{e}")


 
# AI handlerlari AI handlerlari AI handlerlari AI handlerlari AI handlerlari AI handlerlari AI handlerlari AI handlerlari 
# AI handlerlari AI handlerlari AI handlerlari AI handlerlari AI handlerlari AI handlerlari AI handlerlari AI handlerlari 

async def gg_generate_bayon(call: types.CallbackQuery):
    time = datetime.datetime.now(uzbekistan_tz)
    message_text = call.message.text
    topic_line = next((line for line in message_text.split('\n') if line.startswith("📃Mavzu:")), "")
    page_range_line = next((line for line in message_text.split('\n') if line.startswith("📰Sahifalar soni:")), "")
    page_numbers = re.search(r'(\d+dan)\s*–\s*(\d+gacha)', page_range_line)

    max_pages = page_numbers.group(2).replace('gacha', '')
    topic = topic_line.split(":", 1)[-1].strip() if topic_line else "Unknown"
    

    user_id = call.from_user.id
    data = call.data.split(":")
    service = data[1]
    mavzu = topic
    max_pages = int(max_pages)

    page_count = {"10": 0, "15": 2, "20": 3, "25": 4,"30":5}

    # Fetch user from database
    user = await db.select_user(user_id=user_id)
    language = user[0].get('language', "")

    msg = await call.message.edit_text("⏳")

    # Generate themes
    theme_data = [
        {
            "role": "user",
            "content": (
                f"Ortiqcha hech narsa demasdan faqat quyidagi promptni bajar: "
                f"{mavzu} mavzusi bo'yicha {service} uchun 3 ta mavzu yozib ber, {language} tilida. "
                "Albatta, bajaraman degan so'zlarni yozishing shart emas.mavzular orasida hech qanday bosh joy tashlama"
                 "Hech qanday formatlash belgilaridan foydalanma: #, ##, *, **, _, ===, ``, >, [], (), markdown yoki html ishlatma. "
                    "Faqat oddiy, toza matn yoz."
            )
        }
    ]
    theme_response = await get_response_from_server(history=theme_data)
    await call.message.answer(text=f"<b>{theme_response['response']}</b>")
    themes = theme_response.get('response', "").split('\n')

    tasks = []
    await msg.delete()
    for theme in themes:
        tasks.append(generate_text_for_theme_bayon(user_id, theme, language, page_count, max_pages))

    await asyncio.gather(*tasks)

    await asyncio.sleep(0.5)

    time = datetime.datetime.now(uzbekistan_tz)
async def generate_text_for_theme_bayon(user_id, theme, language, page_count, max_pages):
    if page_count[str(max_pages)] == 0:
        history = [
            {
                "role": "system",
                "content": (
                    f"{theme} mavzusida matn kerak. "
                    f"{language} tilida. Matn uzunligi: max_length:4080 bo'lishi kerak va undan ochib ketmasligi kerak. "
                    "Faqat kerakli matnlarni yubor.albatta,bajaraman yoki shunga o'xshagan narsalarni yuborma.faqatgina matnni yubor."
                     "Hech qanday formatlash belgilaridan foydalanma: #, ##, *, **, _, ===, ``, >, [], (), markdown yoki html ishlatma. "
                    "Faqat oddiy, toza matn yoz."
                )
            }
        ]
        
        response = await get_response_from_server(history=history)
        matn = f"**{theme}**\n\n{response['response']}"
        await bot.send_chat_action(int(user_id), "typing")
        await bot.send_message(chat_id=int(user_id),text=matn,parse_mode=types.ParseMode.MARKDOWN)


async def gg_generate_tabrik(call: types.CallbackQuery):
    message_text = call.message.text
    topic_line = next((line for line in message_text.split('\n') if line.startswith("Tabrik Egasining ismi: ")), "")

    topic = topic_line.split(":", 1)[-1].strip() if topic_line else "Unknown"
    

    user_id = call.from_user.id
    data = call.data.split(":")
    service = data[1]
    ega = topic
    msg = await call.message.edit_text("⏳")

    # Generate themes
    tabrik_prompt = [
        {
            "role": "user",
            "content": (
                f"Menga {ega}ning tug'gilgan kuni  uchun chiroyli tabrik kerak, bu tabrik oldin takrorlanmagan va jarangdor bo'lishi kerak.bu tabrik uning hech kimning esidan chiqmasligi kerak va u uzun bo'lsin stikerlardan ham foydalan."
                "Albatta, bajaraman degan so'zlarni yozishing shart emas.tabrik meni nomimdan bo'lishi kerak va uni odam yozgandek bo'lib ko'rinishi kerak."
                 "Hech qanday formatlash belgilaridan foydalanma: #, ##, *, **, _, ===, ``, >, [], (), markdown yoki html ishlatma. "
                    "Faqat oddiy, toza matn yoz."
            )
        }
    ]
    theme_response = await get_response_from_server(history=tabrik_prompt)

    await msg.delete()
    await call.message.answer(text=f"<b>{theme_response['response']}</b>")


# Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI 
# Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI 
# Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI 
# Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI Taqdimot AI 



