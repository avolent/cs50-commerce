from cgitb import reset
from optparse import TitledHelpFormatter
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Auction, Watchlist, Bid, Comment

class CreateListing(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    description = forms.CharField(label="Title",)
    category = forms.CharField(label="Category", max_length=64 )
    Price = forms.CharField(label="Price")
    url = forms.CharField(label="Image URL:")

def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions
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

# Route for creating listings
def create(request):
    # Post request to create a listing on the page. Eventually should add Django forms.
    if request.method == "POST":
        print(request.user.id)
        a = Auction(title=request.POST["title"], description=request.POST["description"], starting_price=request.POST["price"], image=request.POST["image"], category=request.POST["category"].lower().capitalize(), seller=request.user)
        a.save()
        return HttpResponseRedirect(reverse("index"))
    # If a get request just render page template
    else:
        return render(request, "auctions/create_listing.html")

# Route for showing listings
def listing(request, listing):
    # Grab the current listing from auction database
    auction = Auction.objects.get(title=listing)
    comments = Comment.objects.filter(auction=auction)
    # Post requests start here
    if request.method == "POST":
        print(request.POST["action"])
        # If request is for close, change auction status to close and update page
        if request.POST["action"] == "close":
            auction.status = "Closed"
            auction.save()
            return HttpResponseRedirect(reverse("listing", args=[listing]))
        # Add auction to users watchlist.
        elif request.POST["action"] == "watchlist":
            watchlist = Watchlist(auction=auction, user=request.user)
            watchlist.save()
            return HttpResponseRedirect(reverse("listing", args=[listing]))  
        elif request.POST["action"] == "bid":
            if float(request.POST["bid"]) >= auction.price:
                bid = Bid(auction=auction, bidder=request.user, bid=request.POST["bid"])
                bid.save()
                auction.price = request.POST["bid"]
                auction.save()
                return HttpResponseRedirect(reverse("listing", args=[listing]))
            else:
                return render(request, "auctions/listing.html", {
            "auction": auction,
            "alert": "Error: Bid price is lower then asking price, try again!",
            })
        elif request.POST["action"] == "comment":
            comment = Comment(auction=auction, user=request.user, comment=request.POST["comment"])
            comment.save()
            return HttpResponseRedirect(reverse("listing", args=[listing]))
        return HttpResponseRedirect(reverse("listing", args=[listing]))
        
    # Else get request start here and render listing page with all auction details.     
    else:
        # if the auction is closed and you are the highest bidder, Alert that you won!
        if auction.status == "Closed":
            try:
                highestBid = Bid.objects.get(auction=auction, bid=auction.price)
                if highestBid.bidder == request.user:
                    return render(request, "auctions/listing.html", {
                    "auction": auction,
                    "comments": comments,
                    "alert": "Auction Closed. You won!"
                    })
            except ObjectDoesNotExist:
                    return render(request, "auctions/listing.html", {
                        "auction": auction,
                        "comments": comments,
                    })
        return render(request, "auctions/listing.html", {
            "comments": comments,
            "auction": auction,
        })

# Route for categories lists
def categories(request):
    auctions = Auction.objects.all()
    categories = []
    for auction in auctions:
        if auction.category.capitalize() not in categories:
            if auction.category == "":
                categories.append('None')
            else:
                categories.append(auction.category.capitalize())
    print(categories)
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

# Route for category listing pages
def category(request, category):
    if category == "None":
        auctions = Auction.objects.filter(category="")
    else:
        auctions = Auction.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "category": category.capitalize(),
        "auctions": auctions
    })