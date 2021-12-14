from .models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.widgets import Select
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
# from .models import Category, Auction, Watchlist, Bid, Comment
# looks like this is the express equivelent to flash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# some refactoring, and some utility things to make my life more comfortable
from . import angie
from . import forms
# my alias to print()

console = angie.Console()

@login_required # Can't enter the system without being logged in
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
        return render(request, "tabicrm/login.html", {"navlogin":True})

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

    return render(request, "tabicrm/add_customer.html", {"navadd_customer": True})
    pass