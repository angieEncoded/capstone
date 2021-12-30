from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    # path("views/", views.views_view, name="views"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path("add_customer", views.add_customer, name="add_customer"),
    path("all_customers", views.all_customers, name="all_customers"),
    path("view_customer/<int:id>", views.view_customer, name="view_customer"),
    path("edit_customer/<int:id>/<str:fieldName>", views.edit_customer, name="edit_customer"),

    path("add_contact/<int:id>", views.add_contact, name="add_contact"),
    path("get_customer_contacts/<int:id>", views.get_customer_contacts, name="get_customer_contacts"),
    path("get_contact/<int:id>", views.get_contact, name="get_contact"),
    path("edit_contact/<int:id>/<str:fieldName>", views.edit_contact, name="edit_contact"),

    path("add_license/<int:id>", views.add_license, name="add_license"),
    path("get_customer_licenses/<int:id>", views.get_customer_licenses, name="get_customer_licenses"),
    path("download_license/<int:id>", views.download_license, name="download_license"),
    path("get_license/<int:id>", views.get_license, name="get_license"),
    path("edit_license/<int:id>", views.edit_license, name="edit_license"),
    path("delete_license/<int:id>", views.delete_license, name="delete_license"),

    path("customer_full_form/<int:id>", views.customer_full_form, name="customer_full_form"),
    path("delete_customer/<int:id>", views.delete_customer, name="delete_customer"),

    path("add_equipment/<int:id>", views.add_equipment, name="add_equipment"),
    path("add_ticket/<int:id>", views.add_ticket, name="add_ticket"),

    # Display paths here
    path("display_contacts/<int:id>", views.display_contacts, name="display_contacts"),
    path("display_equipment/<int:id>", views.display_equipment, name="display_equipment"),
    path("display_tickets/<int:id>", views.display_tickets, name="display_tickets"),

    # Edit paths below here
    path("full_edit_contact/<int:contactId>", views.full_edit_contact, name="full_edit_contact"),
    path("full_edit_equipment/<int:equipmentId>", views.full_edit_equipment, name="full_edit_equipment"),
    path("full_edit_ticket/<int:ticketId>", views.full_edit_ticket, name="full_edit_ticket"),

    # full delete paths below here
    path("delete_contact/<int:contactId>", views.delete_contact, name="delete_contact"),
    path("delete_equipment/<int:equipmentId>", views.delete_equipment, name="delete_equipment"),

    path("view_single_ticket/<int:ticketId>", views.view_single_ticket, name="view_single_ticket"),
    path("add_ticket_comment/<int:ticketId>", views.add_ticket_comment, name="add_ticket_comment"),
    path("ticket_actions/<int:ticketId>/<str:action>", views.ticket_actions, name="ticket_actions"),


]