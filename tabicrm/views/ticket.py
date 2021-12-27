from os import stat
from django.http.response import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from ..models import Customer, Ticket
# looks like this is the express equivelent to flash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import re


# some refactoring, and some utility things to make my life more comfortable
from ..util import angie
from .. import forms

# my alias to print()
console = angie.Console()


@login_required
def display_tickets(request, id):
    customer = Customer.objects.get(id = id)
    tickets = Ticket.objects.filter(customer = customer)
    return render(request,"tabicrm/full_forms/display_tickets.html", {"tickets": tickets, 'customer': customer, 'cust_tickets': True })


@login_required
def add_ticket(request, id):


    if request.method == "POST":



        form = forms.NewTicketForm(request.POST)
        customer = Customer.objects.get(id = id)
        user = request.user

        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return redirect("customer_full_form", id)


        # Assign all the fields
        assigned_to = form.cleaned_data["assigned_to"]
        title = form.cleaned_data["title"]
        status = form.cleaned_data["status"]
        priority = form.cleaned_data["priority"]
        results = form.cleaned_data["results"]
        description = form.cleaned_data["description"]
        solution = form.cleaned_data["solution"]
        added_by = user
        updated_by = user

   

        ticket = Ticket(
            customer=customer,
            assigned_to=assigned_to,
            title=title, 
            status=status,
            priority=priority,
            results=results,
            description=description,
            solution=solution,
            added_by = added_by,
            updated_by = updated_by
        )

        try:
            ticket.save()
            messages.add_message(request, messages.SUCCESS,
                         "Successfully saved the ticket.")
            return redirect("customer_full_form", id)
        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.ERROR,
                         error)
            return redirect("customer_full_form", id)