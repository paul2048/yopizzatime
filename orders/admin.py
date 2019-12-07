from django.contrib import admin
from .models import Pizza, Pasta, Salad, NotFood, Topping, CartItem

admin.site.register(Pizza)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(NotFood)
admin.site.register(Topping)
admin.site.register(CartItem)