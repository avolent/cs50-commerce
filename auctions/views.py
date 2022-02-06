from optparse import TitledHelpFormatter
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Auction

class CreateListing(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    description = forms.CharField(label="Title",)
    category = forms.CharField(label="Tategory", max_length=64 )
    title = forms.CharField(label="Title")
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

def create(request):
    if request.method == "POST":
        print(request.user.id)
        a = Auction(title=request.POST["title"], description=request.POST["description"], starting_price=request.POST["price"], image=request.POST["image"], category=request.POST["category"].lower().capitalize(), seller=request.user)
        a.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html")

def listing(request, listing):
    auction = Auction.objects.get(title=listing)
    return render(request, "auctions/listing.html", {
        "auction": auction,
    })

# Route for categories lists
def categories(request):
    auctions = Auction.objects.all()
    categories = []
    for auction in auctions:
        if auction.category.capitalize() not in categories:
            if auction.category is "":
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