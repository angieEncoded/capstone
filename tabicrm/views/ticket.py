from os import stat
from django.contrib.auth import login
from django.http.response import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from ..models import Customer, Ticket, TicketHistory, TicketComment, User
# looks like this is the express equivelent to flash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.utils.http import urlencode


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
            owned_by = None
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


@login_required
def view_single_ticket(request, ticketId):
    
    if request.method == "GET":
        ticket = Ticket.objects.get(id = ticketId)
        customer = ticket.customer
        ticketComments = TicketComment.objects.filter(ticket = ticket)
        ticketHistory = TicketHistory.objects.filter(ticket = ticket)
        commentForm = forms.NewTicketCommentForm()
        ticketForm = forms.NewTicketForm(initial={
            'assigned_to': ticket.assigned_to,
            'status': ticket.status, 
            'priority': ticket.priority,
            'results': ticket.results,
            'title':ticket.title,
            'description': ticket.description,
            'solution': ticket.solution
        })
        return render(request,"tabicrm/full_forms/full_edit_ticket.html", {
            "ticket": ticket, 
            'customer': customer, 
            'ticketComments': ticketComments,
            'ticketHistory': ticketHistory,
            'cust_tickets': True, 
            'commentForm':commentForm,
            'editTicketForm': ticketForm })

@login_required
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

def post_new_ticket(request, customerId):

    if request.method == "POST":
        
        customer = Customer.objects.get(id = customerId)
        user = request.user
        customerId = customer.id

        form = forms.NewTicketForm(request.POST)
        
        if not form.is_valid():
            return JsonResponse({"error":"Form is not valid"})
        
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
        owned_by = None
   
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
            # return JsonResponse({"success":"Successfully opened the ticket", "ticket_number": "TEST"})
            return JsonResponse({"success":"Successfully opened the ticket", "ticket_number": result.id})

        except Exception as error:
            console.log(error)
            return JsonResponse({"error":"Unable to process that request."})














    return JsonResponse({"Success": "Success"})
    


@login_required
def ticket_actions(request, ticketId, action):
    # possible actions:
    # accept
    # customer
    # close

    if request.method == "GET":

        user = request.user
        ticket = Ticket.objects.get(id = ticketId)

        # Accept ticket logic
        if action == "accept":
            try: 

                ticketAction = TicketHistory(
                    action = "Accepted Ticket",
                    ticket=ticket,
                    taken_by=user
                )
                ticketAction.save()

                setattr(ticket, 'owned_by',  request.user)
                setattr(ticket, 'status',  "IN PROGRESS")
                ticket.save()
                messages.add_message(request, messages.SUCCESS, "Accepted the ticket")
            except Exception as error:
                console.log(error)
                messages.add_message(request, messages.ERROR, error)
                return redirect("view_single_ticket", ticketId)
    
        if action == "customer":
            try: 

                ticketAction = TicketHistory(
                    action = "Set status to waiting on customer",
                    ticket=ticket,
                    taken_by=user
                )
                ticketAction.save()
                setattr(ticket, 'status',  'WAITING ON CUSTOMER')
                ticket.save()
                messages.add_message(request, messages.SUCCESS, "Set status to WAITING ON CUSTOMER")
            except Exception as error:
                console.log(error)
                messages.add_message(request, messages.ERROR, error)
                return redirect("view_single_ticket", ticketId)

        if action == "close":
            try: 

                ticketAction = TicketHistory(
                    action = "Ticket Closed",
                    ticket=ticket,
                    taken_by=user
                )
                ticketAction.save()
                setattr(ticket, 'status',  'CLOSED')
                ticket.save()
                messages.add_message(request, messages.SUCCESS, "Ticket closed")
            except Exception as error:
                console.log(error)
                messages.add_message(request, messages.ERROR, error)
                return redirect("view_single_ticket", ticketId)   
        
        if action == "resume":
            try: 
                ticketAction = TicketHistory(
                    action = "Set status to IN PROGRESS",
                    ticket=ticket,
                    taken_by=user
                )
                ticketAction.save()
                setattr(ticket, 'status',  'IN PROGRESS')
                messages.add_message(request, messages.SUCCESS, "Resumed ticket")
                ticket.save()
            except Exception as error:
                console.log(error)
                messages.add_message(request, messages.ERROR, error)
                return redirect("view_single_ticket", ticketId)  

        if action == "reopen":
            try: 
                ticketAction = TicketHistory(
                    action = "Reopened closed Ticket",
                    ticket=ticket,
                    taken_by=user
                )
                ticketAction.save()
                setattr(ticket, 'status',  'IN PROGRESS')
                setattr(ticket, 'owned_by',  request.user)
                messages.add_message(request, messages.SUCCESS, "Resumed ticket")
                ticket.save()
            except Exception as error:
                console.log(error)
                messages.add_message(request, messages.ERROR, error)
                return redirect("view_single_ticket", ticketId)  
        
        return redirect("view_single_ticket", ticketId)   

@login_required
def full_edit_ticket(request, ticketId):
    # get the form data
    
    if request.method == "POST":
        form = forms.NewTicketForm(request.POST)

        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return redirect("view_single_ticket", ticketId)

        try: 

            assigned_to = form.cleaned_data["assigned_to"]
            title = form.cleaned_data["title"]
            status = form.cleaned_data["status"]
            priority = form.cleaned_data["priority"]
            results = form.cleaned_data["results"]
            description = form.cleaned_data["description"]
            solution = form.cleaned_data["solution"]
            updated_by = request.user
            

            ticketToEdit = Ticket.objects.get(id = ticketId)
            setattr(ticketToEdit, 'assigned_to',  assigned_to)
            setattr(ticketToEdit, 'title',  title)
            setattr(ticketToEdit, 'status',  status)
            setattr(ticketToEdit, 'priority',  priority)
            setattr(ticketToEdit, 'results',  results)
            setattr(ticketToEdit, 'description',  description)
            setattr(ticketToEdit, 'solution',  solution)
            setattr(ticketToEdit, 'updated_by',  updated_by)

            ticketToEdit.save()
            messages.add_message(request, messages.SUCCESS, "Successfully saved the changes!")
            return redirect("view_single_ticket", ticketId)

        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.ERROR, error)
            return redirect("view_single_ticket", ticketId)


    pass






























