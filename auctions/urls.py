from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("new_bid/<int:listing_id>", views.new_bid, name="new_bid"),
    path("close_bid/<int:listing_id>", views.close_bid, name="close_bid"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("new_comment/<int:listing_id>", views.new_comment, name="new_comment"),
    path("all_categories", views.all_categories, name="all_categories"),
    path("category_branch/<str:category_id>", views.category_branch, name="category_branch")
]
