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
def edit_license_text_field(request, id, fieldName):

    # Get the content from the json object
    data = json.loads(request.body)
    replacement = data[fieldName]

    # validate it and send back if it fails
    if not contentValidator.match(replacement):
        return JsonResponse({"error": "There is something wrong with that input. Please check that you are using 2-255 alphanumeric characters. (server response)"})

    # save the item to the database if we got here and send data back to the front end
    try:
        contactToEdit = License.objects.get(id = id)
        setattr(contactToEdit, fieldName, replacement)
        contactToEdit.save()
        return JsonResponse({"success" :"Successfully saved your changes!", "content": replacement})
    except:
        return JsonResponse({"error" :"Something went wrong."})




