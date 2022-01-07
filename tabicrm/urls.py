from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),

    # Login and logout
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path("add_customer", views.add_customer, name="add_customer"),
    path("all_customers", views.all_customers, name="all_customers"),
    path("view_customer/<int:customerId>", views.view_customer, name="view_customer"),
    path("edit_customer/<int:customerId>/<str:fieldName>", views.edit_customer, name="edit_customer"),

    # customer contacts
    path("add_contact/<int:customerId>", views.add_contact, name="add_contact"),
    path("get_customer_contacts/<int:customerId>", views.get_customer_contacts, name="get_customer_contacts"),
    path("get_contact/<int:contactId>", views.get_contact, name="get_contact"),
    path("edit_contact/<int:contactId>/<str:fieldName>", views.edit_contact, name="edit_contact"),

    # customer equipment
    path("get_customer_equipment/<int:customerId>", views.get_customer_equipment, name="get_customer_equipment"),

    # customer tickets
    path("post_new_ticket/<int:customerId>", views.post_new_ticket, name="post_new_ticket"),

    # customer licenses
    path("add_license/<int:customerId>", views.add_license, name="add_license"),
    path("get_customer_licenses/<int:customerId>", views.get_customer_licenses, name="get_customer_licenses"),


    path("download_license/<int:licenseId>", views.download_license, name="download_license"),
    path("get_license/<int:licenseId>", views.get_license, name="get_license"),
    path("delete_license/<int:licenseId>", views.delete_license, name="delete_license"),

    # Full form management section
    path("customer_full_form/<int:customerId>", views.customer_full_form, name="customer_full_form"),
    path("delete_customer/<int:customerId>", views.delete_customer, name="delete_customer"),
    path("add_equipment/<int:customerId>", views.add_equipment, name="add_equipment"),
    path("add_ticket/<int:customerId>", views.add_ticket, name="add_ticket"),

    # Display paths here
    path("display_contacts/<int:customerId>", views.display_contacts, name="display_contacts"),
    path("display_equipment/<int:customerId>", views.display_equipment, name="display_equipment"),
    path("display_tickets/<int:customerId>", views.display_tickets, name="display_tickets"),
    path("display_licenses/<int:customerId>", views.display_licenses, name="display_licenses"),

    # Edit paths below here
    path("full_edit_contact/<int:contactId>", views.full_edit_contact, name="full_edit_contact"),
    path("full_edit_equipment/<int:equipmentId>", views.full_edit_equipment, name="full_edit_equipment"),
    path("full_edit_ticket/<int:ticketId>", views.full_edit_ticket, name="full_edit_ticket"),
    path("full_edit_license/<int:licenseId>", views.full_edit_license, name="full_edit_license"),


    # full delete paths below here
    path("delete_contact/<int:contactId>", views.delete_contact, name="delete_contact"),
    path("delete_equipment/<int:equipmentId>", views.delete_equipment, name="delete_equipment"),

    # 
    path("view_single_ticket/<int:ticketId>", views.view_single_ticket, name="view_single_ticket"),
    path("add_ticket_comment/<int:ticketId>", views.add_ticket_comment, name="add_ticket_comment"),
    path("ticket_actions/<int:ticketId>", views.ticket_actions, name="ticket_actions"),


]