from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auctions/add_listing", views.add_listings, name="add_listing"),
    path("auctions/<int:list_id>", views.display_listing, name="display_listing"),
    path("auctions/categories", views.categories, name="categories"),
    path("auctions/<str:category>", views.display_category, name="display_category"),
]
