window.onload = () => {
    $("body").fadeIn();

    const login_form = $("#login_form");
    const register_form = $("#register_form");
    const cart_modal_body = $("#shoping_cart_modal .modal-body");

    // Handlebars equality checker helper
    Handlebars.registerHelper('is', (arg1, arg2, options) => {
        return (arg1 == arg2) ? options.fn(this) : options.inverse(this);
    });

    const cart_items_tem = Handlebars.compile(`
        {{#if items}}
            {{#each items}}
                <div class="row cart_item">
                    <div class="col-8">
                        <div class="item_name">
                            <b>{{name}}</b>
                            {{#if is_vegetarian}}(<span class="text-success small">V</span>){{/if}}
                            {{#if is_large}}(L){{/if}}
                        </div>
                        
                        {{#if toppings}}
                            <div>
                                <span>Toppings</span>:

                                {{#each toppings}}
                                    <span class="text-primary">{{name}}</span>{{#is @last false}},{{/is}}
                                {{/each}}
                            </div>
                        {{else}}
                            <div>➖</div>
                        {{/if}}
                    </div>

                    <div class="col-4 text-right m-auto">
                        \${{price}}
                        <button class="btn btn-danger ml-2 cart_btn remove_from_cart_btn" data-cart_item_id="{{id}}">⨯</button>
                    </div>
                </div>
            {{/each}}

            <div class="text-center">
                Total Price: <span id="total_cart_price">\${{total_price}}</span>
            </div>
        {{else}}
            Your shopping cart is empty.
        {{/if}}
    `); 

    $("#log_reg_modal").on("show.bs.modal", (e) => {
        const btn_txt = $(e.relatedTarget).text(); // Gets the inner text of the clicked button

        // Hides both forms
        login_form.css("display", "none");
        register_form.css("display", "none");

        // Displays the desired form of the modal
        if (btn_txt == "Log In") {
            login_form.css("display", "block");
        }
        else {
            register_form.css("display", "block");
        }
    });

    // When the login or register form is submitted
    $("#login_form, #register_form").submit((e) => {
        e.preventDefault();
        
        show_inp_err($(e.target));
    });

    // When the cart button in the navbar is clicked
    $("#show_cart_items").click(() => {
        cart_modal_body.empty(); // Empty the modal body
        cart_modal_body.html(`<div class="text-center" id="loading-screen">🍕</div>`);

        $.getJSON("/cart_items", (response) => {
            const items = response.items;
            const total_price = response.total_price;
            
            // Appends every cart item of the user in the modal's body
            cart_modal_body.html(
                cart_items_tem({"items": items, "total_price": total_price})
            );

            // When the red "⨯" button is clicked
            $(".remove_from_cart_btn").click((e) => {
                e.preventDefault();

                // The cart item id of the database
                const cart_item_id = $(e.target).data("cart_item_id");

                // Make a request to remove the item from the cart
                $.getJSON(`/remove_from_cart/${cart_item_id}`, (response) => {
                    const new_total_price = response.new_total_price;
                    const cart_item = $(e.target).closest(".cart_item");

                    cart_item.fadeOut(300, () => {
                        cart_item.remove(); // Removes the item in the cart
                    });

                    // Updates the total price
                    $("#total_cart_price").html(`$${new_total_price}`);
                });
            });
        });
    });

    $("#place_order_form").submit((e) => {
        e.preventDefault();
        
        const form = $(e.target);

        $.post("/place_order", form.serialize(), (response) => {
            console.log(response) //////////////
            
            cart_modal_body.find("*").fadeOut(300, () => {
                cart_modal_body.html(`
                    <div class="text-center" id="order_placed">
                        <p class="text-primary bounce_in">Order Placed!</p>
                        <!--Credits: https://www.flaticon.com/free-icon/check_811868?term=check%20mark&page=1&position=40-->
                        <img class="fade_in_up" src="/static/images/checkmark.svg">
                    </div>
                `);
            });
        });
    });

    // When the the topping or size of the pizza changes
    $(".pizza_toppings input, select[name='item-size']").change((e) => {
        // Stores the form in which a change was made
        const form = $(e.target).closest($(".add_to_cart_form"));
        
        // Request the new price from the server
        $.post("/item_price_addcart/get_price", form.serialize(), (response) => {
            const price = response.price; // The calculated price from the server

            form.find(".item_price").html(`$${price.toFixed(2)}`); // Replaces the old price
        });
    });

    // When the shopping cart button next to each item is clicked
    $(".add_to_cart_form").submit((e) => {
        e.preventDefault(); // Prevents the form from reloading

        const form = $(e.target); // Stores the form in which a change was made
        const submit_btn = form.find($(".add_to_cart_btn")); // Stores the submit button

        submit_btn.prop("disabled", true); // Disables the submit button
        
        // Request for adding the item in the cart
        $.post("/item_price_addcart/add_to_cart", form.serialize(), () => {
            // Enables the submit button after the item was added to the cart
            submit_btn.prop("disabled", false);
        });
    });
};

// Takes a input element as argument, then indicates the flawed input and shows an errory message
const show_inp_err = (form) => {
    const form_name = form.attr("id").split("_")[0]; // "register" for instance
    const request_to = `/${form_name}`; // A string with the route to make the request to (e.g "/login")
    
    $.post(request_to, form.serialize(), (error_msg_obj) => {
        // If the input is valid
        if ($.isEmptyObject(error_msg_obj)) {
            reset_form_fields(form);

            location.pathname = "/";
        }
        else {
            const inp_name = Object.keys(error_msg_obj)[0]; // "register-confirm", "login-email", etc
            const inp = form.find($(`input[name="${inp_name}"]`));
            const label = inp.closest(".form-group").children("label");

            reset_form_fields(form);

            // Indicate the wrong input field
            label.html(`${inp.data("label")} - ${error_msg_obj[inp_name]}`);
            label.css("color", "red");
            inp.css("border-color", "red");
        }
    });
};

// Apply default styling to the input fields of a form and removes the error messages in the labels
const reset_form_fields = (form) => {
    // Iterates through all the input fields of the form
    form.find("input").each((i, inp) => {
        inp = $(inp); // Convert the input element in a jQuery object

        // The label of the input
        const label = inp.closest(".form-group").children("label");

        // Resets the input and label
        label.html(inp.data("label"));
        label.css("color", "");
        inp.css("border-color", "");
    });
};