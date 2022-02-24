from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .forms import CreateForm
from django.template.defaultfilters import slugify

from .models import Comment, User,Listing, Category, Watchlist, Bid


def index(request):
    return render(request, "auctions/index.html",{
        "products":Listing.objects.filter(is_active=True),
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

@login_required
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

@login_required
def create(request):
    if request.method=="POST":
        listing_form = CreateForm(request.POST)
        if listing_form.is_valid():

            # Save the values of the fields of the form
            listing_form = listing_form.save(commit=False)
            
            # Save the rest of the field of the forms, seller, slug and current bid price
            
            listing_form.seller = request.user
            listing_form.slug = slugify(listing_form.title)
            listing_form.current_bid = listing_form.starting_bid
            listing_form.save()

            return HttpResponseRedirect(reverse("index"))

        else:
            return render (request,"auctions/create.html",
            {
                "form" : listing_form
            })

    # If its a GET request, render a blank form for user to create a listing
    else:
        form= CreateForm()
        return render(request, "auctions/create.html", {
            "form": form
            })


    
def category_list(request):
    return render(request, "auctions/categories.html",{
        "category" : Category.objects.all(),
    })

def category(request,category_slug):
    category = get_object_or_404(Category, slug= category_slug)
    return render(request, "auctions/category.html",{

        "products" : Listing.objects.filter(category = category),
        "category" : category
    })

@login_required
def watchlist(request):
      items_in_watchlist = Watchlist.objects.filter(user=request.user).values_list('item',flat=True)
      products = Listing.objects.filter(pk__in=items_in_watchlist)
      return render(request, "auctions/watchlist.html",
      {
          "products" : products
      })
    





def product(request, product_slug):

    product = get_object_or_404(Listing,slug=product_slug)

    # Check if the user is the buyer or seller
    if product.seller == request.user:
        if request.method == "GET":

            # Check if there are bids for the product
            if product.current_bid == product.starting_bid:
                no_bids = True
            else:
                no_bids = False


            return render(request,"auctions/sellerproduct.html",
            {
                "product" : product,
                "comments": Comment.objects.filter(listing = product.id),
                "no_bids" : no_bids
            })
        # If seller clicks on the close auction button
        else:
            # Close the listing(change is_active status to False )
            product = get_object_or_404(Listing,slug=product_slug, is_active=True)
            product.is_active = False
            product.save()

            return HttpResponseRedirect(reverse("index"))

            




    # If user is a buyer
    else:
        # If user clicks on the add to watchlist button
        if request.method =="POST":
            # Check if item is in user watchlist
            product = get_object_or_404(Listing,slug=product_slug)
            items_in_watchlist = Watchlist.objects.filter(user=request.user).values_list('item',flat=True)
    
            # If item is not in user's watchlist->add the item to the user watchlist
            if product.id not in items_in_watchlist:
                Watchlist.objects.create(user=request.user,item= Listing.objects.get(id=product.id))
            
            # If item is in user's watchlist->remove the item from the user watchlist
            else:
                record = Watchlist.objects.filter(user=request.user, item=Listing.objects.get(id=product.id))
                record.delete()

            return HttpResponseRedirect(reverse("product", args=(product.slug,)))

        
       
        else:
            product = get_object_or_404(Listing,slug=product_slug)
            items_in_watchlist = Watchlist.objects.filter(user=request.user).values_list('item',flat=True)

            if product.id in items_in_watchlist:
                watchlist_message = "Remove from my watchlist"
            else:
                watchlist_message = "Add to my watchlist"

            winner_of_bid = product.highest_bidder
            # Check if user is the winner of the bid
            if request.user.username == winner_of_bid and product.is_active==False:
                winner = True
            else:
                winner = False
            return render(request, "auctions/buyerproduct.html",{
                "product": product,
                "watchlist_message": watchlist_message,
                "comments": Comment.objects.filter(listing = product.id),
                "winner" : winner
                })

@login_required
def bid(request, product_slug):
    product = get_object_or_404(Listing, slug=product_slug, is_active=True)
    if request.method=="GET":  
        return render(request, "auctions/bid.html",
        {
            "product" : product
        })

    else:

        # Create a record in the bid database 
        bid_amount = request.POST.get("bid")
        Bid.objects.create(user=request.user, listing=Listing.objects.get(id=product.id),bid_amount=bid_amount)
        
        # Update the current_bid field of the product, and the highest bidder will be the current bidder
        record = Listing.objects.get(id=product.id)
        record.current_bid = bid_amount
        record.highest_bidder = request.user.username
        record.save()

        return HttpResponseRedirect(reverse("product", args=(product.slug,)))
        
       
@login_required
def comment(request,product_slug):

    if request.method=="POST":
        product = get_object_or_404(Listing,slug=product_slug)
        
        # Add the comment to the comment databas
        user_comment =request.POST.get("comment")
        Comment.objects.create(user=request.user,listing= Listing.objects.get(id=product.id),comment=user_comment)
        return HttpResponseRedirect(reverse("product", args=(product.slug,)))
        
    else:
        product = get_object_or_404(Listing,slug=product_slug)
        return render(request,"auctions/comment.html",{
        "product" : product
        })








    
    

