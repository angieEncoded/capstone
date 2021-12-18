from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("add_customer", views.add_customer, name="add_customer"),
    path("all_customers", views.all_customers, name="all_customers"),
    path("view_customer/<int:id>", views.view_customer, name="view_customer"),
    path("edit_customer/<int:id>/<str:fieldName>", views.edit_customer, name="edit_customer"),
    path("add_contact", views.add_contact, name="add_contact"),
    path("get_customer_contacts/<int:id>", views.get_customer_contacts, name="get_customer_contacts"),
    # path("all_customers", views.all_customers, name="all_customers"),
    # path("listing/<int:id>", views.listing, name="listing"),
    # path("watchlist/<int:id>", views.watchlist, name="watchlist"),
    # path("listing/<int:id>/bid", views.bid, name="bid"),
    # path("listing/<int:id>/end_auction", views.end_auction, name="end_auction"),
    # path("listing/<int:id>/add_comment", views.add_comment, name="add_comment"),
    # path("mywatcheditems/<int:id>", views.mywatcheditems, name="mywatcheditems"),
    # path("categories", views.categories, name="categories"),
    # path("category_listings/<int:id>", views.category_listings, name="category_listings"),
    # path("won_auctions/<int:id>", views.won_auctions, name="won_auctions"),
    # path("my_listings/<int:id>", views.my_listings, name="my_listings"),
]