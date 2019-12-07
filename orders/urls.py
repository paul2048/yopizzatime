from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout_view", views.logout_view, name="logout_view"),
    path("cart_items", views.cart_items, name="cart_items"),
    path("item_price_addcart/<str:action>", views.item_price_addcart, name="item_price_addcart"),
    path("remove_from_cart/<int:id>", views.remove_from_cart, name="remove_from_cart"),
    path("place_order", views.place_order, name="place_order")
]