# Generated by Django 4.0.1 on 2023-03-21 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_remove_tguser_tg_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='username',
            field=models.CharField(blank=True, default=None, max_length=350),
        ),
    ]
