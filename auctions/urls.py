from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("category/", views.category_list, name="category_list"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category/<slug:category_slug>", views.category, name="category"),
    path("product/<slug:product_slug>", views.product, name="product"),
    path("product/<slug:product_slug>/bid", views.bid, name="bid"),
    path("product/<slug:product_slug>/comment", views.comment, name="comment"),
     


]
