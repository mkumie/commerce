from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auctions/add_listing", views.add_listing, name="add_listing"),
    path("auctions/<int:list_id>", views.display_listing, name="display_listing"),
    path("auctions/categories", views.categories, name="categories"),
    path("auctions/<str:category>", views.display_category, name="display_category"),
    path("auctions/<int:listing_id>/", views.watchlist_add, name="watchlist_add"),
    path("auctions/<str:user>/watchlist", views.watchlist, name="watchlist"),
    path("auctions/<int:listing_id>/delete_watchlist", views.delete_watchlist, name="delete_watchlist"),
    path("auctions/<int:listing_id>/bid", views.bid, name="bid"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
