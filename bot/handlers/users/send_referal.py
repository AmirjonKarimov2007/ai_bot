from aiogram import types
from loader import dp, bot
from aiogram.utils.deep_linking import get_start_link

@dp.message_handler(text="🌟 Pul Olish")
async def Money(message: types.Message):
    user_id =message.from_user
    link = await get_start_link(user_id.id)
    bot_get = await bot.get_me()
    await message.answer_photo(photo='https://aifreebox.com/_next/image?url=https%3A%2F%2Fcdn.aifreebox.com%2Fwp-content%2Fuploads%2F2024%2F07%2Fthank-you-note.webp&w=828&q=75'
                               ,caption="<b>✅ Eyyy! Siz hali ham referat,mustaqil ish va slaydlarni qo'lda tayyorlayapsizmi??!</b>\n\n"
                                f"➡️ Va bu ishga ko'p vaqt sariflayapsizmi?\n\n"
                                f"➡️ Endi buni tekinga oson va tez vaqtda qilishingiz mumkin.\n\n"
                                f"➡️ Shunchaki botga start bosing va berilgan havola orqali doʻstlaringizni taklif qiling. Evaziga bot sizga pul beradi. Oʻsha pullarni 📑 Referat,📃 Mustaqil ish va 🏞 Slaydlar uchun ishlating!\n\n"
                                f"Pastdagi havola orqali doʻstlaringizga ulashing:\n"
                                f"<b>🔗 {link}</b>",reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Ulashish ♻️", url=f"https://t.me/share/url?url={link}")))