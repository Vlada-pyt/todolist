# Generated by Django 4.0.1 on 2023-03-21 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_rename_tg_chat_id_tguser_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='tg_id',
            field=models.BigIntegerField(default=None, unique=True),
        ),
    ]
