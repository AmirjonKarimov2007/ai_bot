from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta
class User(models.Model):
    name = models.CharField(verbose_name='Fullname', max_length=100)
    username = models.CharField(verbose_name='Username', max_length=200, null=True,blank=True)
    author = models.CharField(verbose_name='Mualif', max_length=200, null=True,blank=True)
    univer = models.CharField(verbose_name='Universitet', max_length=200, null=True,blank=True)
    LANGUAGE_CHOICES = [
        ('eng', 'English'),
        ('uzb', 'Uzbek'),
        ('rus', 'Russian'),
    ]
    
    language = models.CharField(
        max_length=3,
        choices=LANGUAGE_CHOICES,
        default='eng',
    )
    user_id = models.BigIntegerField(verbose_name='Telegram_id', unique=True)
    balance = models.BigIntegerField(verbose_name='Balance',default=0,null=True,blank=True)
    number = models.BigIntegerField(verbose_name="Telefon raqami",null=True,blank=True)
    ref_father = models.BigIntegerField(verbose_name='ref_father',null=True,blank=True)
    register = models.BooleanField(default=False,verbose_name='Register')
    is_premium = models.BooleanField(default=False,verbose_name="Premium")
    is_blocked = models.BooleanField(default=False,verbose_name="Blocklash")
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Yaratilgan sana")
    updated_date = models.DateTimeField(auto_now=True,verbose_name="O'zgartirilgan sana")
    def __str__(self):
        return self.name

class Promocode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    price = models.BigIntegerField(verbose_name='Promocode Price', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    used_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return str(self.code)

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date


class PromocodeUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User modeliga bog'lash
    promocode = models.ForeignKey(Promocode, on_delete=models.CASCADE, related_name="usage")
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('promocode', 'user')  # Bir foydalanuvchi faqat bitta promo-kodni bir marta ishlatishi kerak

    def __str__(self) -> str:
        return f"User {self.user.username} used {self.promocode.code}"
    



    
class Payment(models.Model):
    name = models.CharField(verbose_name='Fullname', max_length=100)
    username = models.CharField(verbose_name='Username', max_length=200, null=True,blank=True)
    user_id = models.BigIntegerField(verbose_name='Telegram_id')
    file_id = models.CharField(verbose_name='Chek_id', max_length=500)
    number = models.BigIntegerField(verbose_name="Telefon raqami")
    balance = models.BigIntegerField(verbose_name='Umummiy Balance',null=True,blank=True)
    summa = models.BigIntegerField(verbose_name='Tolov Miqtori')
    invoice = models.CharField(verbose_name='Invoice', max_length=100,unique=True)  # Make it unique for safety    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Yaratilgan sana")
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Yaratilgan sana")
    updated_date = models.DateTimeField(auto_now=True,verbose_name="O'zgartirilgan sana")
    def __str__(self) -> str:
        return str(self.username)
    


