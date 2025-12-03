from django.contrib import admin
from .models import User,Payment,Promocode,PromocodeUsage

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username','univer', 'user_id', 'number', 'balance', 'ref_father','created_date','updated_date','updated_date']
    list_filter = ['balance', 'ref_father', 'name','username','user_id','number','is_blocked'] 
admin.site.register(User, UserAdmin)



class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'is_active','start_date', 'end_date', 'used_count']
    list_filter = ['id', 'price', 'is_active','start_date', 'end_date', 'used_count']
admin.site.register(Promocode, PromoCodeAdmin)




class PromocodeUsageAdmin(admin.ModelAdmin):
    list_display = ['user', 'promocode', 'used_at']
    list_filter = ['user', 'promocode', 'used_at']
admin.site.register(PromocodeUsage, PromocodeUsageAdmin)




class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','username', 'user_id', 'number', 'balance', 'summa','updated_date','updated_date']
    list_filter = ['id', 'name','username', 'user_id', 'number', 'balance', 'summa','updated_date','updated_date']
admin.site.register(Payment, PaymentAdmin)
