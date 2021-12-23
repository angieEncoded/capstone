from django.http.response import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from ..models import Customer
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


@login_required
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
        notes = form.cleaned_data["notes"]
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
        customer = Customer(name=name, primary_phone=primary_phone, fax=fax, website=website, notes=notes, secondary_phone=secondary_phone, billing_address_one=billing_address_one,
                            billing_address_two=billing_address_two, billing_address_city=billing_address_city, billing_address_state=billing_address_state, 
                            billing_address_zip=billing_address_zip, billing_address_country=billing_address_country, shipping_address_one=shipping_address_one,
                            shipping_address_two=shipping_address_two, shipping_address_city=shipping_address_city, shipping_address_state=shipping_address_state,
                            shipping_address_zip=shipping_address_zip, shipping_address_country=shipping_address_country)
        try:
            customer.save()
            messages.add_message(request, messages.SUCCESS,
                         "Successfully saved the customer.")
            return redirect("all_customers")
        except:
            messages.add_message(request, messages.ERROR,
                         "Something unexpected happened while trying to save that record. Please try again. If the problem persists, contact the developer.")
            return redirect("all_customers")



    messages.add_message(request, messages.ERROR,
                         "I don't recognize that request. Returning to the home page.")
    return redirect("index")

@login_required
def all_customers(request):
    customers = Customer.objects.all()
    return render(request,"tabicrm/all_customers.html", {"customers": customers})

@login_required
def view_customer(request, id):
    customer = Customer.objects.get(id = id)
    jsonCustomer = serializers.serialize("json", [customer])
    return JsonResponse({"success": "Successfully retrieved data", "data": jsonCustomer})

@login_required
def edit_customer(request, id, fieldName):
    
    # Get the content from the json object
    data = json.loads(request.body)
    replacement = data[fieldName]

    # # validate it and send back if it fails
    if not contentValidator.match(replacement):
        return JsonResponse({"error": "There is something wrong with that input. Please check that you are using 2-255 alphanumeric characters. (server response)"})

    # save the item to the database if we got here and send data back to the front end
    try:
        customerToEdit = Customer.objects.get(id = id)
        console.log(customerToEdit)
        setattr(customerToEdit, fieldName, replacement)
        customerToEdit.save()
        return JsonResponse({"success" :"Successfully saved your changes!", "content": replacement})
    except:
        return JsonResponse({"error" :"Something went wrong."})
