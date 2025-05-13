/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';        
    }
});

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    // when the user clicks the submit button the event listener prevents the form from submitting ...
    ev.preventDefault();
    // ... and instead disables the card element ...
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    /// ... and triggers the loading overlay
    $('#loading-overlay').fadeToggle(100);

    // variables to capture the form data we can't put in the payment intent here ...
    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    var url = '/checkout/cache_checkout_data/';

    // ... and instead post it to the cache_checkout_data view, views.py ...
    //
    // Posting to the URL and that we want to post the post data above
    // to wait for a response that the payment intent was updated before 
    // calling the confirmed payment method
    $.post(url, postData).done(function () {
        // ... call the confirm card payment method from stripe ...
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                // since the payment intent .succeeded webhook will be coming from stripe 
                // and not from our own code into the webhook handler, we need to somehow 
                // stuff the form data into the payment intent object so we can retrieve 
                // it once we receive the webhook, to not get lost in transfer
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address:{
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            },
        }).then(function(result) {
            // ... if there's an error in the form then the loading overlay will be hidden
            // the card element re-enabled and the error displayed for the user
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    // ... if everything is ok with all stripe process submit the form
                    // comment out the form submission, checkout view will fail, simulates the form not
                    // to be submitted, and raise the error, 'handle only in webhook', webhook handler
                    // will catch the payment intent succeeded webhook from stripe and handle everything
                    form.submit();
                }
            }
        });
    // will be triggered if view sends a 400 bad request response
    // ... anything goes wrong posting the data to our view it will reload the page and
    // display the error without ever charging the user
    }).fail(function () {
        // just reload the page, the error will be in django messages
        location.reload();
    })
});