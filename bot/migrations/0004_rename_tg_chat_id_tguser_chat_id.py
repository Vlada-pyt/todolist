# Generated by Django 4.0.1 on 2023-03-21 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_alter_tguser_options_rename_chat_id_tguser_tg_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tguser',
            old_name='tg_chat_id',
            new_name='chat_id',
        ),
    ]
