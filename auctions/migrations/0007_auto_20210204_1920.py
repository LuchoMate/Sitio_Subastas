# Generated by Django 3.1.5 on 2021-02-04 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210203_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='bid_author',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='comments',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
