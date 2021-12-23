refactoring learned from here
https://vsupalov.com/large-django-views-file/

That wasn't enough, also had to do this
https://simpleisbetterthancomplex.com/tutorial/2016/08/02/how-to-split-views-into-multiple-files.html







# CODE THAT IS ON STANDBY DOWN HERE - MAYBE WILL RUN WITH IT MAYBE NOT


# def customer_full_form(request, id):

#     # Get the customer's initial form values
#     customer = Customer.objects.get(id = id)
#     customerForm = forms.newCustomerForm(initial={
#         'name': customer.name,
#         'primary_phone': customer.primary_phone,
#         'secondary_phone': customer.secondary_phone,
#         'fax': customer.fax,
#         'website': customer.website,
#         'notes': customer.notes,
#         'billing_address_one': customer.billing_address_one,
#         'billing_address_two': customer.billing_address_two,
#         'billing_address_city': customer.billing_address_city, 
#         'billing_address_state': customer.billing_address_state,
#         'billing_address_zip': customer.billing_address_zip,
#         'billing_address_country': customer.billing_address_country,
#         'shipping_address_one': customer.shipping_address_one,
#         'shipping_address_two': customer.shipping_address_two,
#         'shipping_address_city': customer.shipping_address_city, 
#         'shipping_address_state': customer.shipping_address_state,
#         'shipping_address_zip': customer.shipping_address_zip,
#         'shipping_address_country': customer.shipping_address_country
#     })

#     # Get the list of licenses 


#     # Get the list of contacts

#     return render(request, "tabicrm/customer_full_form.html", {
#         "form": customerForm,
#     })













