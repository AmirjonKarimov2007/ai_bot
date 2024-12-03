from django.contrib import admin
from .models import User,PromoCode

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username', 'user_id', 'number', 'balance', 'ref_father']
    list_filter = ['balance', 'ref_father', 'name','user_id','user_id'] 

admin.site.register(User, UserAdmin)
admin.site.register(PromoCode)