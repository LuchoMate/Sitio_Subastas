#CS50 Commerce Project 2021- Author: Luis Balladares
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from .models import User, auction_listing, bids, comments
from . import forms
from django.template.defaulttags import register
from django.contrib import messages




@register.filter
def get_bid(dictionary, key):
    return dictionary.get(key)# django's template wont let parse forloop.counter as an index on a list, so
                                # a dictionary must be registered to associate listings with its current bid

def index(request):
    active_listings = auction_listing.objects.filter(active_status = True).all()
    #relate each listing with its current bid
    id_and_bid = {}
    for listing in active_listings:
        current_bid = bids.objects.get(pk =listing.id)
        id_and_bid[int(listing.id)] = current_bid.highest_bid

    return render(request, "auctions/index.html",{
        "active_listings": active_listings,
        "id_and_bid": id_and_bid
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='auctions/login.html')
def new_listing(request):
    if request.method =='POST':
        form = forms.listingform(request.POST)
        if form.is_valid():
            listing = form.save(commit = False)
            listing.author = request.user
            if not listing.img_url:
                listing.img_url = "../static/auctions/images/generic.png"

            listing.save()            
            current_bid = bids(id=listing, highest_bid= listing.starting_bid ,highest_bid_user=str(listing.author))#in this case the original author
            current_bid.save()
            
            messages.success(request, "Your listing was successfully created !")
            active_listings = auction_listing.objects.filter(active_status = True).all()
            #relate each listing with its current bid
            id_and_bid = {}
            for listing in active_listings:
                current_bid = bids.objects.get(pk =listing.id)
                id_and_bid[int(listing.id)] = current_bid.highest_bid

            return render(request, "auctions/index.html",{
                "active_listings": active_listings,
                "id_and_bid": id_and_bid
                })
        else:
            return render(request, "auctions/new_listing.html", {
            "listingform": forms.listingform() })


    else:
        return render(request, "auctions/new_listing.html", {
        "listingform": forms.listingform()
        })

def listing(request, listing_id):
    listing = auction_listing.objects.get(pk = listing_id)
    current_bid = bids.objects.get(pk = listing.id)
    category = listing.get_category_display()
    comments_list = comments.objects.filter(listing_id = listing_id)

    if listing.watchlist.filter(username=request.user):
        usertocheck = True
    else:
        usertocheck = False    
    
    return render(request, "auctions/listing.html",{
        "listing": listing,
        "current_bid": current_bid,
        "bidform": forms.bidform(),
        "usertocheck": usertocheck,
        "category": category,
        "comment": forms.commentform(),
        "comments_list": comments_list
    })


@login_required(login_url='auctions/login.html')
def new_bid(request, listing_id):
    if request.method == 'POST':
        form = forms.bidform(request.POST)
        if form.is_valid():            
            listing = auction_listing.objects.get(pk=listing_id)
            current_bid = bids.objects.get(pk=listing_id)
            category = listing.get_category_display()
            comments_list = comments.objects.filter(listing_id = listing_id)

            if listing.watchlist.filter(username=request.user):
                usertocheck = True
            else:
                usertocheck = False

            bid_to_place = form.save(commit = False)

            if bid_to_place.highest_bid > current_bid.highest_bid:#user placing a higher bid = allow it
                bid_to_place.highest_bid_user = str(request.user)
                bid_to_place.id = listing
                bid_to_place.save()
                #bid_to_place.save(update_fields=['highest_bid', 'highest_bid_user'])
                messages.success(request, "Your bid was successfully placed !")

                return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": bid_to_place,
                    "usertocheck": usertocheck,
                    "bidform": forms.bidform(),
                    "category": category,
                    "comment": forms.commentform(),
                    "comments_list": comments_list

                })
            elif bid_to_place.highest_bid == current_bid.highest_bid:
                if listing.author == current_bid.highest_bid_user:#if its gonna be an EQUAL FIRST bid = allow it
                    bid_to_place.highest_bid_user = str(request.user)
                    bid_to_place.id = listing
                    bid_to_place.save()
                    messages.success(request, "Your bid was successfully placed !")
                    return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": bid_to_place,
                    "bidform": forms.bidform(),
                    "usertocheck": usertocheck,
                    "category": category,
                    "comment": forms.commentform(),
                    "comments_list": comments_list
                    })
                else:#no longer first bid = deny it
                    messages.error(request, "Your bid must be higher than the current price!")
                    return render(request, "auctions/listing.html",{
                        "listing": listing,
                        "current_bid": bid_to_place,
                        "bidform": forms.bidform(),
                        "usertocheck": usertocheck,
                        "category": category,
                        "comment": forms.commentform(),
                        "comments_list": comments_list                   
                        })
            else: #user placing a lower bid = deny it
                messages.error(request, "Your bid must be higher than the current price!")
                return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "usertocheck": usertocheck,
                    "category": category,
                    "comment": forms.commentform(),
                    "comments_list": comments_list 
                    })                
        else:#return to index
            active_listings = auction_listing.objects.filter(active_status = True).all()
            #relate each listing with its current bid
            id_and_bid = {}
            for listing in active_listings:
                current_bid = bids.objects.get(pk =listing.id)
                id_and_bid[int(listing.id)] = current_bid.highest_bid

            return render(request, "auctions/index.html",{
                "active_listings": active_listings,
                "id_and_bid": id_and_bid
            })
    else:#return to index
        active_listings = auction_listing.objects.filter(active_status = True).all()
        #relate each listing with its current bid
        id_and_bid = {}
        for listing in active_listings:
            current_bid = bids.objects.get(pk =listing.id)
            id_and_bid[int(listing.id)] = current_bid.highest_bid

        return render(request, "auctions/index.html",{
            "active_listings": active_listings,
            "id_and_bid": id_and_bid
        })

