# Generated by Django 2.0.3 on 2019-12-01 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20191201_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizza',
            name='vegetarian',
        ),
    ]
