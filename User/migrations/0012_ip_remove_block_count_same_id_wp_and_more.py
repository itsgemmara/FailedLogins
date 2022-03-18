# Generated by Django 4.0.3 on 2022-03-17 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0011_block_count_same_id_wp'),
    ]

    operations = [
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15)),
                ('count_faild_login', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='block',
            name='count_same_id_wp',
        ),
        migrations.RemoveField(
            model_name='block',
            name='user_IP',
        ),
        migrations.AlterField(
            model_name='wrongpass',
            name='user_IP',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='User.ip'),
        ),
    ]