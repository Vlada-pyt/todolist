# Generated by Django 4.0.1 on 2023-03-22 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0010_alter_tguser_chat_id_alter_tguser_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='chat_id',
            field=models.BigIntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='tguser',
            name='verification_code',
            field=models.CharField(default=None, max_length=35),
        ),
    ]
