# Generated by Django 3.2.2 on 2021-05-27 23:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_alter_lesson_auditory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouplead',
            name='group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='bot.studentgroup'),
        ),
        migrations.AlterField(
            model_name='grouplead',
            name='user',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
