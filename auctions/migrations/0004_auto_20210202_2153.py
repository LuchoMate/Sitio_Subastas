# Generated by Django 3.1.5 on 2021-02-03 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210202_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='member_since',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
