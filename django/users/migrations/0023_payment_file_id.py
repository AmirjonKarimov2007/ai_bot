# Generated by Django 5.0 on 2024-12-28 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_payment_invoice_alter_payment_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='file_id',
            field=models.CharField(default='', max_length=500, verbose_name='Fullname'),
            preserve_default=False,
        ),
    ]