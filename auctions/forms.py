from django import forms
from django.forms import ModelForm
from auctions.models import Category, Listing


class CreateForm(ModelForm):
    class Meta:
        category=forms.ModelChoiceField(queryset=Category.objects.all())
        
        model = Listing
        fields = ("title", "category", "description","starting_bid", "image")
        labels = {
        "title": "Title",
        "category": "Category",
        "description": "Description",
        "starting_bid": "Starting Bid",
        "image": "URL for image"}
        widgets ={
        "title": forms.TextInput(attrs={"class": "form-control"}),
        "description": forms.Textarea(attrs={"class": "form-control"}),
        "starting_bid": forms.NumberInput(attrs={"class": "form-control"}),
        "image": forms.URLInput(attrs={"class": "form-control"}),
        }
        category.widget.attrs.update({"class": "form-control"})
      
        

        
