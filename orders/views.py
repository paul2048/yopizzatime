from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.db.models import Sum

from .models import Pizza, Pasta, Salad, NotFood, Topping, CartItem
from .forms import LoginForm, RegisterForm

import re
from django.core.serializers import json

EMAIL_VALIDATOR = r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}"
NAME_VALIDATOR = r"^[A-Za-z ]+$"
PASSW_VALIDATOR = r"^(?=.*[A-Z])(?=(.*[!@#$&*])|(.*[0-9]))(?=.*[a-z]).{8,}$"


def index(request):
    """ Renders the main page """
    first_name = request.user.first_name

    context = {
        "forms": {
            "login": LoginForm(prefix="login"),
            "register": RegisterForm(prefix="register"),
        },
        "items": [
            ("pizza", Pizza.objects.all()),
            ("pasta", Pasta.objects.all()),
            ("salad", Salad.objects.all()),
            ("other", NotFood.objects.all())
        ],
        "is_authenticated": request.user.is_authenticated,
        "first_name": first_name,
    }

    return render(request, "orders/index.html", context)

def login(request):
    """ Logs the user in """
    email = request.POST.get("login-email")
    passw = request.POST.get("login-password")
    msg = {}
    
    # If the email doesn't exist
    if not User.objects.filter(email=email).exists():
        msg["login-email"] = "The email doesn't exist."
    # If no errors were found
    else:
        usern = User.objects.filter(email=email)[0].username # Get the username
        user = authenticate(request, username=usern, password=passw)

        # If the password doesn't match with the email
        if user is None:
            msg["login-password"] = "Invalid credentials."
        else:
            auth_login(request, user) # Log the user in

    # Returns a JSON like {input_name: error_message}
    return JsonResponse(msg)

def register(request):
    """ Registers the user """
    usern = request.POST.get("register-username")
    email = request.POST.get("register-email")
    fname = request.POST.get("register-first_name").title() # e.g converts "de alex" into "De Alex"
    lname = request.POST.get("register-last_name").title()
    passw = request.POST.get("register-password")
    confr = request.POST.get("register-confirm")
    msg = {}

    if len(usern) < 2: # If the USERNAME is too short
        msg["register-username"] = "The username is too short."
    elif "@" in usern: # If the USERNAME contains "@"
        msg["register-username"] = "The username can't contain \"@\" in it."
    elif User.objects.filter(username=usern)[0].exists(): # If the USERNAME already exists
        msg["register-username"] = "The username is already taken."
    elif not re.match(EMAIL_VALIDATOR, email, re.I): # If the EMAIL is invalid
        msg["register-email"] = "The email is invalid."
    elif User.objects.filter(email=email)[0].exists(): # If the EMAIL already exists
        msg["register-email"] = "The email is already taken."
    elif not re.match(NAME_VALIDATOR, fname): # If the FIRST NAME is not valid
        msg["register-first_name"] = "The first name is not valid."
    elif not re.match(NAME_VALIDATOR, lname): # If the LAST NAME is not valid
        msg["register-first_name"] = "The last name is not valid."
    elif not re.match(PASSW_VALIDATOR, passw): # If the PASSWORD is not secure
        msg["register-password"] = "Minimum requirements: 8 characters long; 1 uppercase and 1 lowercase letters; 1 digit or 1 symbol"
    elif confr != passw: # If the CONFIRMATION doesn't match with the PASSWORD
        msg["register-confirm"] = "The confirmation doesn't match with the password."
    else:
        # Creates the user and saves it in the db
        user = User.objects.create_user(username=usern, email=email, first_name=fname, last_name=lname, password=passw)

        # Just in case the user couldn't be created
        if user is None:
            msg["register-confirm"] = "Couldn't register."
        else:
            auth_login(request, user) # Logs the user in

    # Returns a JSON like {input_name: error_message}
    return JsonResponse(msg)

def logout_view(request):
    """ Logs the user out """
    logout(request)

    return HttpResponseRedirect(reverse("index"))

def cart_items(request):
    """ Returns the items in the user's shopping cart """
    # Gets all the items in the user's cart
    username = request.user.username
    items = CartItem.objects.filter(user__username=username)
    
    data = {
        "items": [],
        "total_price": items.aggregate(Sum("price"))["price__sum"]
    }
    
    # Converts the QuerySet into a dictionary
    for item in items:
        try:
            is_vegetarian = item.item.vegetarian
        except AttributeError:
            is_vegetarian = False

        data["items"].append({
            "id": item.id,
            "name": item.item.name,
            "is_vegetarian": is_vegetarian,
            "is_large": item.is_large,
            "price": item.price,
            "toppings": list(item.toppings.values())
        })

    return JsonResponse(data)

def item_price_addcart(request, action):
    """ Returns the price of the item. It also adds item the the shopping cart if the user specified that in "action" """
    args = request.POST
    item_name = request.POST.get("item-name")
    item_size = request.POST.get("item-size")
    is_large = item_size == "L"

    # Calculates the price for the selected toppings
    topping_names = [key for key in args if args[key] == "on" and key != "item-name"]
    toppings = Topping.objects.filter(name__in=topping_names)
    toppings_price = sum([float(topping.price) for topping in toppings])
    
    models = (Pizza, Pasta, Salad, NotFood) # Tuple of possible models

    # Finds the model of the item that is wanted in the cart
    for model in models:
        try:
            item = model.objects.get(name=item_name)
            base_price = float(model.objects.get(name=item_name).price)
        except:
            continue

    price = base_price * (1.3 if is_large else 1) + toppings_price # The total item price

    # If the user clicked on ".add_to_cart_btn"
    if action == "add_to_cart":
        user = User.objects.get(username=request.user.username)
        cart_item = CartItem.objects.create(user=user, item=item, is_large=is_large, price=price)
        cart_item.toppings.set(toppings)

    return JsonResponse({"price": price})

def remove_from_cart(request, id):
    """ Removes a item from the user's shopping cart and returnes the new total price for the cart """
    CartItem.objects.filter(id=id).delete() # Removes the item from the cart
    
    # Gets the new total price of the user's cart
    username = request.user.username
    user = User.objects.get(username=username)
    price = CartItem.objects.filter(user__username=username).aggregate(Sum("price"))["price__sum"]

    return JsonResponse({"new_total_price": price})

def place_order(request):
    """ Places a order on the items in the shopping cart """

    return JsonResponse({})