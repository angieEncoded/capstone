from django.http.response import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from ..models import Customer, Equipment
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
def display_equipment(request, id):
    customer = Customer.objects.get(id = id)
    equipments = Equipment.objects.filter(customer = customer)
    return render(request,"tabicrm/full_forms/display_equipment.html", {"equipments": equipments, 'customer': customer, 'cust_equipment': True })


def full_edit_equipment(request, equipmentId):

    if request.method == "GET":

        equipment = Equipment.objects.get(id = equipmentId)
        customer = equipment.customer
        editEquipmentForm = forms.NewEquipmentForm(initial={
            'type': equipment.type,
            'vendor':equipment.vendor,
            'model':equipment.model,
            'os_version':equipment.os_version,
            'pruchase_date':equipment.purchase_date,
            'warranty_end_date':equipment.warranty_end_date,
            'end_of_life':equipment.end_of_life,
            'internal_ip_address':equipment.internal_ip_address,
            'external_ip_address':equipment.external_ip_address,
            'subnet_mask':equipment.subnet_mask,
            'default_gateway':equipment.default_gateway,
            'primary_dns':equipment.primary_dns,
            'secondary_dns':equipment.secondary_dns,
            'serial_number':equipment.serial_number,
            'product_number':equipment.product_number,
        })
    
        return render(request, "tabicrm/full_forms/edit_equipment.html", {
            "editEquipmentForm": editEquipmentForm,
            'customer_name': customer.name,
            'customer_id': customer.id,
            'customer':customer,
            'equipment': equipment,
            'cust_equipment': True
        })

    pass



@login_required
def add_equipment(request, id):


    if request.method == "POST":



        form = forms.NewEquipmentForm(request.POST)
        customer = Customer.objects.get(id = id)
        user = request.user

        # Short circuit if the form is bad
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return redirect("customer_full_form", id)


        # Assign all the fields
        type = form.cleaned_data["type"]
        vendor = form.cleaned_data["vendor"]
        model = form.cleaned_data["model"]
        os_version = form.cleaned_data["os_version"]
        purchase_date = form.cleaned_data["purchase_date"]
        warranty_end_date = form.cleaned_data["warranty_end_date"]
        end_of_life = form.cleaned_data["end_of_life"]
        internal_ip_address = form.cleaned_data["internal_ip_address"]
        external_ip_address = form.cleaned_data["external_ip_address"]
        subnet_mask = form.cleaned_data["subnet_mask"]
        default_gateway = form.cleaned_data["default_gateway"]
        primary_dns = form.cleaned_data["dns_one"]
        secondary_dns = form.cleaned_data["primary_dns"]
        serial_number = form.cleaned_data["serial_number"]
        product_number = form.cleaned_data["product_number"]
        notes = form.cleaned_data["notes"]
        added_by = user
        updated_by = user

   

        equipment = Equipment(
            customer=customer,
            type=type,
            vendor=vendor,
            model= model,
            os_version=os_version, 
            purchase_date=purchase_date, 
            warranty_end_date=warranty_end_date, 
            end_of_life=end_of_life,
            internal_ip_address=internal_ip_address,
            external_ip_address=external_ip_address,
            subnet_mask=subnet_mask,
            default_gateway=default_gateway,
            primary_dns=primary_dns,
            secondary_dns= secondary_dns,
            serial_number=serial_number,
            product_number=product_number,
            notes=notes, 
            added_by = added_by,
            updated_by = updated_by
        )

        try:
            equipment.save()
            messages.add_message(request, messages.SUCCESS,
                         "Successfully saved the equipment.")
            return redirect("customer_full_form", id)
        except Exception as error:
            console.log(error)
            messages.add_message(request, messages.ERROR,
                         error)
            return redirect("customer_full_form", id)