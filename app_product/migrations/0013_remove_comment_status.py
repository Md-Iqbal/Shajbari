# Generated by Django 3.1.6 on 2021-03-25 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0012_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='status',
        ),
    ]