# Generated by Django 4.0.1 on 2023-03-21 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_alter_tguser_tg_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='tg_id',
            field=models.BigIntegerField(unique=True),
        ),
    ]
