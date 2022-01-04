refactoring learned from here
https://vsupalov.com/large-django-views-file/

That wasn't enough, also had to do this
https://simpleisbetterthancomplex.com/tutorial/2016/08/02/how-to-split-views-into-multiple-files.html







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












