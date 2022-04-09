from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import numbers

from .models import User
from .forms import *


def index(request):

    listings = Listing.objects.all()

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


def add_listing(request):

    data = Listing()
    
    if request.method == 'POST':

        form = AddListing(request.POST, request.FILES, instance=data)

        if form.is_valid:

            form.save()

            return HttpResponseRedirect(reverse("index"))

    form = AddListing()

    return render(request, "auctions/add_listing.html", {
        'form': form,
    })


def display_listing(request, list_id):

    if request.method == 'GET':
        
        listing = Listing.objects.get(pk=list_id)

        form = ViewListing(instance=listing)
        img = form.instance

        return render(request, 'auctions/display_listing.html', {
            'form': form,
            'listing': listing,
            'img': img,
        })


def categories(request):

    categories = []
    
    listings = Listing.objects.exclude(category__isnull=True).exclude(category="")

    for listing in listings:
        categories.append(listing.category)

    categories = set(categories)

    return render(request, 'auctions/categories.html', {
        'categories': categories,
    })


def display_category(request, category):
    
    listings = Listing.objects.filter(category=category)

    return render(request, 'auctions/display_category.html', {
        'listings': listings,
        'category': category,
    })


def watchlist_add(request, listing_id):

    listing_to_save = get_object_or_404(Listing, pk=listing_id)

    if Watchlist.objects.filter(user=request.user, listings=listing_to_save).exists():
        messages.add_message(request, messages.ERROR, 'You already have %s in your watchlist.' % listing_to_save)
        return HttpResponseRedirect(reverse("index"))

    watch_list, created = Watchlist.objects.get_or_create(user=request.user)

    watch_list.listings.add(listing_to_save)
    messages.success(request, 'Successfully added %s to your watchlist.' % listing_to_save)

    return watchlist(request, request.user)


def watchlist(request, user):

    watchlist, created = Watchlist.objects.get_or_create(user=request.user)

    return render(request, "auctions/watchlist.html", {
        'watchlist': watchlist.listings.all(),
    })


def delete_watchlist(request, listing_id):

    listing_to_delete = Listing.objects.get(pk=listing_id)
    watch_list = Watchlist.objects.get(user=request.user)

    watch_list.listings.remove(listing_to_delete)            

    return watchlist(request, request.user)


def bid(request, listing_id):
    
    listing = Listing.objects.get(pk=listing_id)
    bid = 0.0
    user = request.user

    # If not a number/float prompt for appropriate input
    try:
        bid = float(request.POST['bid'])
    except ValueError:
        messages.add_message(request, messages.ERROR, 'Bid value should be a number. "%s" is not a number.' % request.POST['bid'])
        return HttpResponseRedirect(reverse('display_listing', args=(listing_id,)))

    check = False
    bid_value = 0.0
    highest_bid = listing.initial_bid
    biddings = Bid.objects.filter(listing=listing)

    # Check if such bid exists for the listing and update or create otherwise
    for bidding in biddings:
        
        if bidding.user == user and bidding.listing == listing:
            bid_value = bidding.bid
            check = True

        if bidding.listing == listing and bidding.bid > highest_bid:
            highest_bid = bidding.bid

    # If such bid exists...  
    if check:
        
        place_bid = Bid.objects.get(user=user, listing=listing, bid=bid_value)

        if bid > highest_bid:    
            place_bid.bid = bid
            place_bid.save()

        else:
            messages.add_message(request, messages.ERROR, 'Bid value should be greater than %s.' % highest_bid)
    
    # Otherwise...
    else:
        if bid == listing.initial_bid and (biddings.count() == 0):
            place_bid = Bid.objects.create(user=user, listing=listing, bid=bid)

        elif bid > highest_bid:
            place_bid = Bid.objects.create(user=user, listing=listing, bid=bid)

        else:
            messages.add_message(request, messages.ERROR, 'Bid value should be greater than %s.' % highest_bid)
        
    if biddings.filter().count() == 1:
            messages.add_message(request, messages.INFO, 'There is 1 bid to this listing.')

    else:
            messages.add_message(request, messages.INFO, 'There are %s bids to this listing.' % biddings.filter(listing=listing).count())
     
    return HttpResponseRedirect(reverse('display_listing', args=(listing_id,)))