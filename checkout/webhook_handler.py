from django.http import HttpResponse

'''
    If the user somehow intentionally or accidentally closes the browser window 
    after the payment is confirmed but before the form is submitted a payment
    would be processed in stripe but no order will show in database.
    This could result in a customer being charged and never receiving a
    confirmation email or even worse never receiving what they ordered.
    Each time an event occurs on Stripe such as a payment intent being created
    Stripe sends out what's called a webhook sustem can listen for.
    Webhooks are like the 'signals' Django sends each time a model is saved or deleted.
'''


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
