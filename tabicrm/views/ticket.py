from os import stat
from django.http.response import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from ..models import Customer, Ticket, TicketHistory, TicketComment
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
        customerId = customer.id

        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return redirect("customer_full_form", customerId)


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
        owned_by = user
   


        try:
            # interestingly, Python does not return an instance of the object unless we use this format https://stackoverflow.com/questions/10936737/why-does-django-orms-save-method-not-return-the-saved-object
            result = Ticket.objects.create(
            customer=customer,
            assigned_to=assigned_to,
            title=title, 
            status=status,
            priority=priority,
            results=results,
            description=description,
            solution=solution,
            added_by = added_by,
            updated_by = updated_by,
            owned_by = owned_by
        )

            # console.log(result)
            # Add to the history
            action = "Ticket Created"
            ticket = result
            taken_by = user

            ticketAction = TicketHistory(
                action = action,
                ticket=ticket,
                taken_by=taken_by
            )
            ticketAction.save()

            messages.add_message(request, messages.SUCCESS,
                         "Successfully saved the ticket.")
            return redirect("display_tickets", customerId)
        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.ERROR,
                         error)
            return redirect("customer_full_form", customerId)



def view_single_ticket(request, ticketId):
    
    if request.method == "GET":
        ticket = Ticket.objects.get(id = ticketId)
        customer = ticket.customer
        ticketComments = TicketComment.objects.filter(ticket = ticket)
        ticketHistory = TicketHistory.objects.filter(ticket = ticket)
        commentForm = forms.NewTicketCommentForm()
        return render(request,"tabicrm/full_forms/full_edit_ticket.html", {
            "ticket": ticket, 
            'customer': customer, 
            'ticketComments': ticketComments,
            'ticketHistory': ticketHistory,
            'cust_tickets': True, 
            'commentForm':commentForm })

def add_ticket_comment(request, ticketId):

    if request.method == "POST":
        form = forms.NewTicketCommentForm(request.POST)
        ticket = Ticket.objects.get(id = ticketId)
        user = request.user

        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return redirect("view_single_ticket", ticketId)

        comment = form.cleaned_data["comment"]
        added_by = user
        updated_by = user
        ticketComment = TicketComment(comment=comment, added_by=added_by, updated_by=updated_by,ticket=ticket)

        # Add an entry into the ticket history


        action = "Comment Added"
        ticket = ticket
        taken_by = user

        ticketAction = TicketHistory(
            action = action,
            ticket=ticket,
            taken_by=taken_by
        )
        ticketAction.save()


        try:
            ticketComment.save()
            messages.add_message(request, messages.SUCCESS,
                         "Successfully saved the comment.")
            return redirect("view_single_ticket", ticketId)
        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.ERROR,
                         error)
            return redirect("view_single_ticket", ticketId)




def full_edit_ticket(request, ticketId):
    pass































