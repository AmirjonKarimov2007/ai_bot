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
        caption += f"📰Sahifalar soni: <b>{min}dan – {max}gacha</b>\n\n"

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
    markup = InlineKeyboardMarkup(row_width=3)
    markup.insert(InlineKeyboardButton(text="✅Tayyorlash",callback_data="success:referat"))
    markup.insert(InlineKeyboardButton(text="🚫Rad qilish",callback_data="cancel:referat"))
    markup.insert(InlineKeyboardButton(text="✏️O'zgartirish",callback_data="edit:referat"))
    mavzu = message.text
    user_id = str(message.from_user.id)  
    if os.path.exists('user_info.json'):
        with open('user_info.json', "r", encoding="utf-8") as file:
            user_info = json.load(file)
    else:
        user_info = {}

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
                type="REFERAT",
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
    markup = InlineKeyboardMarkup(row_width=3)
    markup.insert(InlineKeyboardButton(text="✅Tayyorlash",callback_data="success:referat"))
    markup.insert(InlineKeyboardButton(text="🚫Rad qilish",callback_data="cancel:referat"))
    markup.insert(InlineKeyboardButton(text="✏️O'zgartirish",callback_data="edit_service:referat"))
    try:
        await db.update_user_univer(univer=univer,user_id=int(message.from_user.id))
        status = await check_info(user_id=message.from_user.id)
    
        if status==True:
            caption = await text_generator(
                type="REFERAT",
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
    markup = InlineKeyboardMarkup(row_width=3)
    markup.insert(InlineKeyboardButton(text="✅Tayyorlash",callback_data="success:referat"))
    markup.insert(InlineKeyboardButton(text="🚫Rad qilish",callback_data="cancel:referat"))
    markup.insert(InlineKeyboardButton(text="✏️O'zgartirish",callback_data="edit:referat"))
    try:
        await db.update_user_author(author=author,user_id=int(message.from_user.id))
        status = await check_info(user_id=message.from_user.id)
    
        if status==True:
            caption = await text_generator(
                type="REFERAT",
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

@dp.callback_query_handler(IsUser(),text_contains="edit_service:")
async def referal_cancel(call: types.CallbackQuery):
    data = call.data.rsplit(":")
    service = data[1]
    text = """"""






























@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Mustaqil)
async def handle_mustaqil_message(message: types.Message, state: FSMContext):
    prompt = message.text
    # Example usage
    history_data = [
        {
            "role": "user",
            "content": f"{prompt}"
        }
    ]
    r = get_response_from_server(history_data)
    r = r['response']
    await message.answer(f"{r}",parse_mode=types.ParseMode.MARKDOWN)
    await state.finish() 

@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Slaydlar)
async def handle_slaydlar_message(message: types.Message, state: FSMContext):
    prompt = message.text
    # Example usage
    history_data = [
        {
            "role": "user",
            "content": f"{prompt}"
        }
    ]
    r = get_response_from_server(history_data)
    r = r['response']
    await message.answer(f"{r}",parse_mode=types.ParseMode.MARKDOWN)
    await state.finish() 

@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Insho)
async def handle_insho_message(message: types.Message, state: FSMContext):
    # Handle message for the 'Insho' state
    prompt = message.text
    # Example usage
    history_data = [
        {
            "role": "user",
            "content": f"{prompt}"
        }
    ]
    r = get_response_from_server(history_data)
    r = r['response']
    await message.answer(f"{r}",parse_mode=types.ParseMode.MARKDOWN)
    await state.finish() 

@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Tabrik)
async def handle_tabrik_message(message: types.Message, state: FSMContext):
    # Handle message for the 'Tabrik' state
    prompt = message.text
    # Example usage
    history_data = [
        {
            "role": "user",
            "content": f"{prompt}"
        }
    ]
    r = get_response_from_server(history_data)
    r = r['response']
    await message.answer(f"{r}",parse_mode=types.ParseMode.MARKDOWN)
    await state.finish() 

@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Bayon)
async def handle_bayon_message(message: types.Message, state: FSMContext):
    prompt = message.text
    # Example usage
    history_data = [
        {
            "role": "user",
            "content": f"{prompt}"
        }
    ]
    r = get_response_from_server(history_data)
    r = r['response']
    await message.answer(f"{r}",parse_mode=types.ParseMode.MARKDOWN)
    await state.finish() 







@dp.callback_query_handler(IsUser(), text="back_to_service_menu", state="*")
async def back_to_main_menu_method(call: types.CallbackQuery,state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text(text="<b>Qaysi Xizmatdan Foydalanmoqchisiz:</b>", reply_markup=services_keyboards__board())
    await state.finish()
