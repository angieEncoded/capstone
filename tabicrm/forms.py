from django import forms
from django.db.models.fields import DateField
from django.forms import Form, ModelForm, TextInput, Textarea, Select
from django.forms.fields import FileField
from django.forms.widgets import DateInput, FileInput, Widget
from .models import Customer, Contact, License


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

# Apparently need to create a custom input to show the datepicker - crazy that this isn't a default and 
# has been this way for seven years... and isn't clarified in the docs. 
# https://stackoverflow.com/questions/22846048/django-form-as-p-datefield-not-showing-input-type-as-date
class DateInput(forms.DateInput):
    input_type = 'date'




class NewLicenseForm(ModelForm):
    class Meta:
        model = License
        fields = ('product', 'purchase_date', 'expiration_date','customer', 'license_key', 'license_file', 'notes','end_of_life')
        widgets = {
            'product': Select(attrs={'class': "form-select mb-2", 'placeholder': ""}),
            'purchase_date' : DateInput(attrs={'class': "form-control mb-2", 'placeholder': ""}),
            'expiration_date': DateInput(attrs={'class': "form-control mb-2", 'placeholder': ""}),
            'customer':  Select(attrs={'class': "form-select mb-2", 'placeholder': ""}),
            'license_key': TextInput(attrs={'class': "form-control mb-2", 'placeholder': ""}),
            'license_file': FileInput(attrs={'class': "form-control mb-2", 'placeholder': ""}),
            'notes': Textarea(attrs={'rows': 3,'class': "form-control mb-2", 'placeholder': ""}),
            'end_of_life': DateInput(attrs={'class': "form-control mb-2", 'placeholder': ""}),
        }

# Note to self - after MUCH googling and about three hours of searching, there is no good, clean answer to the issue of the wonky date formats. I am making the design decision to just... leave it as it is. 
