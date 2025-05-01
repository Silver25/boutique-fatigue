from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.

def view_bag(request):
    """
    docstring / description of the function:
    A simple view to renders the bag contents page
    """
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    # for message strings to work use 'product'
    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # to store/display information of the sizes of the product on shopping bag page
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # variable to temporary store session information,
    # content to the bag and allow user to browse and
    # continue with shoping till browser is open
    bag = request.session.get('bag', {})

    # if statement to check if a product with sizes is being added
    if size:
        # If the item is already in the bag
        if item_id in list(bag.keys()):
            #  need to check if another item of the same id and same size already exists
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                # message use 'product' to inform for products with sizes
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            # otherwise just set it equal to the quantity since the item already exists in the bag
            else:
                bag[item_id]['items_by_size'][size] = quantity
                # message use 'product' to inform for adding a new size for existed item in bag
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        # If the items not already in the bag we just need to add it
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            # message use 'product' to inform for adding the item with a size
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    # otherwise if there's no size we run this next (original) logic
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            # message use 'product' to inform for updating the quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            # message use 'product' to inform for adding items to the bag
            messages.success(request, f'Added {product.name} to your bag!')

    request.session['bag'] = bag
    # to test form for adding product to bag 'print' the shopping bag
    # from the session in the add_to_bag view, check in the console
    # result when click button 'Add to bag' {'1' : 1, '13' : 3}
    # print(request.session['bag'])  = just for the TEST of the Form
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount
    (views to handle updating product quantities and removing them from the bag entirely)
    """

    # for message strings to work use 'product'
    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            # message use 'product' to inform for products with sizes
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
                # message use 'product' to inform for adding a new size for existed item in bag
                messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            # message use 'product' to inform for updating the quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            # message use 'product' to inform for removed from bag here when removing items
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    # for message strings to work use 'product'
    product = get_object_or_404(Product, pk=item_id)

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
