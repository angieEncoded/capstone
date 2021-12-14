from .models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.widgets import Select
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Customer
# looks like this is the express equivelent to flash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# some refactoring, and some utility things to make my life more comfortable
from . import angie
from . import forms
# my alias to print()

console = angie.Console()


@login_required  # Can't enter the system without being logged in
def index(request):

    return render(request, "tabicrm/index.html")


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
            return render(request, "tabicrm/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tabicrm/login.html", {"navlogin": True})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def add_customer(request):
    if request.method == "GET":
        form = forms.newCustomerForm()
        return render(request, "tabicrm/add_customer.html", {
            "form": form,
            "navadd_customer": True
        })

    if request.method == "POST":
        form = forms.newCustomerForm(request.POST)
        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return redirect("add_customer")

        # Assign all the fields
        name = form.cleaned_data["name"]
        primary_phone = form.cleaned_data["primary_phone"]
        fax = form.cleaned_data["fax"]
        website = form.cleaned_data["website"]
        secondary_phone = form.cleaned_data["secondary_phone"]
        billing_address_one = form.cleaned_data["billing_address_one"]
        billing_address_two = form.cleaned_data["billing_address_two"]
        billing_address_city = form.cleaned_data["billing_address_city"]
        billing_address_state = form.cleaned_data["billing_address_state"]
        billing_address_zip = form.cleaned_data["billing_address_zip"]
        billing_address_country = form.cleaned_data["billing_address_country"]
        shipping_address_one = form.cleaned_data["shipping_address_one"]
        shipping_address_two = form.cleaned_data["shipping_address_two"]
        shipping_address_city = form.cleaned_data["shipping_address_city"]
        shipping_address_state = form.cleaned_data["shipping_address_state"]
        shipping_address_zip = form.cleaned_data["shipping_address_zip"]
        shipping_address_country = form.cleaned_data["shipping_address_country"]

        # Create the object
        customer = Customer(name=name, primary_phone=primary_phone, fax=fax, website=website, secondary_phone=secondary_phone, billing_address_one=billing_address_one,
                            billing_address_two=billing_address_two, billing_address_city=billing_address_city, billing_address_state=billing_address_state, 
                            billing_address_zip=billing_address_zip, billing_address_country=billing_address_country, shipping_address_one=shipping_address_one,
                            shipping_address_two=shipping_address_two, shipping_address_city=shipping_address_city, shipping_address_state=shipping_address_state,
                            shipping_address_zip=shipping_address_zip, shipping_address_country=shipping_address_country)
        try:
            customer.save()
            messages.add_message(request, messages.SUCCESS,
                         "Successfully saved the customer.")
            return redirect("index")
        except:
            messages.add_message(request, messages.ERROR,
                         "Something unexpected happened while trying to save that record. Please try again. If the problem persists, contact the developer.")
            return redirect("new_customer")



    messages.add_message(request, messages.ERROR,
                         "I don't recognize that request. Returning to the home page.")
    return redirect("index")
