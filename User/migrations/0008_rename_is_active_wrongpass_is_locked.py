# Generated by Django 4.0.3 on 2022-03-17 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_alter_wrongpass_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wrongpass',
            old_name='is_active',
            new_name='is_locked',
        ),
    ]