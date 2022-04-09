from dataclasses import fields
from tkinter import HIDDEN
from django import forms
from .models import *

class AddListing(forms.ModelForm): # (forms.Form):

    def __init__(self, *args, **kwargs):

        super(AddListing, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Listing
        fields = '__all__' # ['title', 'description', 'initial_bid', 'url', 'category']
        labels = {'title': 'Title', 'description': 'Description', 'initial_bid': 'Initial Bid', 'url': 'Website', 'category': 'Category'}



class AddComment(forms.Form):

    user = User()
    listing = Listing()
    comment = forms.Textarea()
    # comments = forms.CharField(widget=forms.Textarea, label="", max_length=1000)



class ViewListing(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(ViewListing, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs['readonly'] = True

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Listing
        fields = '__all__'
        labels = {'initial_bid': 'Initial Bid',}
        exclude = ('title',)