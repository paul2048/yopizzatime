# Yo Pizza Time
Yo Pizza Time is a made-up restaurant with a food delivery service, that makes pizza, pasta and salads. Pizzas can be made either in normal size or in a big size and all of them can have extra toppings. Add your desired meals to the shopping cart and place an imaginary order!

## orders/migrations/
The folder contains python files, each representing a migration.
## orders/templates/orders/layout.html
This is the layout of the `index.html` template. It containes the `<head>` inside which the links with the static files and the favicon are found.
## orders/templates/orders/index.html
This is the main page.
## orders/admin.py
This python file is used for modifying the admin interface. The tables of the `Pizza`, `Pasta`, `Salad`, `NotFood`, `Topping` and `CartItem` models are displayed in the admin interface. To add new type of food, import the model of the type of the food and add `admin.site.register(FoodType)`.
## orders/apps.py
This file is used for managing the apps used for this project. To create a new app, create a new class to. You can configure each app.
## orders/forms.py
This file is used to create classes that can be used in html files and translated into html forms (use: `{{ ClassName }}`). It contains the `LoginForm` and `RegisterForm` classes.
## orders/models.py
`models.py` has the classes that base on them, database tables will be created with the specified fields. You can choose not to create a table with
```python
class Meta:
    abstract = True
```
inside the desired class.
## orders/tests.py
This file has the purpose to use the `TestCase` class (that uses the `unittest` library) store classes that include test cases for validating the app's functionality before pushing the changes to the origin. No test case is used in this project because I can't successfuly run `python3 manage.py test` :(. 
## orders/urls.py
`urls.py` containes the paths the regular users and the superusers can access. One of the paths is "/place_order"
## orders/views.py
The `views.py` Python file includes all the functionality of the paths, like logging users in (the "login" function) or adding items to the cart (the "item_price_addcart" function).
## pizza/settings.py
This file has the general settings of the project, for example the databese set-up (the `DATABASES` dictionary) and the path to the static folder (the `STATIC_URL` variable).
## pizza/urls.py
`urls.py` containes the paths the superusers can access. One of the paths is "/admin"
## pizza/wsgi.py
This file is the WSGI config for the project. It exposes the WSGI callable as a module-level variable named "application".
## static/css/bootstrap.min.css
[Bootstrap 4](https://getbootstrap.com/) - CSS framework
## static/css/style.css
This is the styling of the `index.html` template. It's the CSS file from the compilation of `style.scss`.
## static/css/style.scss
[Sass](https://sass-lang.com/) - Style sheet language
This is the file where the styling of the app is written.
## static/js/bootstrap.min.js
[Bootstrap 4](https://getbootstrap.com/) - JavaScript framework
## static/js/handlebars-v4.4.3.js
[Handlebars](https://handlebarsjs.com/) - JavaScript templating
## static/js/jquery-v3.4.1.js
[JQuery](https://jquery.com/) - JavaScript framework
## static/js/script.js
`scripts.js` contains the general JavaScript code. It's not vanilla JS since JQuery, Bootstrap and Handlebars are used. It includes the code that marks the wrong fields of the login and register forms, event listeners for forms, buttons etc. and more.
## manage.py
This file accomplishes 2 things:
- It puts the project's package on sys.path.
- It sets the `DJANGO_SETTINGS_MODULE` environment variable so that it points to your project’s settings file (pizza/settings.py).
Also, to run the web app, you can execute `python3 manage.py runserver`.
## requirements.txt
This is a text file that contains a list with the packages required to develop this web app.
Run `pip3 install requirements.txt` or `pip install requirements.txt` to install the required packages.
