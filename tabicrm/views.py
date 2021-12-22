from django.http.response import FileResponse, JsonResponse
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.db import IntegrityError
from django.forms.widgets import Select
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Customer, Contact, License
# looks like this is the express equivelent to flash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import re


# some refactoring, and some utility things to make my life more comfortable
from .util import angie
from . import forms

# my alias to print()
console = angie.Console()


# WORK ON SOME MORE ROBUST CONTENT VALIDATION LATER ON

# Set up some basic validation for the input
contentValidator = re.compile('^[a-zA-Z0-9.,!\"\'?:;\s@#$%^&*()[\]_+={}\-]{0,255}$')

@login_required  # Can't enter the system without being logged in
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
        return render(request, "tabicrm/login.html", {"navlogin": True})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

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



@login_required
def add_contact(request):

    if request.method == "GET":
        form = forms.NewContactForm()
        return render(request, "tabicrm/add_contact.html", {
            "form": form,
            "navadd_contact": True
        })


    if request.method == "POST":
        form = forms.NewContactForm(request.POST)
        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return redirect("add_contact")

        # Assign all the fields
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        job_title = form.cleaned_data["job_title"]
        notes = form.cleaned_data["notes"]
        extension = form.cleaned_data["extension"]
        assigned_to = form.cleaned_data["assigned_to"]

        contact = Contact(first_name=first_name, last_name=last_name, job_title=job_title, notes=notes, extension=extension,assigned_to=assigned_to)

        try:
            contact.save()
            messages.add_message(request, messages.SUCCESS,
                         "Successfully saved the contact.")
            return redirect("add_contact")
        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.ERROR,
                         error)
            return redirect("add_contact")



@login_required
def get_customer_contacts(request, id):

    try:
        # get the customer from the database
        customer = Customer.objects.get(id = id)

        #get the contacts assigned to that customer
        contacts = Contact.objects.filter(assigned_to = customer)

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

@login_required
def add_license(request):

    if request.method == "GET":
        form = forms.NewLicenseForm()
        return render(request, "tabicrm/add_license.html", {
            "form": form,
            "navadd_license": True
        })


    if request.method == "POST":
        form = forms.NewLicenseForm(request.POST, request.FILES)
        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return redirect("add_license")


        # Assign all the fields
        product = form.cleaned_data["product"]
        purchase_date = form.cleaned_data["purchase_date"]
        expiration_date = form.cleaned_data["expiration_date"]
        customer = form.cleaned_data["customer"]
        license_key = form.cleaned_data["license_key"]
        notes = form.cleaned_data["notes"]
        end_of_life = form.cleaned_data["end_of_life"]


        # if we have a file, None if we dont
        if request.FILES:
            license_file=request.FILES['license_file']
        else:
            license_file=None

        license = License(
            product=product, 
            purchase_date=purchase_date, 
            expiration_date=expiration_date, 
            customer=customer, 
            license_key=license_key, 
            notes=notes, 
            end_of_life=end_of_life, 
            license_file=license_file, 
            added_by = request.user
        )

        try:
            license.save()
            messages.add_message(request, messages.SUCCESS,
                         "Successfully saved the license.")
            return redirect("add_license")
        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.ERROR,
                         error)
            return redirect("add_license")


def get_customer_licenses(request, id):

    try:

        # get the customer from the database
        customer = Customer.objects.get(id = id)

        #get the licenses assigned to that customer
        licenses = License.objects.filter(customer = customer)

        console.log(licenses)

        # send them back in a json
        jsonLicenses = serializers.serialize("json", licenses)

        return JsonResponse({"success": "Successfully retrieved data", "data": jsonLicenses})
    except Exception as error:
        return JsonResponse({"error": error})


    pass

def download_license(request, id):
    
    license = License.objects.get(id = id)
    response = FileResponse(open(license.license_file.name, 'rb'))
    return response



def customer_full_form(request, id):

    # Get the customer's initial form values
    customer = Customer.objects.get(id = id)
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

    # Get the list of licenses 


    # Get the list of contacts

    return render(request, "tabicrm/customer_full_form.html", {
        "form": customerForm,
    })


















