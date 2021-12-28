from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import related
from django.db.utils import NotSupportedError
from django.utils import timezone # https://stackoverflow.com/questions/65157917/django-core-exceptions-fielderror-date-cannot-be-specified-for-forum-model-fo
# REMEMBER - IF YOU DECIDE TO RENAME THE APP AGAIN AND MESS WITH THE MIGRATIONS YOU HAVE TO DO THIS
# https://stackoverflow.com/questions/36153748/django-makemigrations-no-changes-detected
# https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html


# helper function to add three years to a date - https://stackoverflow.com/questions/27491248/django-default-timezone-now-delta/27491426
def default_three_year():
    return timezone.now() + timezone.timedelta(days=1095)



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

    # ADDITIONAL details
    added_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="customer_addedby", blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="customer_updatedon", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="contact_customer")
    # Additional details
    added_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="contact_addedby", blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="contact_updatedon", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(this):
        return f"{this.first_name} {this.last_name}"

# https://docs.djangoproject.com/en/4.0/ref/models/fields/



class License(models.Model):

    # Fields for the choices in the drop down
    AVAST_PRO = 'Avast Pro'
    AVAST_ENDPOINT = 'Avast Endpoint Protection'
    MALWAREBYTES = 'Malwarebytes'
    MICROSOFT_OFFICE_2010 = 'Microsoft Office 2010'
    MICROSOFT_OFFICE_2013 = 'Microsoft Office 2013'
    MICROSOFT_OFFICE_2016 = 'Microsoft Office 2016'
    MICROSOFT_OFFICE_2019 = 'Microsoft Office 2019'
    MICROSOFT_OFFICE_365 = 'Microsoft Office 365'

    PRODUCT_CHOICES = [
        (AVAST_PRO, 'Avast Pro'),
        (AVAST_ENDPOINT , 'Avast Endpoint Protection'),
        ( MALWAREBYTES, 'Malwarebytes'),
        ( MICROSOFT_OFFICE_2010,'Microsoft Office 2010' ),
        ( MICROSOFT_OFFICE_2013,'Microsoft Office 2013' ),
        (MICROSOFT_OFFICE_2016 , 'Microsoft Office 2016'),
        ( MICROSOFT_OFFICE_2019, 'Microsoft Office 2019'),
        ( MICROSOFT_OFFICE_365, 'Microsoft Office 365'),
    ]

    id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=255, choices=PRODUCT_CHOICES, default=AVAST_PRO) # microsoft, avast, etc
    purchase_date = models.DateField(default=timezone.now)
    expiration_date = models.DateField(blank=True, null=True, default=default_three_year)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="license_customer")
    license_key = models.CharField(max_length=255,blank=True, null=True)
    license_file = models.FileField(upload_to='licenses/%m_%d_%Y', blank=True, default=None)
    notes = models.TextField(blank=True, null=True)
    end_of_life = models.DateField(blank=True, null=True, default=default_three_year)
    # Additional Details
    added_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="license_addedby", blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="license_updatedon", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)



    def __str__(this):
        return f"{this.product} {this.customer}"

class Equipment(models.Model):

    # Fields for equipment type
    SERVER = 'Server'
    ILO = 'ILO'
    UPS = 'UPS'
    ROUTER = 'Router'
    SWITCH = 'Switch'
    WAP = 'WAP'
    MODEM = 'Modem'
    DESKTOP = 'Desktop'
    LAPTOP = 'Laptop'
    PRINTER = 'Printer'
    IP_PHONE = 'IP Phone'
    RECEIPTER = 'Receipter'
    PRINT_SERVER = 'Print Server'
    TABLET = 'Tablet'
    CELL_PHONE = 'Cell Phont'
    OTHER = 'Other'

    TYPE_CHOICES = [
        (SERVER,'Server'),
        (ILO, 'ILO (or equivalent)'),
        (UPS, 'UPS'),
        (ROUTER,'Router'),
        (SWITCH,'Switch'),
        (WAP, 'Wireless Access Point'),
        (MODEM,'Modem'),
        (DESKTOP,'Desktop'),
        (LAPTOP,'Laptop'),
        (PRINTER, 'Printer'),
        (IP_PHONE,'IP Phone'),
        (RECEIPTER,'Receipter'),
        (PRINT_SERVER, 'Print Server'),
        (TABLET,'Tablet'),
        (CELL_PHONE,'Cell phone'),
        (OTHER, 'Other')
    ]

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=CASCADE, related_name="customer_equipment")
    type =  models.CharField(max_length=255, choices=TYPE_CHOICES, default=SERVER)
    vendor = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    os_version = models.CharField(max_length=255, blank=True, null=True)
    purchase_date = models.DateField(default=timezone.now)
    warranty_end_date = models.DateField(default=default_three_year)
    end_of_life = models.DateField(default=default_three_year)
    internal_ip_address = models.CharField(max_length=255, blank=True, null=True)
    external_ip_address = models.CharField(max_length=255, blank=True, null=True)
    subnet_mask = models.CharField(max_length=255, blank=True, null=True)
    default_gateway = models.CharField(max_length=255, blank=True, null=True)
    primary_dns = models.CharField(max_length=255, blank=True, null=True)
    secondary_dns = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    product_number = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    added_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="equipment_addedby", blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="equipment_updatedon", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(this):
        return f"{this.type} {this.vendor} {this.model} {this.customer}"

