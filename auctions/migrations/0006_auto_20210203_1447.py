# Generated by Django 3.1.5 on 2021-02-03 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210202_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listing',
            name='category',
            field=models.CharField(choices=[('FA', 'Fashion'), ('BM', 'Books, Moves & Music'), ('EL', 'Electronics'), ('CO', 'Collectibles & Art'), ('HG', 'Home & Garden'), ('SG', 'Sporting Goods'), ('TH', 'Toys & Hobbies'), ('BI', 'Business & Industrial'), ('HB', 'Health & Beauty'), ('OT', 'Others')], default='OT', max_length=2),
        ),
        migrations.AddField(
            model_name='auction_listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=17),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='description',
            field=models.TextField(),
        ),
    ]