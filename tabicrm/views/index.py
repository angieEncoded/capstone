from django.contrib.auth import authenticate, login, logout
from django.http import  HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from ..models import Ticket
from django.db.models import Q
# looks like this is the express equivelent to flash
from django.contrib.auth.decorators import login_required
import re
# some refactoring, and some utility things to make my life more comfortable
from ..util import angie
from .. import forms

# my alias to print()
console = angie.Console()

# The open tickets view page - Dashboard
@login_required  # Can't enter the system without being logged in
def index(request):
    # Get the customers and tickets
    openTickets = Ticket.objects.exclude(status = "CLOSED").filter(owned_by = None)
    ownedTickets = Ticket.objects.exclude(status = "CLOSED").filter(owned_by = request.user)
    
    return render(request, "tabicrm/index.html", {
        "openTickets": openTickets,
        "ownedTickets": ownedTickets,
        "navopen_tickets": True
    })
