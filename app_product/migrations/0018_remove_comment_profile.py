# Generated by Django 3.1.7 on 2021-04-09 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0017_comment_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='profile',
        ),
    ]
