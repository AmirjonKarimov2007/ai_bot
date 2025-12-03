from aiogram.utils.exceptions import BotBlocked,TelegramAPIError,ChatNotFound
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.tekshirish import tekshir
from loader import bot, db
from filters import IsUser, IsSuperAdmin, IsGuest
from filters.admins import IsAdmin
from datetime import datetime
import pytz
import re
import html




# O‘zbekiston vaqt zonasi
uzbekistan_tz = pytz.timezone('Asia/Tashkent')

# Hozirgi vaqtni O‘zbekiston vaqt zonasi bilan olish


async def kanallar():
    royxat = []
    ights = await db.select_channels()

    for x in ights:
        royxat.append(x[1])
    return royxat

class Asosiy(BaseMiddleware):
    async def on_pre_process_update(self, xabar: types.Update, data: dict):
        current_time = datetime.now(uzbekistan_tz)

        if xabar.message:
            if xabar.message.pinned_message:
                pass
            if xabar.message.text:
                cleaned_text = re.sub(r"<[^>]*>", "", xabar.message.text)
                xabar.message.text = html.escape(cleaned_text.strip())
            user_id = xabar.message.from_user.id
            username = xabar.message.from_user.username
            first_name = xabar.message.from_user.first_name
            matn = "<b>🤖 Botdan Foydalanish uchun ro'yxatdan o'tishingiz kerak. \n\nIltimos telefon raqamingizni \"Raqamni yuborish\" tugmasi orqali yuboring.!</b>"
            user_info = await db.select_user(user_id=int(user_id))
            argument = xabar.message.get_args()
            if user_info:
               pass
            else:
                if argument:
                    if await db.is_user(user_id=int(argument)) and argument.isdigit() and int(argument) > 10:
                        try:

                            if xabar.message.from_user.is_premium:
                                await db.add_user(
                                    user_id=user_id, username=username, name=first_name, ref_father=int(argument),is_premium=True,
                                    created_date=current_time, updated_date=current_time
                                )                  
                            else:
                                await db.add_user(
                                    user_id=user_id, username=username, name=first_name, ref_father=int(argument),
                                    created_date=current_time, updated_date=current_time
                                )  
                        except asyncpg.exceptions.UniqueViolationError:
                            await db.select_user(user_id=user_id)
                        except Exception as e:
                            await bot.send_message(chat_id=ADMINS[0], text=f'Botda xatolik yuz berdi: majburiy_obuna:40{e}')
                else:
                    try:
                        if xabar.message.from_user.is_premium:
                            await db.add_user(user_id=int(user_id), username=username, name=first_name,is_premium=True,created_date=current_time,updated_date=current_time)
                        else:
                            await db.add_user(user_id=int(user_id), username=username, name=first_name,created_date=current_time,updated_date=current_time)

                    except asyncpg.exceptions.UniqueViolationError:
                        await db.select_user(user_id=int(user_id))
                    except Exception as e:
                            await bot.send_message(chat_id=ADMINS[0], text=f'Botda xatolik yuz berdi: majburiy_obuna:47{e}')
               
        elif xabar.callback_query:
            user_id = xabar.callback_query.from_user.id
        else:
            return
      
        matn = "<b>🤖 Botdan Foydalanish uchun kanallarga a'zo bo'lib. \n\n\"✅ Tekshirish\" tugmasini bosing!</b>"
        royxat = []
        dastlabki = True

        for k in await kanallar():
            holat = await tekshir(user_id=user_id, kanal_id=k)
            dastlabki *= holat
            kanals = await bot.get_chat(k)
            if not holat:
                link = await kanals.export_invite_link()
                button = [InlineKeyboardButton(text=f"{kanals.title}", url=f"{link}")]
                royxat.append(button)
        royxat.append([InlineKeyboardButton(text="✅ Tekshirish", callback_data="start")])
        if not dastlabki:
            if xabar.callback_query:
                data = xabar.callback_query.data
                if data=='start':
                    await xabar.callback_query.message.delete()
            try:
                await bot.send_message(chat_id=user_id, text=matn, reply_markup=InlineKeyboardMarkup(inline_keyboard=royxat))
            except BotBlocked:
                print(f"Foydalanuvchi {user_id} botni bloklagan:line-72")
            except ChatNotFound:
                print(f"Foydalanuvchi {user_id} bilan suhbat topilmadi.")
                return
            except Exception as e:
                print(f"Xatolik yuz berdi:marburiy obuna:80: {e}")

            raise CancelHandler()

