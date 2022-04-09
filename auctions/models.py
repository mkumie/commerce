from cProfile import label
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Listing(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    initial_bid = models.FloatField()
    image = models.ImageField(upload_to='listing_images/', blank=True)
    category = models.CharField(max_length=200, blank=True)

    
    def __str__(self):
        
        return self.title



class Bid(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.FloatField()


    def __str__(self):

        return f"{self.user}'s {self.listing} Bid"



class Comment(models.Model):

    user = models.ManyToManyField(User)
    listing = models.ManyToManyField(Listing)
    comment = models.TextField()


    def __str__(self):

        return self.comment



class Watchlist(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing)


    def __str__(self):
        return f"{self.user}'s Watchlist"