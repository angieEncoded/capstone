from django import forms
from django.forms import Form, ModelForm, TextInput, Textarea, Select
from .models import Customer, Contact


class newCustomerForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}))
    primary_phone = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2",'placeholder': ""}))
    fax = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}))
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control mb-2",'placeholder': ""}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3,'class': "form-control mb-2",'placeholder': ""}))
    secondary_phone = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}))
    billing_address_one = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2",'placeholder': ""}))
    billing_address_two = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}))
    billing_address_city = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}))
    billing_address_state = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}))
    billing_address_zip = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}))
    billing_address_country = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}))
    shipping_address_one = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2",  'placeholder': ""}))
    shipping_address_two = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2",  'placeholder': ""}))
    shipping_address_city = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2",  'placeholder': ""}))
    shipping_address_state = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2",  'placeholder': ""}))
    shipping_address_zip = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2",'placeholder': ""}))
    shipping_address_country = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2",  'placeholder': ""}))


# class NewContactForm(forms.Form):
#     first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}))
#     last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}))
#     job_title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2",'placeholder': ""}))
#     extension = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}))
#     notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3,'class': "form-control mb-2",'placeholder': ""}))
#     assigned_to = 

class NewContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'job_title', 'extension', 'notes', 'assigned_to')
        widgets = {
            'first_name': TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}),
            'last_name': TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}),
            'job_title': TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}),
            'extension': TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}),
            'extension': TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}),
            'notes': Textarea(attrs={'rows': 3,'class': "form-control mb-2", 'placeholder': ""}),
            'assigned_to': Select(attrs={'class': "form-select mb-2", 'placeholder': ""})
        }


# class NewListingForm(forms.Form):
#     title = forms.CharField(label="Listing Title", max_length=100,
#                             widget=forms.TextInput(attrs={'class': "form-control mb-2", 'required': True, 'placeholder': "Enter a title for your listing here"}))
#     description = forms.CharField(label="Description", max_length=100,
#                                   widget=forms.Textarea(attrs={'class': "form-control mb-2", 'required': True}))
#     url = forms.CharField(label="Image URL", max_length=100, required=False,
#                           widget=forms.TextInput(attrs={'class': "form-control mb-2", "placeholder": "Enter a url to an image"}))
#     starting_bid = forms.CharField(label="Starting Bid in US Dollars",
#                                    widget=forms.TextInput(attrs={'class': "form-control mb-2",  'placeholder': "Enter the starting bid here in US Dollars (i.e. 10.50)"}))
#     categories = forms.ModelChoiceField(
#         queryset=Category.objects.all(), empty_label="Select one...", widget=forms.Select(attrs={'class': 'form-select mb-2', 'required': True}))


# class bidForm(forms.Form):
#     bid_amount = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "form-control mb-2",  'placeholder': "Enter your bid here", "placeholder":'Enter an amount in US Dollars' }))


# class simpleListForm(forms.Form):
#     listing = forms.CharField(label="listing", widget=forms.TextInput(
#         attrs={'class': "form-control mb-2", 'required': True}))


# class commentForm(forms.Form):
#     comment = forms.CharField(label="Add a comment:", max_length=500,
#                               widget=forms.Textarea(attrs={'class': "form-control mb-2 mt-1", 'required': True}))