from aiogram import types

class Keyboards:
    def main(self):
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        foydalanish = types.KeyboardButton("✅Foydalanish")
        referal = types.KeyboardButton("🌟 Pul Olish")
        topusers = types.KeyboardButton("TOP foydalanuvchilar")
        prices = types.KeyboardButton("💸 Xizmat Narxlari")
        balans = types.KeyboardButton("💳 Mening Hisobim")
        Manual = types.KeyboardButton("Qollanma 📄")
        Administrator = types.KeyboardButton("👨‍💻 Administrator")
        promocode = types.KeyboardButton("🔑Promo Kod")
        menu.add(foydalanish),menu.add(referal,topusers),menu.add(prices,balans),menu.add(promocode)
        return menu.add(Manual,Administrator)
    
    def contact(self):
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        contact = types.KeyboardButton("Raqamni yuborish 📞",request_contact=True)
        return menu.add(contact)

    def manual(self):
        menu = types.InlineKeyboardMarkup()
        ADMIN = types.InlineKeyboardButton("🧑‍💻Dasturchi",url="https://t.me/Amirjon_Karimov")
        return menu.add(ADMIN)
    def admin(self):
        menu = types.InlineKeyboardMarkup()
        ADMIN = types.InlineKeyboardButton("✅Boglanish",url="https://t.me/Amirjon_Karimov")
        return menu.add(ADMIN)
kb = Keyboards()