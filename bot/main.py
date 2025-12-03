import uuid

generated_codes = set()

def generate_unique_promo_code(length=8):
    while True:
        promo_code = str(uuid.uuid4()).replace("-", "")[:length]  
        promo_code = promo_code.upper()  
        if promo_code not in generated_codes:
            generated_codes.add(promo_code)  
            return promo_code
        else:
            continue
