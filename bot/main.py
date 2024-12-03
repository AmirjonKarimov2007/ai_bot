import uuid

# Yaratilgan promo kodlar ro'yxati (set) - Takrorlanmaslikni ta'minlash uchun
generated_codes = set()

def generate_unique_promo_code(length=8):
    while True:
        # UUID yordamida tasodifiy promo kodni yaratish
        promo_code = str(uuid.uuid4()).replace("-", "")[:length]  # Berilgan uzunlikka moslashtirish
        promo_code = promo_code.upper()  # Katta harflarga o‘zgartirish
        if promo_code not in generated_codes:
            generated_codes.add(promo_code)  # Yangi kodni qo'shish
            return promo_code
        # Agar kod takrorlansa, yangi kod yaratish
        else:
            continue

promo_code = generate_unique_promo_code(length=8)
