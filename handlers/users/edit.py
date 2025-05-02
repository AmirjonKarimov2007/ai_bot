from loader import db,dp,bot
from aiogram import types
from data.config import ADMINS
from filters.admins import ADMINS
from filters.users import IsUser
from states.ai_state import SERVICE_EDIT
import os
import json
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from keyboards.inline.main_keyboard import success_keyboards
from aiogram.dispatcher import FSMContext
from .ai import text_generator,editable_keyboards,check_info

@dp.callback_query_handler(IsUser(),text_contains="change_theme:",state='*')
async def change_theme(call: types.CallbackQuery,state: FSMContext):
    data = call.data.rsplit(":")
    service =data[1]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"edit:{service}"))
    await call.message.edit_text("<b>🆕 Yangi mavzuni to'liq, bexato va tushunarli xolatda yuboring</b>:",reply_markup=markup)
    await state.update_data({"service":service})
    await SERVICE_EDIT.Referat_THEME.set()

@dp.message_handler(IsUser(),content_types=types.ContentType.TEXT,state=SERVICE_EDIT.Referat_THEME)
async def edit_theme(message: types.Message,state:FSMContext):
    mavzu = message.text
    user_id = str(message.from_user.id)  
    data = await state.get_data()
    service = data.get('service')

    if os.path.exists('user_info.json'):
        with open('user_info.json', "r", encoding="utf-8") as file:
            user_info = json.load(file)
    else:
        user_info = {}

    user_info[user_id]['mavzu'] = mavzu

    with open('user_info.json', "w", encoding="utf-8") as file:
            json.dump(user_info, file, indent=4, ensure_ascii=False)
        
    caption = await text_generator(type=f"{service}",user_id=message.from_user.id)
    caption += "<b>Nimani o'zgartirmoqchisiz❓ Quyidagilardan birini tanlang👇</b>"
    markup = editable_keyboards(service=service)
    
    await message.answer(text=caption,reply_markup=markup)
    await state.finish()



# Univerni edit qilish uchun handlerlar shu yerga yozilgan
@dp.callback_query_handler(IsUser(),text_contains="change_univer:",state='*')
async def change_theme(call: types.CallbackQuery,state:FSMContext):
    data = call.data.rsplit(":")
    service =data[1]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"edit:{service}"))
    await call.message.edit_text(f"Institut va kafedrangizni to'liq kiriting\n\n📋Namuna: <b>FARG‘ONA DAVLAT UNIVERSITETI IQTISODIYOT KAFEDRASI</b>",reply_markup=markup)
    await state.update_data({"service":service})
    await SERVICE_EDIT.Referat_UNIVER.set()
    


@dp.message_handler(IsUser(),content_types=types.ContentType.TEXT,state=SERVICE_EDIT.Referat_UNIVER)
async def edit_theme(message: types.Message,state:FSMContext):
    univer = message.text
    data = await state.get_data()
    service = data.get('service')
    
    markup = success_keyboards(service)
    try:
        await db.update_user_univer(univer=univer,user_id=int(message.from_user.id))
        caption = await text_generator(type=f"{service}",user_id=message.from_user.id)
        caption += "<b>Nimani o'zgartirmoqchisiz❓ Quyidagilardan birini tanlang👇</b>"
        markup = editable_keyboards(service=service)
        
        await message.answer(text=caption,reply_markup=markup)
        await state.finish()

    except Exception as e:
        caption = await text_generator(type=f"{service}",user_id=message.from_user.id)
        caption += "<b>Nimani o'zgartirmoqchisiz❓ Quyidagilardan birini tanlang👇</b>"
        markup = editable_keyboards(service=service)
        
        await message.answer(text=caption,reply_markup=markup)
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:137:error:{e}")
        await state.finish()

# Muallifni edit qilish uchun handlerlar shu yerga yozilgan



@dp.callback_query_handler(IsUser(),text_contains="change_author:",state='*')
async def change_theme(call: types.CallbackQuery,state:FSMContext):
    data = call.data.rsplit(":")
    service =data[1]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"edit:{service}"))
    await call.message.edit_text(f"Muallif ism-familiyasi, guruhi va hokazolarni to'liq kiriting.📋Namuna: <b>Isroilov Ismoiljon Muhiddin o'g'li, 4-kurs, 21.36-guruh</b>",reply_markup=markup)
    await state.update_data({"service":service})
    await SERVICE_EDIT.Referat_AUTHOR_NAME.set()
    


@dp.message_handler(IsUser(),content_types=types.ContentType.TEXT,state=SERVICE_EDIT.Referat_AUTHOR_NAME)
async def edit_author_name(message: types.Message,state:FSMContext):
    author = message.text
    data = await state.get_data()
    service = data.get('service')
    
    markup = success_keyboards(service)
    try:
        await db.update_user_author(author=author,user_id=int(message.from_user.id))
        caption = await text_generator(type=f"{service}",user_id=message.from_user.id)
        caption += "<b>Nimani o'zgartirmoqchisiz❓ Quyidagilardan birini tanlang👇</b>"
        markup = editable_keyboards(service=service)
        
        await message.answer(text=caption,reply_markup=markup)
        await state.finish()

    except Exception as e:
        caption = await text_generator(type=f"{service}",user_id=message.from_user.id)
        caption += "<b>Nimani o'zgartirmoqchisiz❓ Quyidagilardan birini tanlang👇</b>"
        markup = editable_keyboards(service=service)
        
        await message.answer(text=caption,reply_markup=markup)
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:137:error:{e}")
        await state.finish()




