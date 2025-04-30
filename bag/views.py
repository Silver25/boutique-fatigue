from django.shortcuts import render, redirect, reverse

# Create your views here.

def view_bag(request):
    """
    docstring / description of the function:
    A simple view to renders the bag contents page
    """
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

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
            # otherwise just set it equal to the quantity since the item already exists in the bag
            else:
                bag[item_id]['items_by_size'][size] = quantity
        # If the items not already in the bag we just need to add it
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    # otherwise if there's no size we run this next (original) logic
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

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

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))
