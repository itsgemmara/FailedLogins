# Generated by Django 4.0.3 on 2022-03-16 08:45

import User.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', User.managers.CustomUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='block',
            name='count_of_wrong_pass',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='number_of_IP_blocking',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='number_of_user_blocking',
            field=models.IntegerField(null=True),
        ),
    ]