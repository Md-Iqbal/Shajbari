# Generated by Django 3.1.7 on 2021-03-29 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0006_auto_20210330_0032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='zipcode',
        ),
    ]
