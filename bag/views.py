from django.shortcuts import render, redirect

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
    # variable to temporary store session information,
    # content to the bag and allow user to browse and
    # continue with shoping till browser is open
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    # to test form for adding product to bag 'print' the shopping bag
    # from the session in the add_to_bag view, check in the console
    # result when click button 'Add to bag' {'1' : 1, '13' : 3}
    print(request.session['bag'])
    return redirect(redirect_url)
