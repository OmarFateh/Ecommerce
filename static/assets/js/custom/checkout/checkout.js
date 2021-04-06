// Create an instance of the Stripe object with your publishable API key
var stripe = Stripe(stripePublicKey);
var elem = document.getElementById("place-order");

var elements = stripe.elements();
var style = {
    base: {
        color: "#000",
        fontSize: "16px",
    }
};
var card = elements.create("card", { style:style });
card.mount("#card-element");

// display card errors
card.on('change', function(e) {
    var displayError = document.getElementById("card-errors");
    if ( e.error ) {
        displayError.textContent = e.error.message;
        $("#card-errors").addClass('alert alert-info');
    }
    else {
        displayError.textContent = '';
        $("#card-errors").removeClass('alert alert-info');
    }

});

// Delivery options
$(document).on("change", 'input[name=radio1]', function (e) {
    $.ajax({
        url: $("#delivery-options").data("url"),
        type: 'POST',
        data: {  
            delivery_option: $("input[name=radio1]:checked").val(), 
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        },
        success: function (data) {
            document.getElementById('shipping-price').innerHTML = `$${data.delivery_price}`
            document.getElementById('total-price').innerHTML = `$${data.total_price}`
        },
    }) 
})

// submit card form stripe integration
var form = document.getElementById("checkout-form");

form.addEventListener('submit', function(e) {
    e.preventDefault();
    var custAdd = document.getElementById("id_address1").value;
    var custName = document.getElementById("id_full_name").value;
    var deliveryOption = $("input[name=radio1]:checked").val();

    $.ajax({
        url: CheckoutUrl,
        type: 'POST',
        data: $(form).serialize() + "&delivery_option="+ deliveryOption, 
        success: function (data) {
            if (data.form_is_valid) {
                stripe.confirmCardPayment(data.client_secret, {
                    payment_method: {
                        card: card,
                        billing_details: {
                            address: custAdd,
                            name: custName,
                        },
                    }
                }).then(function(result){
                    if ( result.error ) {
                        console.log(result.error.message);
                    }
                    else if ( result.paymentIntent.status === "succeeded" ) {
                        window.location.replace(OrderPlacedUrl);
                    }
                })
            }
        },
    }) 
});