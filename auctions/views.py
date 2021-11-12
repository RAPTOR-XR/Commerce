from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.fields import NOT_PROVIDED
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionList, AuctionBid, AuctionComment, AuctionWatchList


def index(request):
    return render(request, "auctions/index.html", {"lists":AuctionList.objects.all().filter(active_status=True), "bid":AuctionBid.objects.all()})


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

def create_auctions(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login_view"), {"message": "Please login to create an auction."})
        user = request.user
        title = request.POST['title']
        description = request.POST['description']
        image_url = request.POST['image_url']
        category = request.POST['category']
        starting_bid = request.POST['starting_bid']
        created = AuctionList.objects.create(user=user,title=title,description=description,image_url=image_url,category=category,starting_bid=starting_bid)
        created.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html")

def list_auction(request, id):
    lists = AuctionList.objects.filter(id = id).first()
    bid = AuctionBid.objects.filter(lists = lists)
    comment = AuctionComment.objects.filter(lists = lists)
    highest_bid = lists.starting_bid
    if bid is not None:
        for bids in bid:
            if bids.input_value > highest_bid:
                highest_bid = bids.input_value
    if request.method == 'POST':
        user = request.user
        lists = AuctionList.objects.filter(id = id).first()
        comment = request.POST.get('comment', None)
        input_value = request.POST.get('Auction_price', None)
        try:
            input_value = float(input_value)
        except:
            input_value = None
        if comment is not None:
            comm = AuctionComment.objects.create(comment = comment, user = user, lists = lists)
            comm.save()
            return HttpResponseRedirect(reverse('lists', args = [id]))
        if input_value is not None:
            if float(input_value) < highest_bid:
                return HttpResponseRedirect(reverse('lists', args = [id]))
            bid = AuctionBid.objects.create(input_value = float(input_value), user = user, lists =lists)
            bid.save()
            prev_bid = AuctionBid.objects.filter(lists = lists).exclude(input_value = input_value)
            prev_bid.delete()
            return HttpResponseRedirect(reverse('lists', args = [id]))
        if comment is None and input_value is None:
            return render(request, "auctions/error.html", {"message": "Please bid the product or add a comment."})
    return render(request, "auctions/lists.html", {"lists": lists, "highest_bid":highest_bid, "min_bid":(highest_bid + 0.50),"comment":comment})
        
def catagory(request):
    lists = []
    listss = AuctionList.objects.all()
    for i in listss:
        if i.category:
            if i.category not in lists:
                lists.append(i.category)
    return render(request, "auctions/categories.html", {"category":lists})

def cat_lists(request, category):
    lists = AuctionList.objects.all().filter(category = category)
    return render (request, "auctions/category_listing.html",{"lists":lists})

def toggle(request, id):
    user = request.user
    lists = AuctionList.objects.filter(id = id).first()
    watch = AuctionWatchList.objects.filter(user = user, lists = lists).first()
    if watch is None:
        watchfor = AuctionWatchList.objects.create(user = user, lists = lists)
        watchfor.save()
        return HttpResponseRedirect(reverse("watchlist"))
    watch.delete()
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def watchlist(request):
    user = request.user
    watchfor = AuctionWatchList.objects.filter(user = user)
    return render(request, "auctions/watchlist.html",{"watchlist":watchfor})

def winned_auctions(request):
    return render(request, "auctions/index.html", {"lists":AuctionList.objects.all().filter(active_status=False),"bid":AuctionBid.objects.all()})

@login_required
def final(request, id):

    lists = AuctionList.objects.filter(id = id).first()
    bid = AuctionBid.objects.filter(lists = lists).first()
    if lists.user == request.user and not bid is None:
        lists.active_status = False
        lists.auction_winner = bid.user
        lists.save()
        return HttpResponseRedirect(reverse("index"))
    elif lists.User == request.user and bid is None:
        lists.active_status = False
        lists.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/error.html",{"message":"You are not authorised to close the bid."})