# BU yerda language uchun handler yozilgan

@dp.callback_query_handler(IsUser(),text_contains="change_language:",state='*')
async def change_theme(call: types.CallbackQuery,state:FSMContext):
    data = call.data.rsplit(":")
    service =data[1]
    markup = InlineKeyboardMarkup(row_width=2)
    LANGUAGE_CHOICES = (
        "🇺🇿uz",
        "🇷🇺ru",
        "🇺🇸en"
    )
    for language in LANGUAGE_CHOICES:
        markup.insert(InlineKeyboardButton(text=f"{language}", callback_data=f"edit_language:{language[2::]}:{service}"))
    markup.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"edit:{service}"))
    await call.message.edit_text(f"🇺🇿 Tilni tanlang",reply_markup=markup)
    


@dp.callback_query_handler(IsUser(),text_contains="edit_language",state='*')
async def edit_language(call: types.CallbackQuery):
    data = call.data.rsplit(":")

    language = data[1]
    service = data[2]    
    markup = success_keyboards(service)
    try:
        await db.update_user_language(language=language,user_id=int(call.from_user.id))
        caption = await text_generator(type=f"{service}",user_id=call.from_user.id)
        caption += "<b>Nimani o'zgartirmoqchisiz❓ Quyidagilardan birini tanlang👇</b>"
        markup = editable_keyboards(service=service)
        
        await call.message.edit_text(text=caption,reply_markup=markup)

    except Exception as e:
        caption = await text_generator(type=f"{service}",user_id=call.from_user.id)
        caption += "<b>Nimani o'zgartirmoqchisiz❓ Quyidagilardan birini tanlang👇</b>"
        markup = editable_keyboards(service=service)
        
        await call.message.edit_text(text=caption,reply_markup=markup)
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:137:error:{e}")



@dp.callback_query_handler(IsUser(),text_contains="add_page:",state='*')
async def add_page(call: types.CallbackQuery):
    call_info = call.data.rsplit(":")
    service = call_info[1]
    markup = editable_keyboards(service=service)
    with open ('user_info.json','r',encoding='utf-8') as file:
        data = json.load(file)
    min = data[str(call.from_user.id)]['min']
    max = data[str(call.from_user.id)]['max']
    if max==30 and min==25:
        await bot.answer_callback_query(callback_query_id=call.id,text="Sahifalar soni dan ko'p bo'lmaydi❗️",show_alert=True)
    elif max<30 and min<25:
        data[str(call.from_user.id)]['min']+=5
        data[str(call.from_user.id)]['max']+=5
        await bot.answer_callback_query(callback_query_id=call.id,text=f"✅Sahifalar soni 5ga ochirildi")
        with open('user_info.json','w')as file:
            json.dump(data,file,indent=4)
        caption = await text_generator(type=service,user_id=call.from_user.id)
        caption+=f"<b>Nimani o'zgartirmoqchisiz❓ Quyidagilardan birini tanlang👇</b>"
        await call.message.edit_text(text=caption,reply_markup=markup)

@dp.callback_query_handler(IsUser(),text_contains="delete_page:",state='*')
async def add_page(call: types.CallbackQuery):
    call_info = call.data.rsplit(":")
    service = call_info[1]
    markup = editable_keyboards(service=service)
    with open ('user_info.json','r',encoding='utf-8') as file:
        data = json.load(file)
    min = data[str(call.from_user.id)]['min']
    max = data[str(call.from_user.id)]['max']
    if max==10 and min==5:
        await bot.answer_callback_query(callback_query_id=call.id,text="Sahifalar soni 5 - 10 dan ko'p bo'lmaydi❗️",show_alert=True)
    elif max>10 and min>5:
        data[str(call.from_user.id)]['min']-=5
        data[str(call.from_user.id)]['max']-=5
        await bot.answer_callback_query(callback_query_id=call.id,text=f"Sahifalar soni 5ga kamaydi 🚫")
        with open('user_info.json','w')as file:
            json.dump(data,file,indent=4)
        caption = await text_generator(type=service,user_id=call.from_user.id)
        caption+=f"<b>Nimani o'zgartirmoqchisiz❓ Quyidagilardan birini tanlang👇</b>"
        await call.message.edit_text(text=caption,reply_markup=markup)




@dp.callback_query_handler(IsUser(),text_contains="see_page:",state='*')
async def add_page(call: types.CallbackQuery):
    call_info = call.data.rsplit(":")
    service = call_info[1]
    markup = editable_keyboards(service=service)
    with open ('user_info.json','r',encoding='utf-8') as file:
        data = json.load(file)
    min = data[str(call.from_user.id)]['min']
    max = data[str(call.from_user.id)]['max']
    await bot.answer_callback_query(callback_query_id=call.id,text=f"Sahifalar soni {min} dan {max} gacha",show_alert=True)
    