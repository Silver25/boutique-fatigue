from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe

'''
    In order to test webhooks, website needs a URL that Stripe can access to
    send webhooks to and from. To get this functionality in local IDE environment,
    we'll use the Stripe CLI in the terminal of VS Code.
    The installation guide for Stripe CLI on Windows:
    https://codeinstitute.s3.eu-west-1.amazonaws.com/vscode-migration-pdf-guides/stripe-cli-installation-guide-windows.pdf
'''


@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WH_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    except Exception as e:
        return HttpResponse(content=e, status=400)

    print('Success!')
    return HttpResponse(status=200)
