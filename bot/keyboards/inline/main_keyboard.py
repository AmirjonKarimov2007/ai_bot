from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram import types
from loader import db,dp,bot


def editable_keyboards(service):
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(InlineKeyboardButton(text="Mavzu",callback_data=f"change_theme:{service}"))
    markup.insert(InlineKeyboardButton(text="Institus",callback_data=f"change_univer:{service}"))
    markup.add(InlineKeyboardButton(text="Muallif",callback_data=f"change_author:{service}"))
    markup.insert(InlineKeyboardButton(text="Til",callback_data=f"change_language:{service}"))
    markup.add(InlineKeyboardButton(text="➕",callback_data=f"change_theme:{service}"))
    markup.insert(InlineKeyboardButton(text="Sahifalar soni",callback_data=f"change_theme:{service}"))
    markup.insert(InlineKeyboardButton(text="➖",callback_data=f"change_theme:{service}"))
    markup.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"back_to_{service}"))
    return markup

def success_keyboards(service):
    markup = InlineKeyboardMarkup(3)
    markup = InlineKeyboardMarkup(row_width=3)
    markup.insert(InlineKeyboardButton(text="✅Tayyorlash",callback_data=f"success:{service}"))
    markup.insert(InlineKeyboardButton(text="🚫Rad qilish",callback_data=f"cancel:{service}"))
    markup.insert(InlineKeyboardButton(text="✏️O'zgartirish",callback_data=f"edit:{service}"))
    return markup