from django.contrib import admin
from .models import User, Customer, License, Equipment, Ticket
from django.contrib.auth.admin import UserAdmin # Import this to allow us to adjust the user passwords in the admin module

# Helpful post to configure custom fields in the django admin interface
# https://stackoverflow.com/questions/48011275/custom-user-model-fields-abstractuser-not-showing-in-django-admin/48013640
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Custom Fields',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'role',
                    'title',
                    'department',
                    'extension',
                    'cellphone',
                    'street',
                    'city',
                    'state',
                    'zip',
                    'country',
                ),
            },
        ),
    )

class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "primary_phone", "fax", "secondary_phone")

class LicenseAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "purchase_date", "expiration_date", "customer", "license_key", "license_file")

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vendor', 'model')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'title',)

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Ticket, TicketAdmin)

