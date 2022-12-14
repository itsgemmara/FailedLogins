# Generated by Django 4.0.3 on 2022-03-27 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0017_remove_ip_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnBlockCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('used', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('expired_at', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
