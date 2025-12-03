from keyboards.inline.main_menu_super_admin import edit_services_prices
import re
import time
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters import IsSuperAdmin
from keyboards.inline.main_menu_super_admin import main_menu_for_super_admin, back_to_main_menu
from loader import dp, db, bot
from states.admin_state import SuperAdminState
from keyboards.inline.main_menu_super_admin import settings_menu_for_super_admin,back_settings

# ADMIN TAYORLASH VA CHIQARISH QISMI UCHUN
@dp.callback_query_handler(IsSuperAdmin(), text="add_admin", state="*")
async def add_admin(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Yangi adminni chat IDsini yuboring...\n"
                                 "🆔 Admin ID raqamini olish uchun @userinfobot ga /start bosishini ayting",
                                 reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_ADD_ADMIN.set()

@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_ADD_ADMIN)
async def add_admin_method(message: types.Message, state: FSMContext):
    admin_id =message.text
    await state.update_data({"admin_id": admin_id})
    await message.answer("👨🏻‍💻 Yangi admin ismini yuborin",
                                 reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_ADD_FULLNAME.set()


@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_ADD_FULLNAME)
async def add_admin_method(message: types.Message,state: FSMContext):
    try:
        royxat = await db.select_admins()
        full_name = message.text
        await state.update_data({"full_name": full_name})
        malumot = await state.get_data()
        # Dasturchi @Amirjon Karimov kanla @Amirjon_Karimov_Blog
        adminid = malumot.get("admin_id")
        full_name = malumot.get("full_name")
        try:
            if adminid not in royxat:
                await db.add_admin(user_id=int(adminid), full_name=full_name)
                await bot.send_message(chat_id=adminid,text="tabriklaymiz siz botimizda adminlik huquqini qolgan kiritidingiz /start bosing.")
                await message.answer("✅ Yangi admin muvaffaqiyatli qo'shildi!", reply_markup=main_menu_for_super_admin)
                await state.finish()

        except Exception as e:
            await message.answer("Adminni qo'shishda muammo yuz berdi.Admin botga start bosganligi yoki botni bloklamganligiga ishonch hozil qiling.")
            await state.finish()

    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi!", reply_markup=main_menu_for_super_admin)
        await state.finish()

@dp.callback_query_handler(IsSuperAdmin(), text="del_admin", state="*")
async def show_admins(call: types.CallbackQuery):

    await call.answer(cache_time=2)
    admins = await db.select_all_admins()
    buttons = InlineKeyboardMarkup(row_width=1)
    for admin in admins:
        buttons.insert(InlineKeyboardButton(text=f"{admin[2]}", callback_data=f"admin:{admin[1]}"))
    # Dasturchi @Amirjon Karimov kanla @Amirjon_Karimov_Blog
    buttons.add(InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="add_admin"))
    buttons.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu"))
    await call.message.edit_text(text="👤 Adminlar", reply_markup=buttons)
    

@dp.callback_query_handler(IsSuperAdmin(), text_contains="admin:", state="*")
async def del_admin_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    admin = await db.select_all_admin(user_id=int(data[1]))
    for data in admin:
        text = f"Sizning ma'lumotlaringiz\n\n"
        text += f"<i>👤 Admin ismi :</i> <b>{data[2]}\n</b>"
        text += f"<i>🆔 Admin ID raqami :</i> <b>{data[1]}</b>"
        buttons = InlineKeyboardMarkup(row_width=1)

        buttons.insert(InlineKeyboardButton(text="❌ Admindan bo'shatish", callback_data=f"deladm:{data[1]}"))
        buttons.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admins"))

        await call.message.edit_text(text=text, reply_markup=buttons)

@dp.callback_query_handler(IsSuperAdmin(), text_contains="deladm:", state="*")
async def del_admin_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    delete_orders = await db.delete_admin(admin_id=int(data[1]))
    await bot.send_message(chat_id=data[1],
                           text="Sizdan adminlik huquqi olindi")

    await call.answer("🗑 Admin o'chirildi !",show_alert=True)
    await call.message.edit_text("✅ Admin muvaffaqiyatli o'chirildi!", reply_markup=main_menu_for_super_admin)


# ADMIN TAYORLASH VA CHIQARISH QISMI UCHUN

