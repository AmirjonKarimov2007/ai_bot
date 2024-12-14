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
    print(user_info['author'])
    if user_info['author'] and user_info['language'] and user_info['univer']:
        return True
    elif not user_info['author']:
        return False
    elif not user_info['language']:
        return False
    elif not user_info['univer']:
        return False


@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Referat)
async def handle_referal_message(message: types.Message, state: FSMContext):
    text = """Institut va kafedrangizni(majburiy emas) to'liq kiriting.

📋Namuna: FARG‘ONA DAVLAT UNIVERSITETI IQTISODIYOT KAFEDRASI"""
    mavzu = message.text
    try:
        await state.update_data({"mavzu":mavzu})
        status = await check_info(user_id=message.from_user.id)
        if status==True:
            await message.answer('sizda hammasi joyida')
        else:
            await message.answer(text=f"<b>{text}</b>")
            await ServicesStates.Referat_AUTHOR_NAME.set()
    except Exception as e:
        await state.finish()
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:52:error:{e}")





@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Referat_AUTHOR_NAME)
async def handle_referal_author__message(message: types.Message, state: FSMContext):
    univer = message.text
    text = """Muallif ism-familiyasi, guruhi va hokazolarni to'liq kiriting.

📋Namuna: Isroilov Ismoiljon Muhiddin o'g'li, 4-kurs, 21.36-guruh"""
    try:
        await state.update_data({"univer":{univer}})
        await db.update_user_univer(univer=univer,user_id=int(message.from_user.id))
        status = await check_info(user_id=message.from_user.id)
        if status==True:
            await message.answer('Sizda hammasi joyida')
        else:
            await message.answer(f"<b>{text}</b>")
            await ServicesStates.Referat_LANGUAGE.set()
    except Exception as e:
        await state.finish()
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:70:error:{e}")

@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Referat_LANGUAGE)
async def handle_referal_langugage__message(message: types.Message, state: FSMContext):
    text="""Tilni tanlang"""
    LANGUAGE_CHOICES = [
    ('eng', 'English'),
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
]
    try:
        name = message.text
        await db.update_user_author(author=name,user_id=int(message.from_user.id))
        
        await state.update_data({"name":{name}})
        await message.answer(f"<b>{text}</b>")
        await ServicesStates.Referat_LANGUAGE.set()
    except Exception as e:
        await state.finish()
        await bot.send_message(chat_id=ADMINS[0],text=f"xatolik: ai.py ,line:81:error:{e}")







































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
