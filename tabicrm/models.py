from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import related
from django.db.utils import NotSupportedError
from django.utils import timezone # https://stackoverflow.com/questions/65157917/django-core-exceptions-fielderror-date-cannot-be-specified-for-forum-model-fo
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

# https://docs.djangoproject.com/en/4.0/ref/models/fields/

class License(models.Model):

    # Fields for the choices in the drop down
    AVAST_PRO = 'AVAST PRO'
    AVAST_ENDPOINT = 'AVAST ENDPOINT'
    MALWAREBYTES = 'MALWAREBYTES'
    MICROSOFT_OFFICE_2010 = 'MICROSOFT OFFICE 2010'
    MICROSOFT_OFFICE_2013 = 'MICROSOFT OFFICE 2013'
    MICROSOFT_OFFICE_2016 = 'MICROSOFT OFFICE 2016'
    MICROSOFT_OFFICE_2019 = 'MICROSOFT OFFICE 2019'
    MICROSOFT_OFFICE_365 = 'MICROSOFT OFFICE 365'

    PRODUCT_CHOICES = [
        (AVAST_PRO, 'AVAST PRO'),
        (AVAST_ENDPOINT , 'AVAST ENDPOINT'),
        ( MALWAREBYTES, 'MALWAREBYTES'),
        ( MICROSOFT_OFFICE_2010,'MICROSOFT OFFICE 2010' ),
        ( MICROSOFT_OFFICE_2013,'MICROSOFT OFFICE 2013' ),
        (MICROSOFT_OFFICE_2016 , 'MICROSOFT OFFICE 2016'),
        ( MICROSOFT_OFFICE_2019, 'MICROSOFT OFFICE 2019'),
        ( MICROSOFT_OFFICE_365, 'MICROSOFT OFFICE 365'),
    ]

    id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=255, choices=PRODUCT_CHOICES, default=AVAST_PRO) # microsoft, avast, etc
    purchase_date = models.DateField(default=timezone.now)
    expiration_date = models.DateField(blank=True, null=True, )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="license_customer")
    license_key = models.CharField(max_length=255,blank=True, null=True)
    license_file = models.FileField(upload_to='licenses/%m_%d_%Y', blank=True)
    notes = models.TextField(blank=True, null=True)
    end_of_life = models.DateField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="license_addedby", blank=True, null=True)

    def __str__(this):
        return f"{this.product} {this.customer}"

class Equipment(models.Model):


    # Fields for equipment type
    SERVER = 'SERVER'
    ROUTER = 'ROUTER'
    SWITCH = 'SWITCH'
    MODEM = 'MODEM'
    DESKTOP = 'DESKTOP'
    LAPTOP = 'LAPTOP'
    IP_PHONE = 'IP_PHONE'
    TABLET = 'TABLET'
    CELL_PHONE = 'CELL_PHONE'

    TYPE_CHOICES = [
        (SERVER,'SERVER'),
        (ROUTER,'ROUTER'),
        (SWITCH,'SWITCH'),
        (MODEM,'MODEM'),
        (DESKTOP,'DESKTOP'),
        (LAPTOP,'LAPTOP'),
        (IP_PHONE,'IP_PHONE'),
        (TABLET,'TABLET'),
        (CELL_PHONE,'CELL_PHONE')
    ]



    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, default=SERVER)
    vendor = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    purchase_date = models.DateField()
    warranty_end_date = models.DateField()
    internal_ip_address = models.CharField(max_length=255, blank=True, null=True)
    external_ip_address = models.CharField(max_length=255, blank=True, null=True)
    subnet_mask = models.CharField(max_length=255, blank=True, null=True)
    default_gateway = models.CharField(max_length=255, blank=True, null=True)

    customer = models.ForeignKey(Customer, on_delete=CASCADE, related_name="customer_equipment")
    notes = models.TextField(blank=True, null=True)

