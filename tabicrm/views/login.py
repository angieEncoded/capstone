from django.contrib.auth import authenticate, login, logout
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import re


# some refactoring, and some utility things to make my life more comfortable
from ..util import angie

# my alias to print()
console = angie.Console()


# WORK ON SOME MORE ROBUST CONTENT VALIDATION LATER ON

# Set up some basic validation for the input
contentValidator = re.compile('^[a-zA-Z0-9.,!\"\'?:;\s@#$%^&*()[\]_+={}\-]{0,255}$')



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
