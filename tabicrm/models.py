from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import related
from django.db.utils import NotSupportedError

# REMEMBER - IF YOU DECIDE TO RENAME THE APP AGAIN AND MESS WITH THE MIGRATIONS YOU HAVE TO DO THIS
# https://stackoverflow.com/questions/36153748/django-makemigrations-no-changes-detected
# https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html


# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=64)
    title = models.CharField(max_length=64, null=True, blank=True)
    department = models.CharField(max_length=64, null=True, blank=True)
    extension = models.CharField(max_length=64, null=True, blank=True)
    cellphone = models.CharField(max_length=64, null=True, blank=True)
    street = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=64, null=True, blank=True)
    zip = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=True)

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    primary_phone = models.CharField(max_length=255)
    fax =  models.CharField(max_length=255, null=True, blank=True)
    secondary_phone =  models.CharField(max_length=64, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    # PRIMARY Address details
    billing_address_one = models.CharField(max_length=255, null=True, blank=True)
    billing_address_two = models.CharField(max_length=255, null=True, blank=True)
    billing_address_city = models.CharField(max_length=255, null=True, blank=True)
    billing_address_state = models.CharField(max_length=255, null=True, blank=True)
    billing_address_zip = models.CharField(max_length=255, null=True, blank=True)
    billing_address_country = models.CharField(max_length=255, null=True, blank=True)
    # SECONDARY Address Details
    shipping_address_one = models.CharField(max_length=255, null=True, blank=True)
    shipping_address_two = models.CharField(max_length=255, null=True, blank=True)
    shipping_address_city = models.CharField(max_length=255, null=True, blank=True)
    shipping_address_state = models.CharField(max_length=255, null=True, blank=True)
    shipping_address_zip = models.CharField(max_length=255, null=True, blank=True)
    shipping_address_country = models.CharField(max_length=255, null=True, blank=True)

    # Set this up to represent the object in the select field - this is how django represents objects
    def __str__(this):
        return f"{this.name}"



class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name =  models.CharField(max_length=255,blank=True, null=True)
    job_title =   models.CharField(max_length=255,blank=True, null=True)
    extension = models.CharField(max_length=255,blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="contact_customer")

    def __str__(this):
        return f"{this.first_name} {this.last_name}"



# class License(models.Model):
#     id = models.AutoField(primary_key=True)
#     type = models.CharField(max_length=255) #antivirus, office, etc
#     vendor = models.CharField(max_length=255) # microsoft, avast, etc
#     purchase_date = models.DateField()
#     expiriration_date = models.DateField(blank=True, null=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="license_customer")
#     notes = models.TextField(blank=True, null=True)
#     end_of_life = models.DateField(blank=True, null=True)
#     added_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="license_addedby", blank=True, null=True)

# class Equipment(models.Model):
#     id = models.AutoField(primary_key=True)
#     type = models.CharField(max_length=255) #antivirus, office, etc
#     vendor = models.CharField(max_length=255) # microsoft, avast, etc
#     model = models.CharField(max_length=255) # Vostro 1200, etc
#     purchase_date = models.DateField()
#     warranty_length = models.IntegerField()
#     warranty_end_date = models.DateField()
#     customer = models.ForeignKey(Customer, on_delete=CASCADE, related_name="customer_equipment")
#     user = models.ForeignKey(Contact, on_delete=SET_NULL, related_name="user_equipment", null=True)