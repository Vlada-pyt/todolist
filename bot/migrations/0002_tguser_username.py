# Generated by Django 4.0.1 on 2023-03-19 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='username',
            field=models.CharField(blank=True, default=None, max_length=300, null=True),
        ),
    ]
