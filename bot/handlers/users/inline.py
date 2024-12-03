from loader import dp, bot, db
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.deep_linking import get_start_link
from data.config import ADMINS
import json
@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    query_text = query.query.strip()
    user_id = query.from_user.id
    username = await bot.get_me()
    username = username.username
    link = await get_start_link(user_id)
    if query_text == '':
        caption="<b>✅ Eyyy! Siz hali ham referat,mustaqil ish va slaydlarni qo'lda tayyorlayapsizmi??!</b>\n\n"\
                                f"➡️ Va bu ishga ko'p vaqt sariflayapsizmi?\n\n"\
                                f"➡️ Endi buni tekinga oson va tez vaqtda qilishingiz mumkin.\n\n"\
                                f"➡️ Shunchaki botga start bosing va berilgan havola orqali doʻstlaringizni taklif qiling. Evaziga bot sizga pul beradi. Oʻsha pullarni 📑 Referat,📃 Mustaqil ish va 🏞 Slaydlar uchun ishlating!\n\n"\
                                f"Pastdagi havola orqali doʻstlaringizga ulashing:\n"\
                                f"<b>🔗 {link}</b>"
        
        input_content = types.InputTextMessageContent(caption, disable_web_page_preview=True)
        inl = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ Boshlash ✅", url=f"{link}"))
        
        referal = types.InlineQueryResultArticle(
            id='01',
            thumb_url='https://aifreebox.com/_next/image?url=https%3A%2F%2Fcdn.aifreebox.com%2Fwp-content%2Fuploads%2F2024%2F07%2Fthank-you-note.webp&w=828&q=75',
            title="Do'stlarga yuborish 📲",
            description="Do'stlarga yuborish uchun shu yerni bosing",
            input_message_content=input_content,
            reply_markup=inl,
        )
        
        await query.answer(results=[referal], cache_time=1)
        return

    if query_text.isalnum() and query_text.isupper() and len(query_text) == 8:
        promo_code = await db.select_promocode(promo_code=query_text)
        str_user_id = str(query.from_user.id)
        if promo_code and int(user_id) == int(promo_code[0]['user_id']) and str_user_id not in ADMINS:

            promo_message = f"<b>🎉 Mening promo kodim: <code>{query_text}</code></b>\n\n" \
                            f"🚀 Bu promo kod yordamida botdagi  Xizmatlarni bepul yoki chegirmalar bilan olishim mumkinmi?!\n\n" \

            await query.answer(
                results=[
                    types.InlineQueryResultArticle(
                        id=query_text,
                        title='Promo kodni tekshirish',
                        thumb_url='https://as2.ftcdn.net/v2/jpg/05/33/75/35/1000_F_533753588_1krxEE0SDZWl0ZKd9cUzCL6HaTRo9UxK.jpg',
                        description='Adminga yuborish uchun shu yerni bosing',
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"{promo_message}"
                        ),
                    )
                ],
                cache_time=1
            )
            return
        elif promo_code and str(user_id) in ADMINS:
                package = promo_code[0]['package']
                with open('data.json','r') as file:
                    data = json.load(file)
                premium_price = data['premium_prices'][package]
                end_date = promo_code[0]['end_date']
                formatted_end_date = end_date.strftime('%Y-%m-%d %H:%M')
                
                premium_keyboard = InlineKeyboardMarkup(row_width=1)
                premium_keyboard.insert(InlineKeyboardButton(text="✅Xizmat Bajarildi", callback_data=f"premium_olindi:{promo_code[0]['promo_code']}"))

                promo_message = f"<b>{package.replace('_', ' ')}lik Xizmat Haqida Ma'lumot ✅</b>\n" \
                                f"Promo kod⏬⏬⏬\n<code>{query_text}</code>\n\n" \
                                f"💸Narxi: {str(premium_price)} so'm\n" \
                                f"🕔Yaroqlilik muddati: {formatted_end_date}\n\n" \
                                f"🍱Promo kodni adminga yuborish orqali Xizmatni qo'lga kiritishingiz mumkin.\n\n"

                await query.answer(
                    results=[
                        types.InlineQueryResultArticle(
                            id=query_text,
                            title='Promo kodni Tekshirish',
                            thumb_url='https://as2.ftcdn.net/v2/jpg/05/33/75/35/1000_F_533753588_1krxEE0SDZWl0ZKd9cUzCL6HaTRo9UxK.jpg',
                            description='Promo Kodni Tekshirish Uchun Bosing!',
                            input_message_content=types.InputTextMessageContent(
                                message_text=f"{promo_message}"
                            ),
                            reply_markup=premium_keyboard
                        )
                    ],
                    cache_time=1
                )


                return
    await query.answer(results=[], cache_time=1)


from filters.admins import IsSuperAdmin
@dp.callback_query_handler(IsSuperAdmin(),text_contains="premium_olindi:")
async def premium_olindi(call: types.CallbackQuery):
    data = call.data.rsplit(":")
    promo_code = data[1]
    try:
        if await db.select_promocode(promo_code=promo_code):
            await call.answer(cache_time=1)
            await db.delete_promo_code(promo_code=promo_code)
            await bot.send_message(chat_id=call.from_user.id,text=f"✅Promo Kod o'chirildi:{promo_code}")
        else:
            await call.answer("❌Bu Promo kop topilmadi,Oldin o'chirilgan.")
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0],text=f"Botda xatolik.inline.py:{e}")