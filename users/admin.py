from django.contrib import admin
from .models import User,Payment

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username','univer', 'user_id', 'number', 'balance', 'ref_father','created_date','updated_date','updated_date']
    list_filter = ['balance', 'ref_father', 'name','username','user_id','number','is_blocked'] 
admin.site.register(User, UserAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','username', 'user_id', 'number', 'balance', 'summa','updated_date','updated_date']
    list_filter = ['id', 'name','username', 'user_id', 'number', 'balance', 'summa','updated_date','updated_date']
admin.site.register(Payment, PaymentAdmin)
