# Generated by Django 3.0.2 on 2022-01-05 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ekatagp', '0001_initial'),
        ('core_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statssnapshot',
            name='payment_form',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statssnapshot', to='ekatagp.PaymentForm'),
        ),
    ]