@login_required(login_url='auctions/login.html')
def close_bid(request, listing_id):
    if request.method =='POST':
        listing = auction_listing.objects.get(pk=listing_id)
        listing.active_status = False
        listing.save()
        current_bid = bids.objects.get(pk=listing_id)
        category = listing.get_category_display()
        comments_list = comments.objects.filter(listing_id = listing_id)

        if listing.author == current_bid.highest_bid_user:#no winners
            messages.error(request, "You closed this auction with no bidders. Better luck next time !") 
            return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "category": category,
                    "comments_list": comments_list,
                    "comment": forms.commentform(),


                    }) 
        else:
            messages.success(request, f"You closed this auction !-- Get in touch with the winner, user: {current_bid.highest_bid_user} ")        

            return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "category": category,
                    "comments_list": comments_list,
                    "comment": forms.commentform()
                    }) 
    else:
        listing = auction_listing.objects.get(pk=listing_id)
        current_bid = bids.objects.get(pk=listing_id)
        category = listing.get_category_display()
        comments_list = comments.objects.filter(listing_id = listing_id)
        return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "comments_list": comments_list,
                    "comment": forms.commentform(),
                    "category": category

                    })


@login_required(login_url='auctions/login.html')
def add_watchlist(request, listing_id):
    current_bid = bids.objects.get(pk=listing_id)
    listing = auction_listing.objects.get(pk=listing_id)
    category = listing.get_category_display()
    comments_list = comments.objects.filter(listing_id = listing_id)

    usertowatchlist = User.objects.get(username=request.user)
    listing.watchlist.add(usertowatchlist)

    try:
        listing.save()
    except IntegrityError:
        messages.error(request, "There was an error trying to process your request, please try again.")
        usertocheck = False
        
        return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "usertocheck": usertocheck,
                    "comments_list": comments_list,
                    "comment": forms.commentform(),
                    "category": category

                    })

    messages.success(request, "Listing successfully added to your watchlist !")
    usertocheck = True

    return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "usertocheck": usertocheck,
                    "comments_list": comments_list,
                    "comment": forms.commentform(),
                    "category": category
                    })


