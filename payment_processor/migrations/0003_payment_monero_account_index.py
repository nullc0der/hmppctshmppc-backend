# Generated by Django 3.0.2 on 2021-07-23 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_processor', '0002_payment_raw_tx_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='monero_account_index',
            field=models.IntegerField(null=True),
        ),
    ]
