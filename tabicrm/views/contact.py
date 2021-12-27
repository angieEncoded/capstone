from django.http.response import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from ..models import Customer, Contact
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


# WORK ON SOME MORE ROBUST CONTENT VALIDATION LATER ON

# Set up some basic validation for the input
contentValidator = re.compile('^[a-zA-Z0-9.,!\"\'?:;\s@#$%^&*()[\]_+={}\-]{0,255}$')



# BACK END TEMPLATE LOGIC HERE
@login_required
def add_contact(request, id):

    if request.method == "POST":
        form = forms.NewContactForm(request.POST)
        customer = Customer.objects.get(id = id)

        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'You are trying to submit an invalid form.')
            return redirect("customer_full_form", id)

        # Assign all the fields
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        job_title = form.cleaned_data["job_title"]
        notes = form.cleaned_data["notes"]
        extension = form.cleaned_data["extension"]
        assigned_to = customer
        added_by = request.user
        updated_by = request.user

        contact = Contact(first_name=first_name, last_name=last_name, job_title=job_title, notes=notes, extension=extension,assigned_to=assigned_to, added_by=added_by, updated_by=updated_by)

        try:
            contact.save()
            messages.add_message(request, messages.SUCCESS,
                         "Successfully saved the contact.")
            return redirect("customer_full_form", id)
        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.ERROR,
                         error)
            return redirect("add_contact", id)

@login_required
def display_contacts(request, id):
    customer = Customer.objects.get(id = id)
    contacts = Contact.objects.filter(customer = customer)
    return render(request,"tabicrm/full_forms/display_contacts.html", {"contacts": contacts, 'customer': customer, 'cust_contacts': True })










# FRONT END ITEMS BELOW HERE - ALL JSON RESPONSES

@login_required
def get_customer_contacts(request, id):

    try:
        # get the customer from the database
        customer = Customer.objects.get(id = id)

        #get the contacts assigned to that customer
        contacts = Contact.objects.filter(customer = customer)

        # send them back in a json
        jsonContacts = serializers.serialize("json", contacts)

        return JsonResponse({"success": "Successfully retrieved data", "data": jsonContacts})
    except Exception as error:
        return JsonResponse({"error": error})


@login_required
def get_contact(request, id):
    try:
        #get the contacts assigned to that customer
        contact = Contact.objects.get(id = id)

        # send them back in a json
        jsonContact = serializers.serialize("json", [contact])

        return JsonResponse({"success": "Successfully retrieved data", "data": jsonContact})
    except Exception as error:
        console.log(error)
        return JsonResponse({"error": error})



@login_required
def edit_contact(request, id, fieldName):
        
    # Get the content from the json object
    data = json.loads(request.body)
    replacement = data[fieldName]

    # # validate it and send back if it fails
    if not contentValidator.match(replacement):
        return JsonResponse({"error": "There is something wrong with that input. Please check that you are using 2-255 alphanumeric characters. (server response)"})

    # save the item to the database if we got here and send data back to the front end
    try:
        contactToEdit = Contact.objects.get(id = id)
        setattr(contactToEdit, fieldName, replacement)
        contactToEdit.save()
        return JsonResponse({"success" :"Successfully saved your changes!", "content": replacement})
    except:
        return JsonResponse({"error" :"Something went wrong."})