# MAJBURIY OBUNA SOZLASH UCHUN
@dp.callback_query_handler(text = "add_channel")
async def add_channel(call: types.CallbackQuery):
    await SuperAdminState.SUPER_ADMIN_ADD_CHANNEL.set()
    await call.message.edit_text(text="<i><b>📛 Kanal usernamesini yoki ID sini kiriting: </b></i>")
    await call.message.edit_reply_markup(reply_markup=back_to_main_menu)


@dp.message_handler(IsSuperAdmin(),state=SuperAdminState.SUPER_ADMIN_ADD_CHANNEL)
async def add_channel(message: types.Message, state: FSMContext):
    matn = message.text
    if matn.isdigit() or matn.startswith("@") or matn.startswith("-"):
        try:
            if await db.check_channel(channel=message.text):
                await message.answer("<i>❌Bu kanal qo'shilgan! Boshqa kanal qo'shing!</i>", reply_markup=back_to_main_menu)
            else:
                try:
                    deeellll = await bot.send_message(chat_id=message.text, text=".")
                    await bot.delete_message(chat_id=message.text, message_id=deeellll.message_id)
                    try:
                        await db.add_channel(channel=message.text)
                    except:
                        pass
                    await message.answer("<i><b>Channel succesfully added ✅</b></i>")
                    await message.answer("<i>Siz admin panelidasiz. 🧑‍💻</i>", reply_markup=main_menu_for_super_admin)
                    await state.finish()
                except:
                    await message.reply("""<i><b>
Bu kanalda admin emasman!⚙️
Yoki siz kiritgan username ga ega kanal mavjud emas! ❌
Kanalga admin qilib qaytadan urinib ko'ring yoki to'g'ri username kiriting.🔁
                    </b></i>""", reply_markup=back_to_main_menu)
        except Exception as err:
            await message.answer(f"Xatolik ketdi: {err}")
            await state.finish()
    else:
        await message.answer("Xato kiritdingiz.", reply_markup=back_to_main_menu)

@dp.callback_query_handler(text="del_channel")
async def channel_list(call: types.CallbackQuery):
    royxat = await db.select_channels()
    text = "🔰 Kanallar ro'yxati:\n\n"
    son = 0
    for o in royxat:
        son +=1
        text += f"{son}. {o[1]}\n💠 Username: {o[1]}\n\n"
    await call.message.edit_text(text=text)
    admins =await db.select_all_channels()
    buttons = InlineKeyboardMarkup(row_width=2)
    for admin in admins:
        buttons.insert(InlineKeyboardButton(text=f"{admin[1]}", callback_data=f"delchanel:{admin[1]}"))

    buttons.add(InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_channel"))
    buttons.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu"))
    await call.message.edit_text(text=text, reply_markup=buttons)

@dp.callback_query_handler(IsSuperAdmin(), text_contains="delchanel:", state="*")
async def del_admin_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    delete_orders = await db.delete_channel(channel=data[1])
    await call.answer("🗑 Channel o'chirildi !",show_alert=True)
    await call.message.edit_text("✅ Kanal muvaffaqiyatli o'chirildi!", reply_markup=main_menu_for_super_admin)

# ADMINLARNI KORISH
@dp.callback_query_handler(text="admins")
async def channel_list(call: types.CallbackQuery):
    royxat = await db.select_admins()
    text = "🔰 Adminlar ro'yxati:\n\n"
    son = 0
    for o in royxat:
        son +=1
        text += f"{son}. {o[2]}\nID : {o[1]}💠 Ismi: {o[2]}\n\n"
    await call.message.edit_text(text=text)

    buttons = InlineKeyboardMarkup(row_width=1)
    buttons.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu"))
    await call.message.edit_text(text=text, reply_markup=buttons)
# ADMINLARNI KORISH

# STATISKA KORISH UCHUN
import pytz

@dp.callback_query_handler(IsSuperAdmin(), text="statistics")
async def stat(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    uzbekistan_tz = pytz.timezone('Asia/Tashkent')
    import datetime

    datas = datetime.datetime.now(uzbekistan_tz)
    yil_oy_kun = datas.date() 
    soat_minut_sekund = f"{datas.hour}:{datas.minute}:{datas.second}" 

    daily_stat = await db.stat(timeframe="daily")  
    weekly_stat = await db.stat(timeframe="weekly") 
    monthly_stat = await db.stat(timeframe="monthly") 
    all_stat = await db.stat(timeframe="all") 

    stat_message = f"<b>👥 Bot foydalanuvchilari soni:</b>\n"
    stat_message += f"<b>🗓 Kunlik: {daily_stat} nafar</b>\n"
    stat_message += f"<b>📆 Haftalik: {weekly_stat} nafar</b>\n"
    stat_message += f"<b>📊 Oylik: {monthly_stat} nafar</b>\n"
    stat_message += f"<b>✅ Jami: {all_stat} nafar</b>\n"
    stat_message += f"<b>⏰ Soat: {soat_minut_sekund}</b>\n"
    stat_message += f"<b>🕔 Sana: {yil_oy_kun}</b>"

    inline_button = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("◀️ Orqaga", callback_data="back_to_main_menu")
    )

    await call.message.delete()
    await call.message.answer(stat_message, reply_markup=inline_button)


# ADMINGA SEND FUNC
@dp.callback_query_handler(IsSuperAdmin(), text="send_message_to_admins", state="*")
async def send_advertisement(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Reklamani yuboring...\n"
                                 "Yoki bekor qilish tugmasini bosing", reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_SEND_MESSAGE_TO_ADMINS.set()


@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_SEND_MESSAGE_TO_ADMINS,content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message,state: FSMContext):
    users = await db.stat_admins()
    users = str(users)
    await message.answer(f"📢 Reklama jo'natish boshlandi...\n"
                             f"📊 Adminlar soni: {users} ta\n"
                             f"🕒 Kuting...\n")
    user = await db.select_all_admins()

    for i in user:
        user_id= i['user_id']
        try:
            await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id,
                                    message_id=message.message_id,reply_markup=message.reply_markup, parse_mode=types.ParseMode.HTML)

            time.sleep(0.5)
        except Exception as e:
            print(e)


        await message.answer("✅ Reklama muvaffaqiyatli yuborildi!", reply_markup=main_menu_for_super_admin)
        await state.finish()