from keyboards.default.menu import *
import asyncpg
from data.config import ADMINS
from states.admin_state import RegisterState
from aiogram.dispatcher import FSMContext
from loader import dp
class CheckPhoneNumber(BaseMiddleware):
    async def on_pre_process_update(self, xabar: types.Update, data: dict):
        current_time = datetime.now(uzbekistan_tz)

        if xabar.message:
            user_id = xabar.message.from_user.id
            username = xabar.message.from_user.username
            first_name = xabar.message.from_user.first_name
            content_type = xabar.message.content_type
            
            if content_type == 'contact':
                return 
            if xabar.message.pinned_message:
                return
            if str(xabar.message.chat.id).startswith('-'):
                return


        elif xabar.callback_query:

            user_id = xabar.callback_query.from_user.id
            username = xabar.callback_query.from_user.username
            first_name = xabar.callback_query.from_user.first_name
            data = xabar.callback_query.data
            if data=='start':
                await xabar.callback_query.message.delete()
        else:
            return
        
        bot_username = await  bot.get_me()
        bot_username = bot_username.username
        if bot_username == username:
            return
        

        user_state = await dp.current_state(user=user_id).get_state()
        matn = "<b>🤖 Botdan Foydalanish uchun ro'yxatdan o'tishingiz kerak. \n\nIltimos telefon raqamingizni \"Raqamni yuborish\" tugmasi orqali yuboring.!</b>"
        user_info = await db.select_user(user_id=int(user_id))
        if user_info:
            user = user_info[0]
            register = user['register']
            number = user['number']
            
            if number is None and bot_username!=username:
                try:
                    await bot.send_message(chat_id=user_id, text=matn, reply_markup=kb.contact())
                    await dp.current_state(user=user_id).set_state(RegisterState.PhoneNumber)
                except BotBlocked:
                    print(f"Foydalanuvchi {user_id} botni bloklagan:line-131")
                except Exception as e:
                    await bot.send_message(ADMINS[0],text=f"Xatolik yuz berdi:Check_Phone_Number:136:{e}")
            else:
                return
        else:
            if xabar.message:
                argument = xabar.message.get_args()
                if argument:
                    if argument.isdigit() and int(argument) > 10 and await db.is_user(user_id=int(argument)):
                        try:
                            rfather = await db.is_user(user_id=int(argument))
                            ffather_name = rfather[0]['name']
                            ffather_username = rfather[0]['username']
                            try:
                                if xabar.message.from_user.is_premium:
                                    await db.add_user(user_id=user_id, username=username, name=first_name,is_premium=True ,ref_father=int(argument),created_date=current_time,updated_date=current_time)
                                else:
                                    await db.add_user(user_id=user_id, username=username, name=first_name, ref_father=int(argument),created_date=current_time,updated_date=current_time)

                                await bot.send_message(
                                    chat_id=user_id, 
                                    text=f"<b>👋🏻 Assalomu Aleykum {first_name}, botimizga Tashrif buyurganingizdan xursandmiz kelipsiz!\n\nSizni <a href='t.me/{ffather_username}'>{xabar.message.from_user.full_name}</a> taklif qildi.</b>", 
                                    reply_markup=kb.contact()
                                )
                            except BotBlocked:
                                print(f"Foydalanuvchi {user_id} botni bloklagan:153-line")
                            except asyncpg.exceptions.UniqueViolationError:
                                await db.select_user(user_id=user_id)
                            except Exception as e:
                                await bot.send_message(ADMINS[0],text=f"Xatolik yuz berdi::Check_Phone_Number:158{e}")
                        except Exception as e:
                            await bot.send_message(chat_id=ADMINS[0], text=f'Botda xatolik yuz berdi::Check_Phone_Number:160 {e}')
                else:
                    
                    try:
                        if xabar.message.from_user.is_premium:
                            await db.add_user(user_id=user_id, username=username, name=first_name, is_premium=True,ref_father=int(argument),created_date=current_time,updated_date=current_time)
                        else:
                            await db.add_user(user_id=user_id, username=username, name=first_name, ref_father=int(argument),created_date=current_time,updated_date=current_time)

                    except asyncpg.exceptions.UniqueViolationError:
                        await db.select_user(user_id=int(user_id))
                    except Exception as e:
                                await bot.send_message(ADMINS[0],text=f"Xatolik yuz berdi::Check_Phone_Number:170{e}")

            await dp.current_state(user=user_id).set_state(RegisterState.PhoneNumber)
            
        raise CancelHandler()