# Generated by Django 4.0.1 on 2023-03-21 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_alter_tguser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='username',
            field=models.CharField(blank=True, default=None, max_length=350, null=True),
        ),
    ]
