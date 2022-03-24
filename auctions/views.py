from typing import List
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .forms import *


def index(request):

    listings = Listings.objects.all()

    return render(request, "auctions/index.html", {
        'listings': listings,
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


def add_listings(request):

    data = Listings()
    
    if request.method == 'POST':

        form = AddListing(request.POST, instance=data)

        if form.is_valid:

            form.save()

            return HttpResponseRedirect(reverse("index"))

    form = AddListing()

    return render(request, "auctions/add_listing.html", {
        'form': form,
    })


def display_listing(request, list_id):

    if request.method == 'GET':
        
        listing = Listings.objects.get(pk=list_id)

        form = ViewListing(instance=listing)

        return render(request, 'auctions/display_listing.html', {
            'form': form,
            'listing': listing,
        })


def categories(request):

    categories = []
    
    listings = Listings.objects.exclude(category__isnull=True).exclude(category="")

    for listing in listings:
        categories.append(listing.category)

    categories = set(categories)

    return render(request, 'auctions/categories.html', {
        'categories': categories,
    })


def display_category(request, category):
    
    listings = Listings.objects.filter(category=category)

    return render(request, 'auctions/display_category.html', {
        'listings': listings,
        'category': category,
    })