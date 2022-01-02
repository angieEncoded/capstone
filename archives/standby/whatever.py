
# I have no idea how this ended up lost..
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