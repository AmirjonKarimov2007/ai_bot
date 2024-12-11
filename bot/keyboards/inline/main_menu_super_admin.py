from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
main_menu_for_super_admin = InlineKeyboardMarkup(row_width=2)

main_menu_for_super_admin.add(InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_channel"),
                              InlineKeyboardButton(text="➖ Kanal o'chirish", callback_data="del_channel"),
                              InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="add_admin"),
                              InlineKeyboardButton(text="➖ Admin o'chirish", callback_data="del_admin"),
                              InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings"),
                              InlineKeyboardButton(text="👤 Adminlar", callback_data="admins"),
                              InlineKeyboardButton(text="📝 Adminlarga Xabar yuborish",callback_data="send_message_to_admins"),
                              InlineKeyboardButton(text="📝 Reklama Jo'natish", callback_data="send_advertisement"),
                              InlineKeyboardButton(text="📊 Statistika", callback_data="statistics"),
                              )
settings_menu_for_super_admin = InlineKeyboardMarkup(row_width=2)
settings_menu_for_super_admin.add(
    InlineKeyboardButton(text='💸Narxni o\'zgartirish',callback_data='edit_narx'),
    InlineKeyboardButton(text='📄Qo\'llanmani o\'zgartirish',callback_data='edit_qollanma'),
    InlineKeyboardButton(text='🧑‍💻Adminni o\'zgartirish',callback_data='edit_admin'),
    InlineKeyboardButton(text='💴Referal Narxini o\'zgartirish',callback_data='edit_ref_sum'),
    InlineKeyboardButton(text='💎Xizmat Narxlarini o\'zgartirish',callback_data='edit_services_prices'),
)
settings_menu_for_super_admin.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu"))

edit_price_button = InlineKeyboardMarkup(row_width=2)
edit_price_button.add(InlineKeyboardButton(text="✅Oddiy", callback_data="edit_price_normal"))
edit_price_button.add(InlineKeyboardButton(text="💎Premium", callback_data="edit_service_premium"))
edit_price_button.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="settings"))
# Premium Price

def edit_services_prices():
    # Tariflarga mos emoji tayyorlash
    services = InlineKeyboardMarkup(row_width=1)
    with open('data.json', 'r') as file:
        data = json.load(file)
    services_prices = data['services']
    
    for k, v in services_prices.items():
        services.insert(
            InlineKeyboardButton(
                text=f"{k.replace('_', ' ')} - {v} so'm", 
                callback_data=f"services_edit:{k}"
            )
        )
    services.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="settings"))
    
    return services




back_settings= InlineKeyboardMarkup(row_width=2)
back_settings.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="settings"))
# Admin Button
main_menu_for_admin = InlineKeyboardMarkup(row_width=2)
main_menu_for_admin.add(InlineKeyboardButton(text="📊 Statistika", callback_data="stat"))

# Back buttons
back_to_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu")
        ]
    ]
)
def services_keyboards__board():
    with open('data.json','r') as file:
        data = json.load(file)
    markup = InlineKeyboardMarkup(row_width=2)
    services = data['services']
    for k,v in services.items():
        markup.insert(InlineKeyboardButton(text=f"{k}",callback_data=f"select_service:{k}"))
    return markup