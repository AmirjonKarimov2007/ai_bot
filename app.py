import requests

class PromocodeService:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_promocode(self, code, price, start_date, end_date, used_count=0, is_active=True):
        url = f'{self.base_url}/api/promocodes/'
        data = {
            'code': code,
            'price': price,
            'start_date': start_date,
            'end_date': end_date,
            'used_count': used_count,
            'is_active': is_active
        }
        response = requests.post(url, data=data)

        if response.status_code == 201:
            print('Promocode created successfully:', response.json())
            return response.json()  # Return the created promocode data
        else:
            print('Failed to create promocode:', response.status_code, response.text)
            return None

    def get_promocode(self, promocode_id):
        url = f'{self.base_url}/api/promocodes/{promocode_id}/'
        response = requests.get(url)

        if response.status_code == 200:
            print('Promocode details:', response.json())
        else:
            print('Failed to fetch promocode:', response.status_code, response.text)

    def update_promocode(self, promocode_id, code, price, start_date, end_date, used_count=0, is_active=True):
        url = f'{self.base_url}/api/promocodes/{promocode_id}/'
        data = {
            'code': code,
            'price': price,
            'start_date': start_date,
            'end_date': end_date,
            'used_count': used_count,
            'is_active': is_active
        }
        response = requests.put(url, data=data)

        if response.status_code == 200:
            print('Promocode updated successfully:', response.json())
        else:
            print('Failed to update promocode:', response.status_code, response.text)

    def delete_promocode(self, promocode_id):
        url = f'{self.base_url}/api/promocodes/{promocode_id}/'
        response = requests.delete(url)

        if response.status_code == 204:
            print('Promocode deleted successfully')
        else:
            print('Failed to delete promocode:', response.status_code, response.text)

    def activate_promocode(self, promocode_id, user_token):
        url = f'{self.base_url}/api/promocodes/{promocode_id}/activate/'
        headers = {
            'Authorization': f'Token {user_token}'  # Foydalanuvchi tokeni bilan autentifikatsiya
        }
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            print('Promocode activated successfully:', response.json())
        else:
            print('Failed to activate promocode:', response.status_code, response.text)

    def create_promocode_usage(self, user_id, promocode_id):
        url = f'{self.base_url}/api/promocode-usage/'
        data = {
            'user': user_id,
            'promocode': promocode_id
        }
        response = requests.post(url, data=data)

        if response.status_code == 201:
            print('Promocode usage created successfully:', response.json())
        else:
            print('Failed to create promocode usage:', response.status_code, response.text)

    def get_promocode_usage(self, promocode_usage_id):
        url = f'{self.base_url}/api/promocode-usage/{promocode_usage_id}/'
        response = requests.get(url)

        if response.status_code == 200:
            print('Promocode usage details:', response.json())
        else:
            print('Failed to fetch promocode usage:', response.status_code, response.text)

# URL bazasi (o'z serveringizga moslab o'zgartiring)
base_url = 'http://127.0.0.1:8000'

# Servisni yaratamiz
promocode_service = PromocodeService(base_url)

# 1. Promocode yaratish
response = promocode_service.create_promocode(
    code='PROMO2025_NEW',
    price=1000,
    start_date='2025-05-01T00:00:00Z',
    end_date='2025-06-01T00:00:00Z'
)

# Agar promocode muvaffaqiyatli yaratildi, undan IDni olish

promocode_id = 8


# 2. Promocode haqida ma'lumot olish
if promocode_id:
    promocode_service.get_promocode(promocode_id=promocode_id)

# 3. Promocode yangilash
if promocode_id:
    promocode_service.update_promocode(
        promocode_id=promocode_id,
        code='PROMO2025_UPDATED_code',
        price=15000,
        start_date='2025-05-01T00:00:00Z',
        end_date='2025-06-01T00:00:00Z'
    )

# if promocode_id:
#     # Foydalanuvchi tokeni bilan autentifikatsiya qilish
#     user_token = 'your_user_token_here'  # Tokenni o'zgartiring
#     promocode_service.activate_promocode(promocode_id=promocode_id, user_token=user_token)

# 6. Promocode usage yaratish
if promocode_id:
    promocode_service.create_promocode_usage(user_id=1, promocode_id=promocode_id)

# 7. Promocode usage haqida ma'lumot olish
promocode_service.get_promocode_usage(promocode_usage_id=1)