class Ticket(models.Model):

    OPEN='OPEN'
    IN_PROGRESS='In Progres'
    WAITING_ON_CUSTOMER = 'Waiting on customer'
    CLOSED = 'Closed'
    LOW = 'Low'
    NORMAL = 'Normal'
    HIGH = 'High'
    URGENT = 'Urgent'
    SOLVED_ON_PHONE = 'Solved on Phone'
    SERVER_SERVICE = 'Server service'
    ROUTER_SERVICE = 'Router service'
    CONTRACT_SERVICE = 'Contract service'
    NON_CONTRACT_SERVICE = 'Non-contract service'
    NETWORK_SUPPORT_TEAM = "NETWORK"
    SOFTWARE_SUPPORT_TEAM = "SOFTWARE"
    SERVER_SUPPORT_TEAM = "SERVER"
    HARDWARE_SUPPORT_TEAM = "HARDWARE"
    SALES_TEAM = "SALES"
    DEVELOPMENT_TEAM = "DEVELOPMENT"


    STATUS_CHOICES = [
        (OPEN, 'OPEN'),
        (IN_PROGRESS, 'IN PROGRESS'),
        (WAITING_ON_CUSTOMER, 'WAITING ON CUSTOMER'),
        (CLOSED, 'CLOSED')
    ]

    PRIORITY_CHOICES = [
        (LOW, 'LOW'),
        (NORMAL, 'NORMAL'),
        (HIGH, 'HIGH'),
        (URGENT, 'URGENT')
    ]

    # The display portion is handled here
    RESULTS_CHOICES = [
        (SOLVED_ON_PHONE, 'Solved on phone'),
        (SERVER_SERVICE, 'Server service'),
        (ROUTER_SERVICE, 'Router service'),
        (CONTRACT_SERVICE, 'Contract service'),
        (NON_CONTRACT_SERVICE, 'Non-contract service')
    ]

    TEAM_CHOICES = [
        (NETWORK_SUPPORT_TEAM, "Network Support"),
        (SOFTWARE_SUPPORT_TEAM, "Software Support"),
        (SERVER_SUPPORT_TEAM, "Server Support"),
        (HARDWARE_SUPPORT_TEAM, "Hardware Support"),
        (SALES_TEAM, "Sales"),
        (DEVELOPMENT_TEAM, "Development")
    ]

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=CASCADE, related_name="customer_ticket")
    assigned_to = models.CharField(max_length=255, choices=TEAM_CHOICES, default=SOFTWARE_SUPPORT_TEAM)
    owned_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="ticket_ownedby", blank=True, null=True)
    title = models.CharField(max_length=255)
    status =  models.CharField(max_length=255, choices=STATUS_CHOICES, default=OPEN)
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES, default=NORMAL)
    results = models.CharField(max_length=255, choices=RESULTS_CHOICES, default=SOLVED_ON_PHONE)
    description = models.TextField(blank=True, null=True)
    solution = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="ticket_addedby", blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="ticket_updatedon", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(this):
        return f"{this.title} {this.assigned_to}"


class TicketComment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField(blank=True, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=CASCADE, related_name="ticket_comment", blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="ticket_comment_addedby", blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="ticket_comment_updatedon", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class TicketHistory(models.Model):
    id = models.AutoField(primary_key=True)    
    action =  models.TextField(blank=True, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=CASCADE, related_name="ticket_history", blank=True, null=True)
    taken_by = models.ForeignKey(User, on_delete=SET_NULL, related_name="ticket_action_taken_by", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)