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


