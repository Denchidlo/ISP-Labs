# Generated by Django 3.2.2 on 2021-05-21 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='auditory',
            field=models.CharField(blank=True, default='unknown', max_length=30, null=True),
        ),
    ]
