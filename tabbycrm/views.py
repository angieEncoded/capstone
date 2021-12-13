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


def index(request):
    # this will be a login page
    return render(request, "tabbycrm/index.html")

def login(request):
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
            return render(request, "tabbycrm/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tabbycrm/login.html", {"navlogin":True})


def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))