# ====================Foydalanuvchliar uchun SEND SUNC  ============================
@dp.callback_query_handler(IsSuperAdmin(), text="send_advertisement", state="*")
async def send_advertisement(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Reklamani yuboring...\n"
                                 "Yoki bekor qilish tugmasini bosing", reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_STATE_GET_ADVERTISEMENT.set()

from asyncio import Semaphore,gather
from asyncio import Semaphore, gather, sleep
import datetime


@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_STATE_GET_ADVERTISEMENT,
                    content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message, state: FSMContext):
    users = await db.stat(timeframe='all')
    user_list = await db.select_all_users()

    black_list = 0
    white_list = 0

    datas = datetime.now()
    boshlanish_vaqti = f"{datas.hour}:{datas.minute}:{datas.second}"

    start_msg = await message.answer(
        f"📢 Reklama jo'natish boshlandi...\n"
        f"📊 Foydalanuvchilar soni: {users} ta\n"
        f"🕒 Kuting...\n"
    )

    semaphore = Semaphore(15)
    errors = []

    # =============================
    # 1) — Bitta userga xabar yuborish
    # =============================
    async def try_send(user_id):
        nonlocal white_list, black_list

        async with semaphore:
            try:
                await bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id,
                    reply_markup=message.reply_markup
                )
                white_list += 1
                await sleep(0.05)
                return True

            except Exception as e:
                txt = str(e).lower()

                print(f"[ERROR] User: {user_id} | Xato: {e}")

                if "bot was blocked by the user" in txt:
                    black_list += 1
                    return True  
                if "user is deactivated" in txt:
                    black_list += 1 
                    return True      

                if "chat not found" in txt:
                    black_list += 1
                    return True

                if "too many requests" in txt:
                    return False  # retry

                return False


    # ==========================================
    # 2) — Retry funksiyasi (3 marotaba urinish)
    # ==========================================
    async def retry_failed_users(failed_users):
        retry_delays = [3, 1, 1]  # tez ishlashi uchun optimallashtirilgan

        for attempt, delay in enumerate(retry_delays, start=1):
            await sleep(delay)

            new_failed = []

            tasks = [try_send(user) for user in failed_users]
            results = await gather(*tasks)

            for idx, ok in enumerate(results):
                if not ok:
                    new_failed.append(failed_users[idx])

            failed_users = new_failed

            # progressni yangilash
            await bot.edit_message_text(
                chat_id=start_msg.chat.id,
                message_id=start_msg.message_id,
                text=(
                    f"📢 Reklama yuborilmoqda (retry {attempt})...\n"
                    f"👥 Jami: {users}\n"
                    f"✅ Yuborildi: {white_list}\n"
                    f"🚫 Bloklagan: {black_list}\n"
                    f"🔁 Qayta urinilayotgan: {len(failed_users)}\n"
                )
            )

            if not failed_users:
                break

        return failed_users  # oxirgi qolgani qaytadi

    # ================================
    # 3) — Barcha userlarga 1-turn yuborish
    # ================================
    failed = []
    batch_size = 100

    for i in range(0, len(user_list), batch_size):
        batch = user_list[i:i + batch_size]

        tasks = [try_send(user["user_id"]) for user in batch]
        results = await gather(*tasks)

        for idx, ok in enumerate(results):
            if not ok:
                failed.append(batch[idx]["user_id"])

        # progress
        await bot.edit_message_text(
            chat_id=start_msg.chat.id,
            message_id=start_msg.message_id,
            text=(
                f"📢 Reklama jo'natilmoqda...\n"
                f"👥 Jami: {users}\n"
                f"✅ Yuborildi: {white_list}\n"
                f"🚫 Bloklagan: {black_list}\n"
                f"🔁 Xato: {len(failed)}\n"
            )
        )

    # ===================================
    # 4) — Xato bo‘lganlarga qayta retry
    # ===================================
    final_failed = await retry_failed_users(failed)
    seriy_list = len(final_failed)

    # =====================
    # 5) — Yakuniy xabar
    # =====================
    data = datetime.now()
    tugash_vaqti = f"{data.hour}:{data.minute}:{data.second}"

    text = (
        f'<b>✅ Reklama yakunlandi!</b>\n\n'
        f'<b>⏰ Boshlangan: {boshlanish_vaqti}</b>\n'
        f'<b>👥 Yuborilgan: {white_list}</b>\n'
        f'<b>🚫 Bloklagan: {black_list}</b>\n'
        f'<b>🔖 Yuborilmagan (yakuniy xatolik): {seriy_list}</b>\n'
        f'<b>🏁 Tugagan: {tugash_vaqti}</b>\n'
    )

    await bot.delete_message(chat_id=start_msg.chat.id, message_id=start_msg.message_id)
    await message.answer(text, reply_markup=main_menu_for_super_admin)
    await state.finish()

