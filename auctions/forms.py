#CS50 Commerce Project 2021- Author: Luis Balladares
from django.forms import ModelForm
from .models import auction_listing, bids, comments

class listingform(ModelForm):
    class Meta:
        model = auction_listing
        fields = ['title', 'description', 'starting_bid', 'img_url', 'category']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'starting_bid': 'Your starting bid',
            'img_url': 'Copy here an image url to show your article',
            'category': 'Category'
        }


        
class bidform(ModelForm):
    class Meta:
        model = bids
        fields = ['highest_bid']
        labels = {'highest_bid': ''}

class commentform(ModelForm):
    class Meta:
        model = comments
        fields = ['comment']
        labels = {'comment': ''}
