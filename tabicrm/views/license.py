from django.http.response import FileResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from ..models import Customer, License
# looks like this is the express equivelent to flash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re
import os


# some refactoring, and some utility things to make my life more comfortable
from ..util import angie
from .. import forms

# my alias to print()
console = angie.Console()


# WORK ON SOME MORE ROBUST CONTENT VALIDATION LATER ON

# Set up some basic validation for the input
contentValidator = re.compile('^[a-zA-Z0-9.,!\"\'?:;\s@#$%^&*()[\]_+={}\-]{0,255}$')


@login_required
def add_license(request, customerId):


    if request.method == "POST":

        form = forms.NewLicenseForm(request.POST, request.FILES)
        customer = Customer.objects.get(id = customerId)
        user = request.user

        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return redirect("customer_full_form", customerId)


        # Assign all the fields
        product = form.cleaned_data["product"]
        purchase_date = form.cleaned_data["purchase_date"]
        expiration_date = form.cleaned_data["expiration_date"]
        license_key = form.cleaned_data["license_key"]
        notes = form.cleaned_data["notes"]
        end_of_life = form.cleaned_data["end_of_life"]
        added_by = request.user
        updated_by = request.user

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
            added_by = added_by,
            updated_by = updated_by
        )

        try:
            license.save()
            messages.add_message(request, messages.SUCCESS,
                         "Successfully saved the license.")
            return redirect("customer_full_form", customerId)
        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.ERROR,
                         error)
            return redirect("customer_full_form", customerId)

@login_required
def get_customer_licenses(request, customerId):

    try:

        # get the customer from the database
        customer = Customer.objects.get(id = customerId)

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
def download_license(request, licenseId):
    
    license = License.objects.get(id = licenseId)
    response = FileResponse(open(license.license_file.name, 'rb'))
    return response

@login_required
def get_license(request, licenseId):
    try:
        #get the contacts assigned to that customer
        license = License.objects.get(id = licenseId)

        # send them back in a json
        jsonLicense = serializers.serialize("json", [license])

        return JsonResponse({"success": "Successfully retrieved data", "data": jsonLicense})
    except Exception as error:
        console.log(error)
        return JsonResponse({"error": error})
    pass

@login_required
def delete_license(request, licenseId):

    if request.method == "POST":
        
        # Check and make sure we're getting what we expect
        form = request.POST.dict() # This will turn it into a 'dictionary'
        if not form['delete'] == 'True': # and remember, it isn't json, we have to use this other way because Python is the language of less unnecessary syntax.
            messages.add_message(request, messages.ERROR,
                         "I don't recognize that request. Please use the form to make your request.")
            return redirect("/edit_license", licenseId)

        # find the record
        license = License.objects.get(id = licenseId)
        customer = license.customer

        try:

            license.delete()
            messages.add_message(request, messages.SUCCESS,
                         "Successfully deleted the record.")
            return redirect("display_licenses", customer.id)


        except Exception as error:
            # console.log(error)
            messages.add_message(request, messages.ERROR,
                         error)
            return redirect("edit_license", licenseId)

@login_required
def display_licenses(request, customerId):
    
    # get all the customer licenses and render the table
    if request.method == "GET":
        customer = Customer.objects.get(id = customerId)
        licenses = License.objects.filter(customer = customer)
        return render(request, "tabicrm/full_forms/display_licenses.html", {"customer": customer, "licenses": licenses, "cust_licenses": True})

@login_required
def full_edit_license(request, licenseId):

    # Get the license details and render the edit form
    if request.method == "GET":
        license = License.objects.get(id = licenseId)
        customer = Customer.objects.get(id = license.customer.id)
        editLicenseForm = forms.NewLicenseForm(initial= {
            'product':license.product, 
            'purchase_date':license.purchase_date, 
            'expiration_date':license.expiration_date, 
            'customer':license.customer, 
            'license_key':license.license_key, 
            'notes':license.notes, 
            'end_of_life':license.end_of_life, 
            'license_file':license.license_file, 
        })

        return render(request, "tabicrm/full_forms/full_edit_license.html", {
            "editLicenseForm": editLicenseForm,
            'customer_name': customer.name,
            'customer_id': customer.id,
            'customer':customer,
            'license': license,
            'cust_licenses': True
        })

    if request.method == "POST":

        # get the form data
        form = forms.NewLicenseForm(request.POST, request.FILES)
        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return redirect("full_edit_license", licenseId)

        try: 
            product = form.cleaned_data["product"]
            purchase_date = form.cleaned_data["purchase_date"]
            expiration_date = form.cleaned_data["expiration_date"]
            license_key = form.cleaned_data["license_key"]
            license_file = form.cleaned_data["license_file"]
            notes = form.cleaned_data["notes"]
            end_of_life = form.cleaned_data["end_of_life"]
            updated_by = request.user
                    
            # Get the current data from the license field
            currentLicense = License.objects.get(id = licenseId)

            # if we have a file unlink the old file, set to None if we don't which will leave the record alone
            if request.FILES:
                license_file=request.FILES['license_file']
                if currentLicense.license_file:
                    os.unlink(str(currentLicense.license_file))
            else:
                license_file=currentLicense.license_file


            # Get the contact being edited
            licenseToEdit = License.objects.get(id = licenseId)
            customerId = licenseToEdit.customer.id


            # set all the attributes to what we got from the form
            setattr(licenseToEdit, 'product',  product)
            setattr(licenseToEdit, 'purchase_date',  purchase_date)
            setattr(licenseToEdit, 'expiration_date',  expiration_date)
            setattr(licenseToEdit, 'license_key',  license_key)
            setattr(licenseToEdit, 'license_file',  license_file)
            setattr(licenseToEdit, 'notes',  notes)
            setattr(licenseToEdit, 'end_of_life',  end_of_life)
            setattr(licenseToEdit, 'updated_by',  updated_by)

            # Save the contact and go back to all the customer's contacts
            licenseToEdit.save()
            messages.add_message(request, messages.SUCCESS, "Successfully saved the changes!")
            return redirect("display_licenses", customerId)

        except Exception as error:
            messages.add_message(request, messages.ERROR, error)
            return redirect("full_edit_license", licenseId)































































