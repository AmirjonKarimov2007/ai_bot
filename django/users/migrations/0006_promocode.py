# Generated by Django 5.0 on 2024-11-23 09:00

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_premium'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promo_code', models.CharField(max_length=20, unique=True)),
                ('package', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('unused', 'Unused'), ('used', 'Used')], default='unused', max_length=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promo_codes', to='users.user')),
            ],
        ),
    ]
