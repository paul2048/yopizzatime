from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Item(models.Model):
    name = models.CharField(max_length=64, default="", unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True # "Item" will not be used to create any db table

class Food(Item):
    ingredients = models.CharField(max_length=128, default="")
    has_large = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}: {self.ingredients} ({self.timestamp})"

class NotFood(Item):
    class Meta:
        ordering = ["name"] # Order the "Item" objects by name

    def __str__(self):
        return f"{self.name}: ${self.price} ({self.timestamp})"

class Topping(Item):
    def __str__(self):
        return f"{self.name}: ${self.price} ({self.timestamp})"

class Pizza(Food):
    toppings = models.ManyToManyField(Topping)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}: ${self.price} - {self.toppings} ({self.timestamp})"

class Pasta(Food):
    vegetarian = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}: ${self.price} - {self.ingredients} ({self.timestamp})"

class Salad(Food):
    vegetarian = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}: ${self.price} - {self.ingredients} ({self.timestamp})"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Enables to point to multiple models, like Salad, Pizza, NotFood, etc.
    limit = models.Q(app_label="orders", model="pizza") | models.Q(app_label="orders", model="pasta") | models.Q(app_label="orders", model="salad") | models.Q(app_label="orders", model="notfood")
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    is_large = models.BooleanField(default=False)
    toppings = models.ManyToManyField(Topping)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        large = "(L)" if self.is_large else ""
        full_name = f"{self.user.first_name} {self.user.last_name}"
        toppings = [topping.name for topping in self.toppings.all()]

        return f"{self.item.name} (+{toppings}) {large} for {full_name} - ${self.price} ({self.timestamp})"