# ==================== Foydalanuvchliar uchun SEND SUNC TUGADI ============================
#<><><><> ===================Post qo'shish=====================<><><><>
@dp.callback_query_handler(IsSuperAdmin(), text="add_post", state="*")
async def add_post(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("rasm va textdan iborat post yuboring...\n"
                                 "Yoki Orqaga tugmasini bosing", reply_markup=back_to_main_menu)
    
    await SuperAdminState.SUPER_ADMIN_ADD_POST.set()

from typing import List, Union
# @dp.message_handler(IsSuperAdmin(),state=SuperAdminState.SUPER_ADMIN_ADD_POST,
#                     content_types=types.ContentTypes.ANY)
# @dp.message_handler(is_media_group=True, content_types=types.ContentType.ANY)
# async def add_post_to_social(message: types.Message,state: FSMContext):

#     file = message.content_type
#     niamdir = message.content_type
#     users =  await db.stat()
#     admin_id = message.from_user.id
#     caption = message.caption
    
#     caption_entities = message.caption_entities
#     urls = []

#     for caption_entry in caption_entities:
#         if caption_entry.type == 'text_link':
#             urls.append(caption_entry.url)
#     users = str(users)
#     for x in users:
#         user = await db.select_all_users()
#         for i in user:
#             user_id = i['user_id']
#             try:
#                 await bot.copy_message(
#                     chat_id=user_id,
#                     from_chat_id=message.from_user.id,
#                     message_id=message.message_id,
#                     reply_markup=message.reply_markup
#                 )

#                 time.sleep(0.5)
#             except Exception as e:
#                 await bot.send_message(admin_id, e)

#         # await message.answer("✅ Reklama muvaffaqiyatli yuborildi!", reply_markup=main_menu_for_super_admin)
    
#     channels = await db.channel_stat()
#     channels = str(channels)

#     for y in channels:

#         await message.answer(f"📢 Reklama jo'natish boshlandi...\n"
#                              f"📊 Foydalanuvchilar soni: {x} ta\n"
#                              f"📌 Kanallar soni: {y} ta\n"
#                              f"🕒 Kuting...\n")
#         channels = await db.select_all_channels()
#         for i in channels:
#             channel=i['channel']
#             channel_info = await bot.get_chat(channel)
#             channel = channel_info.id
#             try:
#                 await bot.copy_message(chat_id=channel, from_chat_id=admin_id,
#                                        message_id= message.message_id,reply_markup=message.reply_markup, parse_mode=types.ParseMode.HTML)
                
                
#                 time.sleep(0.5)
#             except Exception as e:
#                 await bot.send_message(admin_id,e)
#         await message.answer("✅ Reklama muvaffaqiyatli yuborildi!", reply_markup=main_menu_for_super_admin)
# # =================== ADD POST ON INSTAGRAM =================================
#         file_type = message.content_type
#         if file_type=='photo':
#             photo = message.photo[-1]
#             file_id = photo.file_id
#             caption = f"\n{message.caption}\n"
#             rasm = await upload_instagram(content_type=file_type,file_id=file_id,photo=photo,caption=caption)


#     await state.finish()


#Media group uchun handler yozdim

# Bot Edit Section
@dp.callback_query_handler(IsSuperAdmin(),text='settings',state='*')
async def settings(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("<b>✏️Nimani o'zgartirmoqchisiz</b>",reply_markup=settings_menu_for_super_admin)


def get_telegram_ids(url):
    pattern = r"https?://t\.me/c/(\d+)/(\d+)"
    match = re.match(pattern, url)
    if match:
        chat_id = match.group(1)
        message_id = match.group(2)
        return f"-100{chat_id}", message_id
    return None, None


# Premium olish uchun handlerlar


# @dp.callback_query_handler(IsSuperAdmin(),text='edit_premium')
# async def edit_premium(call: types.CallbackQuery):
#     await call.answer(cache_time=1)
#     await call.message.edit_text('🟪Premium Olish potini o\'zgartirish uchun,post kanaldan linkini olib menga  yuboring.',reply_markup=back_to_main_menu)
#     await SuperAdminState.SUPER_ADMIN_UPDATE_PREMIUM.set()
# import json
# @dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_PREMIUM)
# async def edit__premium(message: types.Message,state:FSMContext):
#     url = message.text
#     channel_id, message_id = get_telegram_ids(url)
       
#     if channel_id and message_id:
#         with open('data.json', 'r') as file:
#             data = json.load(file) 
    
#         if data['primum_post']['message_id'] and data['primum_post']['from_chat_id']:
#             data['primum_post']['message_id']= message_id
#             data['primum_post']['from_chat_id']= channel_id
#             with open('data.json', 'w') as file:
#                 json.dump(data, file, indent=4)
#             await message.answer(text='<b>✅Premium Posti yangilandi</b>',reply_markup=main_menu_for_super_admin)
#             await state.finish()

#         else:
#             await message.answer(text='<b>❌Premium Posti yangilanmadi</b>',reply_markup=main_menu_for_super_admin)
#             await state.finish()
#     else:
#         await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
#         await state.finish()

# Narx uchun handler
@dp.callback_query_handler(IsSuperAdmin(),text='edit_narx')
async def edit_premium(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Xizmat Narxlari uchun postni kanalga olib menga linkini yuboring.',reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_UPDATE_PREMIUM_PRICE.set()

@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_PREMIUM_PRICE)
async def edit__premium(message: types.Message,state:FSMContext):
    url = message.text
    channel_id, message_id = get_telegram_ids(url)
       
    if channel_id and message_id:
        with open('data.json', 'r') as file:
            data = json.load(file) 
    
        if data['premium_price']['message_id'] and data['premium_price']['from_chat_id']:
            data['premium_price']['message_id']= message_id
            data['premium_price']['from_chat_id']= channel_id
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            await message.answer(text='<b>✅Xizmat Narxlari yangilandi</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()

        else:
            await message.answer(text='<b>❌Xizmat Narxlari yangilanmadi</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()
    
# Qo'llanma uchun handler


@dp.callback_query_handler(IsSuperAdmin(),text='edit_qollanma')
async def edirt_qollanma(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('📄Qo\'llanma  uchun postni kanalga olib menga linkini yuboring.',reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_UPDATE_QOLLANMA.set()

import json
@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_QOLLANMA)
async def edirt__qollanma(message: types.Message,state:FSMContext):
    url = message.text
    channel_id, message_id = get_telegram_ids(url)
       
    if channel_id and message_id:
        with open('data.json', 'r') as file:
            data = json.load(file) 
    
        if data['get_qollanma']['message_id'] and data['get_qollanma']['from_chat_id']:
            data['get_qollanma']['message_id']= message_id
            data['get_qollanma']['from_chat_id']= channel_id
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            await message.answer(text='<b>✅Qo\'llanma  yangilandi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()

        else:
            await message.answer(text='<b>❌Qo\'llanma  yangilanmadi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()




# <><><><><><><<><><><><><<><<<<>><<><>><<>><><<>><<><><><><><><><><><><>
# ADMIN UCHUN HANDLERLAR

@dp.callback_query_handler(IsSuperAdmin(),text='edit_admin')
async def edirt_administator(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('🧑‍💻Adminni uchun postni kanalga olib menga linkini yuboring.',reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_UPDATE_ADMINS.set()

@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_ADMINS)
async def edirt__administator(message: types.Message,state:FSMContext):
    url = message.text
    channel_id, message_id = get_telegram_ids(url)
       
    if channel_id and message_id:
        with open('data.json', 'r') as file:
            data = json.load(file) 
    
        if data['administator']['message_id'] and data['administator']['from_chat_id']:
            data['administator']['message_id']= message_id
            data['administator']['from_chat_id']= channel_id
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            await message.answer(text='<b>✅Adminni post yangilandi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()

        else:
            await message.answer(text='<b>❌✅Admin post  yangilanmadi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()




# Start uchun handlerlar





# Referalning Qiymatini o'zgartirish
from keyboards.inline.main_menu_super_admin import edit_price_button
@dp.callback_query_handler(IsSuperAdmin(),text='edit_ref_sum')
async def edirt_starts(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('<b>Qaysi narxni o\'zgartirmoqchisiz?</b>',reply_markup=edit_price_button)






@dp.callback_query_handler(IsSuperAdmin(),text='edit_price_normal')
async def edit_price_normal(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    
    await call.message.edit_text('💴Oddiy Referal Narxini menga yuboring va uni joriy qilaman.\n\nEtibor bering faqat raqamlardan tashkil topsin va va belgilardan iborat bo\'lmasin',reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_UPDATE_REF_SUM_NORMAL.set()

@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_REF_SUM_NORMAL)
async def edit_price__normal(message: types.Message,state:FSMContext):
    ref_sum = message.text
    if ref_sum and ref_sum.isdigit():
        with open('data.json', 'r') as file:
            data = json.load(file) 
        if data['price']['normal_price']:
            data['price']['normal_price'] = ref_sum
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            await message.answer(text='<b>✅Normal Referal Summasi yangilandi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()

        else:
            await message.answer(text='<b>❌Normal Referal Summasiyangilanmadi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()

@dp.callback_query_handler(IsSuperAdmin(),text='edit_service_premium')
async def edit_price_premium(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('💎Premium Referal Narxini menga yuboring va uni joriy qilaman.\n\nEtibor bering faqat raqamlardan tashkil topsin va va belgilardan iborat bo\'lmasin',reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_UPDATE_REF_SUM_PREMIUM.set()

@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_REF_SUM_PREMIUM)
async def edit_price__premium(message: types.Message,state:FSMContext):

    ref_sum = message.text
    if ref_sum and ref_sum.isdigit():
        with open('data.json', 'r') as file:
            data = json.load(file) 
        if data['price']['premium_price']:
            data['price']['premium_price'] = ref_sum
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            await message.answer(text='<b>✅Premium Referal Summasi yangilandi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()

        else:
            await message.answer(text='<b>❌Premium  Referal Summasi yangilanmadi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()


# Premium narxlarini o'zgartirish
@dp.callback_query_handler(IsSuperAdmin(),text='edit_services_prices')
async def edit_primium_prices(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Qaysi Xizmat o\'zgartirmoqchisiz?',reply_markup=edit_services_prices())
    
@dp.callback_query_handler(IsSuperAdmin(),text_contains="select_service_package:")
async def select_service_of_ai(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    package = call.data.rsplit(":")[1]
    with open('data.json', 'r') as file:
        data = json.load(file)
    services_prices = data['services'][package]
    markup =  InlineKeyboardMarkup(row_width=1)
    for k,v in services_prices.items():
        markup.add(InlineKeyboardButton(text=f"{int(k)-5}-{k}->{v} so'm",callback_data=f'services_edit:{package}:{k}'))
    markup.insert(InlineKeyboardButton(text=f"⬅️Orqaga",callback_data=f"edit_services_prices"))
    await call.message.edit_text("Iltimos endi o'zgartimoqchi bo'lgan xizmatingizning tarifnini tanlang!",reply_markup=markup)




@dp.callback_query_handler(IsSuperAdmin(),text_contains='services_edit:')
async def edit_premium__price(call: types.CallbackQuery,state: FSMContext):
    await state.finish()
    await call.answer(cache_time=1)
    dataa = call.data.rsplit(":")
    service = dataa[1]
    package = dataa[2]
    if service and package:
        await state.update_data({'service':service,
                                 'package':package
                                 })
        await call.message.edit_text('💎Xizmat Narxini menga yuboring va uni joriy qilaman.\n\nEtibor bering faqat raqamlardan tashkil topsin va va belgilardan iborat bo\'lmasin',reply_markup=back_to_main_menu)
        await SuperAdminState.SUPER_ADMIN_UPDATE_SUM_PREMIUM_MONTH.set()

@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_SUM_PREMIUM_MONTH)
async def change_premium(message: types.Message,state:FSMContext):
    service_data = await state.get_data()
    price = message.text
    if price and price.isdigit():
        service = service_data.get('service')
        package = service_data.get('package')
        with open('data.json','r') as file:
            data = json.load(file)
        if service and service:
            data['services'][service][package]=price
            with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
            await message.answer(text=f'<b>✅{service.title()} Xizmat  Narxi yangilandi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
        else:
            await message.answer(text='<b>❌Xizmat  Narxi yangilanmadi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()



    
    








# Promocode Promocode Promocode Promocode Promocode


@dp.callback_query_handler(IsSuperAdmin(),text='create_new_promo_code',state='*')
async def create_new_promocode(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    try:
        text = "<b>Qanday turdagi PromoCode yaratmoqchisiz?</b>"
        markup = InlineKeyboardMarkup(row_width=2)
        markup.insert(InlineKeyboardButton(text="🔒Maxfiy",callback_data="create_private_promocode"))
        markup.insert(InlineKeyboardButton(text="👥Ommaviy",callback_data="create_public_promocode"))
        markup.insert(InlineKeyboardButton(text="⬅️Orqaga",callback_data="back_to_main_menu"))
        await call.message.edit_text(text=text,reply_markup=markup)
    except Exception as e:
        await call.message.answer(f"Botda xatolik yuz berdi:{e},superadmin.py line 785")

from data.config import ADMINS
@dp.callback_query_handler(IsSuperAdmin(),text='create_private_promocode',state='*')
async def private_promocode(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    try:
        text = "<b>Yaxshi Maxfiy promoCode necha kishilik bo'lishi va nech puldan bo'lishini yuboring.`Odamlar Soni`,`PromoCode Qiymati`,`Necha Kun Amal qilishi`\nMisol uchun: 1,1000,5</b>"
        markup = InlineKeyboardMarkup(row_width=1)
        markup.insert(InlineKeyboardButton(text="⬅️Orqaga",callback_data="create_new_promo_code"))
        await call.message.edit_text(text=text,reply_markup=markup)
        await SuperAdminState.CREATE_PRIVATE_PROMOCODE.set()
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0],text=e)
        await call.message.answer('Botda xatolik yuz berdi.Boshqatdan urinib koring')


from main import generate_unique_promo_code
from datetime import datetime, timedelta
async def check_date(input_date: str) -> bool:
    try:
        date_to_check = datetime.strptime(input_date, "%Y-%m-%d")
    except ValueError:
        return False
    today = datetime.today()

    if date_to_check >= today:
        return True
    else:
        return False
    

    
from utils.promocode_api import promocode_service

@dp.message_handler(IsSuperAdmin(), content_types=types.ContentType.TEXT, state=SuperAdminState.CREATE_PRIVATE_PROMOCODE)
async def generate_promo_code_for_private(message: types.Message, state: FSMContext):
    data = message.text.rsplit(",")
    
    # Ma'lumotlar sonini tekshirish
    if len(data) < 3:
        await message.answer("Iltimos, to'g'ri formatda kiriting: Odamlar soni, PromoCode Narxi")
        return

    person_count = data[0].strip()
    promo_price = data[1].strip()
    end_day_count = data[2].strip()
    today = datetime.today()

    end_date = today + timedelta(days=int(end_day_count))
    # Kiritilgan qiymatlarni tekshirish
    if not person_count.isdigit() or not end_day_count.isdigit() or not promo_price.isdigit() or int(person_count) <= 0 or int(promo_price) <= 0:
        await message.answer("Iltimos, musbat sonlarni kiriting: <Odamlar soni>, <PromoCode Narxi>")
        return

    promo_code = generate_unique_promo_code()

    
    timeNow = datetime.now()
    promocode_service.create_promocode(code=promo_code,start_date=timeNow,end_date=end_date,used_count=int(person_count),price=int(promo_price))
    # Faylga yozish
    # with open('promo_codes.json', 'w') as file:
    #     json.dump(promo_data, file, indent=4)

    await message.answer(f"Maxfiy PromoCodingiz Muvaffaqiyatli yaratildi: <code>{promo_code}</code>")
    await state.finish()
 




@dp.callback_query_handler(IsSuperAdmin(),text='create_public_promocode',state='*')
async def public_promocode(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    try:
        text = "<b>Yaxshi Ommaviy(Public) promoCode necha kishilik bo'lishi va nech puldan bo'lishini yuboring.`Odamlar Soni`,`PromoCode Qiymati`,`Necha Kun Amal qilishi`\nMisol uchun: 1,1000,5</b>"
        markup = InlineKeyboardMarkup(row_width=1)
        markup.insert(InlineKeyboardButton(text="⬅️Orqaga",callback_data="create_new_promo_code"))
        await call.message.edit_text(text=text,reply_markup=markup)
        await SuperAdminState.CREATE_PUBLIC_PROMOCODE.set()
    except:
        await call.message.answer('Botda xatolik yuz berdi.Boshqatdan urinib koring')

from data.config import PROMOCODE_CHANNEL
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@dp.message_handler(IsSuperAdmin(), content_types=types.ContentType.TEXT, state=SuperAdminState.CREATE_PUBLIC_PROMOCODE)
async def generate_promo_code_for_public(message: types.Message, state: FSMContext):
    data = message.text.rsplit(",")

    
    if len(data) < 3:
        await message.answer("Iltimos, to'g'ri formatda kiriting: Odamlar soni, PromoCode Narxi")
        return

    person_count = data[0].strip()
    promo_price = data[1].strip()
    end_day_count = data[2].strip()
    today = datetime.today()

    end_date = today + timedelta(days=int(end_day_count))

    if not person_count.isdigit() or not promo_price.isdigit() or int(person_count) <= 0 or int(promo_price) <= 0:
        await message.answer("Iltimos, musbat sonlarni kiriting: <Odamlar soni>, <PromoCode Narxi>")
        return

    promo_code = generate_unique_promo_code()

    timeNow = datetime.now()
    promocode_data = promocode_service.create_promocode(code=promo_code,start_date=timeNow,end_date=end_date,used_count=int(person_count),price=int(promo_price),status='public')



   
    users_count = 0
    max_count = promocode_data['used_count']
    bosh_joylar = max_count - users_count

    text = (
        f"🎟 Promokod: <code>{promo_code}</code>\n"
        f"💰 Qiymat: <b>{promo_price}</b>\n"
        f"💰 Foydalanishlar soni: <b>{users_count}</b>\n"
        f"🗂 Bo'sh Joylar soni: <b>{bosh_joylar}</b>\n"
    )

    markup = InlineKeyboardMarkup(row_width=1)
    bot_name = (await bot.get_me()).username
    markup.insert(InlineKeyboardButton(text="🤖 Botga o'tish", url=f"t.me/{bot_name}"))

    await message.answer(f"✅ Ommaviy PromoCodingiz muvaffaqiyatli yaratildi: <code>{promo_code}</code>")
    xabar = await bot.send_message(chat_id=PROMOCODE_CHANNEL, text=text, reply_markup=markup)
    promocode_service.update_promocode(promocode_id=promocode_data['id'],
                                        code=promo_code,
                                       start_date=timeNow,
                                       end_date=end_date,
                                       message_id = xabar.message_id,
                                       used_count=int(person_count),
                                       price=int(promo_price))
    
    await state.finish()






# Bosh menu
@dp.callback_query_handler(IsSuperAdmin(), text="back_to_main_menu", state="*")
async def back_to_main_menu_method(call: types.CallbackQuery,state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text(text="👨‍💻 Bosh menyu", reply_markup=main_menu_for_super_admin)
    await state.finish()
