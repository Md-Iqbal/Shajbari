# Generated by Django 3.1.7 on 2021-04-03 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0006_auto_20210402_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='users_img/default/default.jpg', null=True, upload_to='users_img/'),
        ),
    ]
