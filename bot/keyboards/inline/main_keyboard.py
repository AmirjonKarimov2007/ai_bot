from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram import types
from loader import db,dp,bot


def editable_keyboards(service):
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(InlineKeyboardButton(text="🗓Mavzu",callback_data=f"change_theme:{service}"))
    markup.insert(InlineKeyboardButton(text="🏫Institus",callback_data=f"change_univer:{service}"))
    markup.add(InlineKeyboardButton(text="👩‍🏫Muallif",callback_data=f"change_author:{service}"))
    markup.insert(InlineKeyboardButton(text="🌐Til",callback_data=f"change_language:{service}"))
    markup.add(InlineKeyboardButton(text="☘️Reja",callback_data=f"change_plan:{service}"))
    markup.add(InlineKeyboardButton(text="➖",callback_data=f"delete_page:{service}"))
    markup.insert(InlineKeyboardButton(text="📄Sahifalar soni",callback_data=f"see_page:{service}"))
    markup.insert(InlineKeyboardButton(text="➕",callback_data=f"add_page:{service}"))
    markup.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"back_to_:{service}"))
    return markup

def plans_keyboard(service):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="♻️ Auto Yangilash", callback_data=f"change_plan_auto:{service}"))
    markup.insert(InlineKeyboardButton(text="✍️ Qo'lda Yangilash(coming soon)", callback_data=f"change_plan_by_hand:{service}"))
    markup.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"edit:{service}"))
    return markup
def success_keyboards(service):
    markup = InlineKeyboardMarkup(3)
    markup = InlineKeyboardMarkup(row_width=3)
    markup.insert(InlineKeyboardButton(text="✅Tayyorlash",callback_data=f"success:{service}"))
    markup.insert(InlineKeyboardButton(text="🚫Rad qilish",callback_data=f"cancel:{service}"))
    markup.insert(InlineKeyboardButton(text="✏️O'zgartirish",callback_data=f"edit:{service}"))
    return markup

def success_keyboards_bayon(service):
    markup = InlineKeyboardMarkup(3)
    markup = InlineKeyboardMarkup(row_width=3)
    markup.insert(InlineKeyboardButton(text="✅Tayyorlash",callback_data=f"success:{service}"))
    markup.insert(InlineKeyboardButton(text="🚫Rad qilish",callback_data=f"cancel:{service}"))
    return markup



def prices_keybaord():
    prices = [1000,2000,3000,4000,5000,10000,20000,50000]
    markup = InlineKeyboardMarkup(row_width=2)
    for price in prices:
        markup.insert(InlineKeyboardButton(text=f"{str(price)} so'm",callback_data=f"select_user_payment:{price}"))
    markup.add(InlineKeyboardButton(text="❌Bekor qilish",callback_data=f"cancel_payment"))
    return markup
