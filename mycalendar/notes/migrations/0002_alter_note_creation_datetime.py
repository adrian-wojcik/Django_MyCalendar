# Generated by Django 4.1.5 on 2023-01-14 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='creation_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
