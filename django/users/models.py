from django.db import models

class User(models.Model):
    name = models.CharField(verbose_name='Fullname', max_length=100)
    username = models.CharField(verbose_name='Username', max_length=200, null=True,blank=True)
    user_id = models.BigIntegerField(verbose_name='Telegram_id', unique=True, default=1)
    balance = models.BigIntegerField(verbose_name='Balance',default=0,null=True,blank=True)
    number = models.BigIntegerField(verbose_name="Telefon raqami",null=True,blank=True)
    ref_father = models.BigIntegerField(verbose_name='ref_father',null=True,blank=True)
    register = models.BooleanField(default=False)
    def __str__(self):
        return self.name
from django.utils.timezone import now
from datetime import timedelta

class PromoCode(models.Model):
    user_id = models.BigIntegerField(verbose_name='Telegram_id')
    promo_code = models.CharField(max_length=20, unique=True)
    package = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=[('activate', 'Activate'), ('deactivate', 'Deactivate')], default='activate')
    created_at = models.DateTimeField(default=now)
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='Tugash sanasi va vaqti')

    def __str__(self):
        return f"Promo Code: {self.promo_code} | Status: {self.status}"
