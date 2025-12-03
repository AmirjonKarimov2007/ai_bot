from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import json
check = InlineKeyboardMarkup(row_width=2)
check.insert(InlineKeyboardButton(text="✅Ha", callback_data='ha'))
check.insert(InlineKeyboardButton(text="❌Yo'q", callback_data='Yoq'))

get_premium_keyboard = InlineKeyboardMarkup(row_width=1)
get_premium_keyboard.insert(InlineKeyboardButton(text='Balansni to\'ldirish✅',callback_data="hisobni_toldirish"))

def service_keyboard(balance):
    # Tariflarga mos emoji tayyorlash

    
    premiums = InlineKeyboardMarkup(row_width=1)
    with open('data.json', 'r') as file:
        data = json.load(file)
    premium_prices = data['services']
    
    for k, v in premium_prices.items():
        v = int(v)
        if balance >= v: 
            premiums.insert(
                InlineKeyboardButton(
                    text=f"{k.replace('_', ' ')} - {v} so'm",  
                    callback_data=f"take_service:{k}"
                )
            )
    return premiums 