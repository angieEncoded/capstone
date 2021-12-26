from django.http.response import FileResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from ..models import Customer, License
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

@login_required
def get_customer_licenses(request, id):

    try:

        # get the customer from the database
        customer = Customer.objects.get(id = id)

        #get the licenses assigned to that customer
        licenses = License.objects.filter(customer = customer)

        # console.log(licenses)

        # send them back in a json
        jsonLicenses = serializers.serialize("json", licenses)

        return JsonResponse({"success": "Successfully retrieved data", "data": jsonLicenses})
    except Exception as error:
        return JsonResponse({"error": error})


    pass

@login_required
def download_license(request, id):
    
    license = License.objects.get(id = id)
    response = FileResponse(open(license.license_file.name, 'rb'))
    return response

@login_required
def get_license(request, id):
    try:
        #get the contacts assigned to that customer
        license = License.objects.get(id = id)

        # send them back in a json
        jsonLicense = serializers.serialize("json", [license])

        return JsonResponse({"success": "Successfully retrieved data", "data": jsonLicense})
    except Exception as error:
        console.log(error)
        return JsonResponse({"error": error})
    pass


@login_required
def edit_license(request, id):

    if request.method == "GET":
        # get the license information
        license = License.objects.get(id = id)
        console.log(license.license_file)
        # Set it to a form
        form = forms.NewLicenseForm(initial={
           'product': license.product, 
           'purchase_date': license.purchase_date, 
           'expiration_date' : license.expiration_date,
           'customer' : license.customer, 
           'license_key' : license.license_key,
           'license_file' : license.license_file, 
           'notes' : license.notes, 
           'end_of_life' : license.end_of_life
        })

        return render(request, "tabicrm/edit_license.html", {'form': form, 'license_name': license.license_file, 'license_id': id})



    if request.method == "POST":

        form = forms.NewLicenseForm(request.POST, request.FILES)
        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return redirect(f"edit_license/{id}")

        # Assign all the fields
        product = form.cleaned_data["product"]
        purchase_date = form.cleaned_data["purchase_date"]
        expiration_date = form.cleaned_data["expiration_date"]
        customer = form.cleaned_data["customer"]
        license_key = form.cleaned_data["license_key"]
        notes = form.cleaned_data["notes"]
        end_of_life = form.cleaned_data["end_of_life"]

        # Get the current data from the license field
        currentLicense = License.objects.get(id = id)

        # if we have a file, None if we dont
        if request.FILES:
            license_file=request.FILES['license_file']
        else:
            license_file=currentLicense.license_file


        try:
            licenseToEdit = License.objects.get(id = id)
            setattr(licenseToEdit, 'product', product)
            setattr(licenseToEdit, 'purchase_date', purchase_date )
            setattr(licenseToEdit, 'expiration_date', expiration_date)
            setattr(licenseToEdit, 'customer', customer)
            setattr(licenseToEdit, 'license_key', license_key)
            setattr(licenseToEdit, 'notes', notes )
            setattr(licenseToEdit, 'end_of_life', end_of_life )
            setattr(licenseToEdit, 'license_file', license_file )
            licenseToEdit.save()
            messages.add_message(request, messages.SUCCESS,
                         "Successfully saved your changes.")
            return redirect(f"/edit_license/{id}")
        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.ERROR,
                         error)
            return redirect(f"/edit_license/{id}")

@login_required
def delete_license(request, id):

    if request.method == "POST":
        
        # Check and make sure we're getting what we expect
        form = request.POST.dict() # This will turn it into a 'dictionary'
        if not form['delete'] == 'True': # and remember, it isn't json, we have to use this other way because Python is the language of less unnecessary syntax.
            messages.add_message(request, messages.ERROR,
                         "I don't recognize that request. Please use the form to make your request.")
            return redirect(f"/edit_license/{id}")


        try:
            # find the record
            license = License.objects.get(id = id)
            license.delete()
            messages.add_message(request, messages.SUCCESS,
                         "Successfully deleted the record.")
            return redirect("/all_customers")


        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.ERROR,
                         error)
            return redirect(f"/edit_license/{id}")



































































