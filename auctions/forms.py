from tkinter import HIDDEN
from django import forms
from .models import *

class AddListing(forms.Form):

    title = forms.CharField(max_length=100)
    description = forms.Textarea()
    initial_bid = forms.FloatField()
    url = forms.URLField(null=True)
    category = forms.CharField(max_length=200, null=True)



class AddComments(forms.Form):

    user = User(HIDDEN=True)
    listing = Listings(HIDDEN=True)
    comment = forms.Textarea()