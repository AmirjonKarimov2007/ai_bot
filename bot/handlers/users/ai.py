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
@dp.callback_query_handler(IsUser(),text_contains='select_service:',state='*')
async def select_service(call: types.CallbackQuery):
    info =  call.data.rsplit(":")
    service = info[1]
    with open ('data.json','r') as f:
        data = json.load(f)
    service_price = data['services'][service]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="⬅️Orqaga",callback_data="back_to_service_menu"))
    await call.message.edit_text(text=f"<b>{service} mavzusini yuboring</b>",reply_markup=markup)
    if service == "Referat":
        await ServicesStates.Referal.set()
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
        

@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Referal)
async def handle_referal_message(message: types.Message, state: FSMContext):
    # Handle message for the 'Referal' state
    user_input = message.text
    await message.answer(f"Siz {user_input} haqida ma'lumot berdingiz.")
    await state.finish()  

@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Mustaqil)
async def handle_mustaqil_message(message: types.Message, state: FSMContext):
    user_input = message.text
    await message.answer(f"Siz {user_input} haqida mustaqil ma'lumot berdingiz.")
    await state.finish()

@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Slaydlar)
async def handle_slaydlar_message(message: types.Message, state: FSMContext):
    # Handle message for the 'Slaydlar' state
    user_input = message.text
    await message.answer(f"Siz {user_input} haqida slaydlar yubordingiz.")
    await state.finish()

@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Insho)
async def handle_insho_message(message: types.Message, state: FSMContext):
    # Handle message for the 'Insho' state
    user_input = message.text
    await message.answer(f"Siz {user_input} haqida insho yubordingiz.")
    await state.finish()

@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Tabrik)
async def handle_tabrik_message(message: types.Message, state: FSMContext):
    # Handle message for the 'Tabrik' state
    user_input = message.text
    await message.answer(f"Siz {user_input} haqida tabrik yubordingiz.")
    await state.finish()

@dp.message_handler(IsUser(),content_types=ContentTypes.TEXT, state=ServicesStates.Bayon)
async def handle_bayon_message(message: types.Message, state: FSMContext):
    # Handle message for the 'Bayon' state
    user_input = message.text
    await message.answer(f"Siz {user_input} haqida bayon yubordingiz.")








@dp.callback_query_handler(IsUser(), text="back_to_service_menu", state="*")
async def back_to_main_menu_method(call: types.CallbackQuery,state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text(text="<b>Qaysi Xizmatdan Foydalanmoqchisiz:</b>", reply_markup=services_keyboards__board())
    await state.finish()