@login_required(login_url='auctions/login.html')
def remove_watchlist(request, listing_id):
    current_bid = bids.objects.get(pk=listing_id)
    listing = auction_listing.objects.get(pk=listing_id)
    category = listing.get_category_display()
    comments_list = comments.objects.filter(listing_id = listing_id)

    usertoremove = User.objects.get(username=request.user)
    listing.watchlist.remove(usertoremove)

    try:
        listing.save()
    except IntegrityError:
        messages.error(request, "There was an error trying to process your request, please try again.")
        usertocheck = True
        
        return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "usertocheck": usertocheck,
                    "comments_list": comments_list,
                    "comment": forms.commentform(),
                    "category": category

                    })

    messages.success(request, "Listing successfully removed from your watchlist !")
    usertocheck = False

    return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "usertocheck": usertocheck,
                    "comments_list": comments_list,
                    "comment": forms.commentform(),
                    "category": category
                    })

@login_required(login_url='auctions/login.html')
def my_watchlist(request):
    myuser = User.objects.get(username=request.user)
    userwatchlist = myuser.user_watchlist.all()
    id_and_bid = {}

    for listing in userwatchlist:
        current_bid = bids.objects.get(pk=listing)
        id_and_bid[int(listing.id)] = current_bid.highest_bid
        

    return render(request, "auctions/watchlist.html", {
        "userwatchlist": userwatchlist,
        "id_and_bid": id_and_bid
        })

@login_required(login_url='auctions/login.html')
def new_comment(request, listing_id):
    if request.method =='POST':
        listing = auction_listing.objects.get(pk=listing_id)
        current_bid = bids.objects.get(pk=listing_id)
        form = forms.commentform(request.POST)
        category = listing.get_category_display()
        if form.is_valid():
            newcomment = form.save(commit = False)
            newcomment.listing_id= listing
            newcomment.post_author = str(request.user)

            if listing.watchlist.filter(username=request.user):
                usertocheck = True
            else:
                usertocheck = False
              
            try:
                newcomment.save()
            except IntegrityError:
                messages.error(request, "There was an error trying to process your request, please try again.")
                comments_list = comments.objects.filter(listing_id = listing_id)
                return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "usertocheck": usertocheck,
                    "comments_list": comments_list,
                    "comment": forms.commentform(),
                    "category": category

                    })
            messages.success(request, "Comment successfully posted !")
            comments_list = comments.objects.filter(listing_id = listing_id)
            return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "comments_list": comments_list,
                    "usertocheck": usertocheck,
                    "comment": forms.commentform(),
                    "category": category
                    })       
            
        else:
            comments_list = comments.objects.filter(listing_id = listing_id)
            if listing.watchlist.filter(username=request.user):
                usertocheck = True
            else:
                usertocheck = False
                return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "comments_list": comments_list,
                    "usertocheck": usertocheck,
                    "comment": forms.commentform(),
                    "category": category
                    })

    else:
        category = listing.get_category_display()
        comments_list = comments.objects.filter(listing_id = listing_id)

        if listing.watchlist.filter(username=request.user):
                usertocheck = True
        else:
                usertocheck = False

        return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "usertocheck": usertocheck,
                    "category": category,
                    "comments_list": comments_list,
                    "comment": forms.commentform()
                    })

def all_categories(request):
    return render (request, "auctions/all_categories.html" )

def category_branch(request, category_id):
    categorylist = auction_listing.objects.filter(active_status=True, category=category_id)
    if categorylist:
        aux = categorylist.first()
        categorytitle = aux.get_category_display()

        id_and_bid = {}
        for listing in categorylist:
            current_bid = bids.objects.get(pk =listing.id)
            id_and_bid[int(listing.id)] = current_bid.highest_bid

        return render(request, "auctions/category_branch.html", {
            "categorylist": categorylist,
            "id_and_bid": id_and_bid,
            "categorytitle": categorytitle
        })

    else:
        return render(request, "auctions/category_branch.html", {
            "categorylist": False
        })



        





    







            



        
