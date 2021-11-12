from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_auctions, name="create"),
    path("lists/<int:id>", views.list_auction, name="lists"),
    path("toggle/<int:id>", views.toggle, name="toggle"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("final/<int:id>", views.final, name="final"),
    path("winned", views.winned_auctions, name="winned"),
    path("category", views.catagory, name="category"),
    path("lists<str:category>", views.cat_lists, name="cat_lists")
]
