# Generated by Django 3.0.2 on 2022-01-05 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ekatagp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatsSnapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stats', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('payment_form', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ekatagp.PaymentForm')),
            ],
        ),
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=32)),
                ('used_count', models.PositiveIntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('stats_snapshot', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core_api.StatsSnapshot')),
            ],
        ),
    ]
