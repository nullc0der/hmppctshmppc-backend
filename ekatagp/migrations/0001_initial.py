# Generated by Django 3.0.2 on 2022-01-05 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_id', models.CharField(default='', max_length=100)),
                ('created_on', models.DateTimeField()),
                ('is_payment_success', models.BooleanField(default=False)),
                ('payment_payload', models.TextField()),
            ],
        ),
    ]
