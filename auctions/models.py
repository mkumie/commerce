from cProfile import label
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Listings(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    initial_bid = models.FloatField()
    url = models.URLField(blank=True)
    category = models.CharField(max_length=200, blank=True)

    
    def __str__(self):
        
        return self.title



class Bids(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bid = models.FloatField()



class Comments(models.Model):

    user = models.ManyToManyField(User)
    listing = models.ManyToManyField(Listings)
    comment = models.TextField()


    def __str__(self):

        return self.comment