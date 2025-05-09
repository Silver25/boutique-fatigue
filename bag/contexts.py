from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    # to display total cost on the shopping bag page and elsewhere
    # with the new context processor 'bag'
    for item_id, item_data in bag.items():

        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
            
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    # REPAIRED to display/render Qty selector box with quantity number on bag page
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        # to get free delivery, get user know how much more they need to spend
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total
        
    # context processor dictionary
    # add all these items to the context so they'll be available in templates across the site
    # A Context is a dictionary with variable names as the key and their values as the value. 
    # If context for the 'home/index.html' template looks like: {myvar1: 101, myvar2: 102}, 
    # when it's passed this context to the template render method, {{ myvar1 }} would be replaced with 101 
    # and {{ myvar2 }} with 102 in template. 
    # A Context object is the context in which the template is being rendered.
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
