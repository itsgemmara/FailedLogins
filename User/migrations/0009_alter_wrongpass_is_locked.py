# Generated by Django 4.0.3 on 2022-03-17 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_rename_is_active_wrongpass_is_locked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wrongpass',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
    ]