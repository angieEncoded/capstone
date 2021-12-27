from django.http.response import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from ..models import Customer, License, Contact
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
        added_by = request.user
        updated_by = request.user

        # Create the object
        customer = Customer(name=name, primary_phone=primary_phone, fax=fax, website=website, notes=notes, secondary_phone=secondary_phone, billing_address_one=billing_address_one,
                            billing_address_two=billing_address_two, billing_address_city=billing_address_city, billing_address_state=billing_address_state, 
                            billing_address_zip=billing_address_zip, billing_address_country=billing_address_country, shipping_address_one=shipping_address_one,
                            shipping_address_two=shipping_address_two, shipping_address_city=shipping_address_city, shipping_address_state=shipping_address_state,
                            shipping_address_zip=shipping_address_zip, shipping_address_country=shipping_address_country, added_by=added_by, updated_by=updated_by)
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


def customer_full_form(request, id):

    if request.method == "GET":

        customer = Customer.objects.get(id = id)
        
        newContactForm = forms.NewContactForm()
        newLicenseForm = forms.NewLicenseForm()
        newEquipmentForm = forms.newEquipmentForm()

        # Get the customer's initial form values
        customerForm = forms.newCustomerForm(initial={
            'name': customer.name,
            'primary_phone': customer.primary_phone,
            'secondary_phone': customer.secondary_phone,
            'fax': customer.fax,
            'website': customer.website,
            'notes': customer.notes,
            'billing_address_one': customer.billing_address_one,
            'billing_address_two': customer.billing_address_two,
            'billing_address_city': customer.billing_address_city,
            'billing_address_state': customer.billing_address_state,
            'billing_address_zip': customer.billing_address_zip,
            'billing_address_country': customer.billing_address_country,
            'shipping_address_one': customer.shipping_address_one,
            'shipping_address_two': customer.shipping_address_two,
            'shipping_address_city': customer.shipping_address_city,
            'shipping_address_state': customer.shipping_address_state,
            'shipping_address_zip': customer.shipping_address_zip,
            'shipping_address_country': customer.shipping_address_country
        })

        


        return render(request, "tabicrm/customer_full_form.html", {
            "form": customerForm,
            'newContactForm': newContactForm,
            'newLicenseForm': newLicenseForm,
            'newEquipmentForm': newEquipmentForm,
            'customer_name': customer.name,
            'customer_id': customer.id,
            'customer':customer,
        })

    if request.method == "POST":

        form = forms.newCustomerForm(request.POST)

        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return redirect("customer_full_form", id)

        try: 

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



            customerToEdit = Customer.objects.get(id = id)
            setattr(customerToEdit, 'name',  name)
            setattr(customerToEdit, 'primary_phone', primary_phone)
            setattr(customerToEdit, 'fax',  fax)
            setattr(customerToEdit, 'website',  website)
            setattr(customerToEdit, 'notes',  notes)
            setattr(customerToEdit, 'secondary_phone',  secondary_phone)
            setattr(customerToEdit, 'billing_address_one',  billing_address_one)
            setattr(customerToEdit, 'billing_address_two',  billing_address_two)
            setattr(customerToEdit, 'billing_address_city',  billing_address_city)
            setattr(customerToEdit, 'billing_address_state',  billing_address_state)
            setattr(customerToEdit, 'billing_address_zip',  billing_address_zip)
            setattr(customerToEdit, 'billing_address_country',  billing_address_country)
            setattr(customerToEdit, 'shipping_address_one',  shipping_address_one)
            setattr(customerToEdit, 'shipping_address_two',  shipping_address_two)
            setattr(customerToEdit, 'shipping_address_city',  shipping_address_city)
            setattr(customerToEdit, 'shipping_address_state',  shipping_address_state)
            setattr(customerToEdit, 'shipping_address_zip',  shipping_address_zip)
            setattr(customerToEdit, 'shipping_address_country',  shipping_address_country)
            customerToEdit.save()
            messages.add_message(request, messages.SUCCESS, "Successfully saved the changes!")
            return redirect("customer_full_form", id)

        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.ERROR, error)
            return redirect("customer_full_form", id)





def delete_customer(request, id):
    
    if request.method == "POST":
        try: 
            # Check and make sure we're getting what we expect
            form = request.POST.dict() # This will turn it into a 'dictionary'
            if not form['delete'] == 'True': # and remember, it isn't json, we have to use this other way because Python is the language of less unnecessary syntax.
                messages.add_message(request, messages.ERROR,"I don't recognize that request. Please use the form to make your request.")
                return redirect(f"/customer_full_form/{id}")
             
            customer = Customer.objects.get(id = id)
            customer.delete()

            messages.add_message(request, messages.SUCCESS,"Successfully deleted the customer.")
            return redirect("all_customers")

        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.SUCCESS, error)
            return redirect("all_customers")



