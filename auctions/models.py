from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms.widgets import NullBooleanSelect
from django.urls import reverse

class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length= 255, db_index=True)
    slug = models.SlugField(max_length= 255, unique=True)

    class Meta:
        verbose_name_plural="categories"

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length= 255, unique=True)
    slug = models.SlugField(max_length = 255)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    seller= models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_creator")
    description = models.TextField()
    image = models.URLField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2) 
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True) 
    highest_bidder = models.CharField(max_length=255, default="")
    is_active = models.BooleanField(default= True) 
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product",args=[self.slug])
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} bid {self.bid_amount} on {self.create_date}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name= "listing_comments")
    comment = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.create_date}"