# Generated by Django 4.0.3 on 2022-03-17 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_alter_block_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='count_of_wrong_pass',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='wrongpass',
            name='state',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='wrongpass',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]