#CS50 Commerce Project 2021- Author: Luis Balladares
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class User(AbstractUser):
    member_since = models.DateField(auto_now_add=timezone.now())


#An article to be auctioned
class auction_listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    creation_date = models.DateTimeField(auto_now_add=timezone.now())   
    author = models.CharField(max_length=150)#150 is max length of abstract user
    img_url = models.CharField(max_length=256, blank=True, null=True, help_text="Optional")
    watchlist = models.ManyToManyField(User, blank=True, related_name="user_watchlist")
    active_status = models.BooleanField(default=True)

    categories_list = (
        ('FA', 'Fashion'),
        ('BM', 'Books, Moves & Music'),
        ('EL', 'Electronics'),
        ('CO', 'Collectibles & Art'),
        ('HG', 'Home & Garden'),
        ('SG', 'Sporting Goods'),
        ('TH', 'Toys & Hobbies'),
        ('BI', 'Business & Industrial'),
        ('HB', 'Health & Beauty'),
        ('OT', 'Others')
    )
   
    category = models.CharField(max_length=2, choices=categories_list, default='OT', help_text="If not specified it will be set as Others")    

    class meta:
        ordering = ('-creation_date')

    def __str__(self):
        return f"{ self.id} {self.title} -- {self.creation_date}"

#Current bid on a given article
class bids(models.Model):
    id = models.OneToOneField(auction_listing,
        on_delete=models.CASCADE, primary_key=True, related_name="listing_bid")
    
    highest_bid = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    highest_bid_user = models.CharField(max_length=150, blank=True, null=True)
    last_bid_date = models.DateTimeField(auto_now=timezone.now())

    class meta:
        ordering = ('last_bid_date')


    def __str__(self):
        return f"-- Bid $ {self.highest_bid} by {self.highest_bid_user} on -- {self.last_bid_date}"


#Articles comments
class comments(models.Model):
    listing_id = models.ForeignKey(auction_listing, on_delete=models.CASCADE, related_name="listing_comments")
    post_author = models.CharField(max_length=150)
    commentary_date = models.DateTimeField(auto_now_add=timezone.now()) 
    comment = models.TextField(null=True)

    def __str__(self):
        return f"Listing id: {self.listing_id} by {self.post_author} on {self.commentary_date}"


