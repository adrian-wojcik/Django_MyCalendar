# Generated by Django 4.1.5 on 2023-01-22 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0006_todolist_todolistitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todolist',
            options={'ordering': ('-id',), 'verbose_name': 'Lista TODO', 'verbose_name_plural': 'Listy TODO'},
        ),
        migrations.AlterField(
            model_name='todolistitem',
            name='status',
            field=models.CharField(choices=[('a', 'Aktualne'), ('b', 'Wykonane')], default='a', max_length=1),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
            },
        ),
    ]